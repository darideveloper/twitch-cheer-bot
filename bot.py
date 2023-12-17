import sys
from time import sleep
from datetime import datetime
from threading import Thread
from random import randint

from api import Api
from chrome_dev.chrome_dev import ChromDevWrapper
from credentials import PORT, DEBUG_USERS, DEBUG_MODE, CHROME_PATH

class Bot ():
    
    def __init__ (self): 
        """ Start threads to send donations to twitch chat
        """
         
        # variables
        self.api = Api()
        self.selectors = {
            'twitch_login_input': '#login-username',
            'comment_textarea': '[data-a-target="chat-input"]',
            'comment_send_btn': 'button[data-a-target="chat-send-button"]',
            'comment_accept_buttons': [
                'button[data-test-selector="chat-rules-ok-button"]',
                'button[data-test-selector="chat-rules-show-intro-button"]',
            ],
            'comment_warning_before': '[data-test-selector="chat-rules-ok-button"]',
            'comment_warning_after': '[data-test-selector="full-error"], [data-test-selector="inline-error"]',
        }
        self.running = False
        self.error = False
        
        # Get data from api
        data = self.api.get_donations()
        donations = data["donations"]
        print ()
        
        if not donations:
            self.__show_message__ ("No donations to send")
            return None
        
        # Submit each donation
        threads = []
        for donation in donations:
            
            if DEBUG_USERS and donation["user"] not in DEBUG_USERS:
                continue
            
            # Format data
            id = donation["id"]
            user = donation["user"]
            stream_chat_link = donation["stream_chat_link"]
            time = donation["time"]
            message = donation["message"]
            amount = donation["amount"]
            
            # Get streamer name
            streamer = stream_chat_link.split("/")[4]
            
            # Show donation data       
            self.__show_message__ (f"bot: '{user}', time: {time}, stramer: '{streamer}', message: '{message}', amount: {amount}", donation["id"]) 
            
            # Submit donation with thread
            thread = Thread (target=self.submit_donation, args=(id, stream_chat_link, user, time, message, amount))
            thread.start()
            threads.append (thread)
            
        # Wait for threads to end
        while True:
            if threads and any ([thread.is_alive() for thread in threads]):
                sleep (1)
                continue
            
            # Raise error when end
            if self.error:
                sys.exit (1)

            break
        
    def __show_message__ (self, message:str, id:int=0, is_error:bool=False):
        """ print error message

        Args:
            id (int): id of the donation
            message (str): error text
            is_error (bool, optional): if the message is an error. Defaults to False.
        """
        
        prefix = "Info: "
        if is_error:
            prefix = "Error: "
            self.error = True
            
        if id != 0:
            prefix += f"Donation {id}: "
        
        print (f"{prefix}{message}")
        
    def __login__ (self, id:int, user:str, scraper:ChromDevWrapper)-> bool:
        """ Validate login in twitch

        Args:
            id (int): donation id
            user (str): bot name
            scraper (ChromDevWrapper): chrome dev wrapper instance

        Returns:
            bool: True if the login was successful
        """
        
        logged = True
        
        # Validate login
        scraper.set_page ("https://www.twitch.tv/login")    
        login_input_visible = scraper.count_elems (self.selectors["twitch_login_input"])
        if login_input_visible:
            
            # Show error and update status
            self.__show_message__ (f"login error, bot: {user}", id, is_error=True)
            logged = False
            
            #  Disable user in
            response = self.api.disable_user (user)
            if response != "User disabled":
                self.__show_message__ (f"bot {user} not disabled", id, is_error=True)
                                       
        return logged 
    
    def __validate_inputs__ (self, id:int, scraper:ChromDevWrapper) -> bool:
        """ Validate if inputs are visible and available

        Args:
            id (int): donation id
            scraper (ChromDevWrapper): chrome dev wrapper instance

        Returns:
            bool: True if inputs are visible and available
        """
        
        inputs_valid = True
        
        # Validate if constrols are visible
        comment_textarea_visible = scraper.count_elems (self.selectors["comment_textarea"])
        comment_send_btn_visible = scraper.count_elems (self.selectors["comment_send_btn"])
        if not comment_textarea_visible or not comment_send_btn_visible:
            self.__show_message__ ("inputs not visible", id, is_error=True)
            inputs_valid = False
            
        # Validate error messages
        warning_text = scraper.get_text (self.selectors["comment_warning_before"])
        if warning_text:
            self.__show_message__ (f"Inputs not available: {warning_text}", id, is_error=True)
            inputs_valid = False
            
        return inputs_valid
    
    def __validate_submit__ (self, id:int, scraper:ChromDevWrapper) -> bool:
        """ Validate if donation was send

        Args:
            id (int): donation id
            scraper (ChromDevWrapper): chrome dev wrapper instance
            
        Returns:
            bool: True if donation was send
        """
        
        donation_sent = True
        
        warning_text = scraper.get_text (self.selectors["comment_warning_after"])
        if warning_text:
            self.__show_message__ (f"Donation not send: {warning_text}", id, is_error=True)
            donation_sent = False
            
        return donation_sent
        
    def submit_donation (self, id:int, stream_chat_link:str, user:str,
                         time_str:str, message:str, amount:int):
        """ Send donation to twitch chat

        Args:
            id (int): donation id
            stream_chat_link (str): link to the chat of the stream
            user (str): bot name
            time (str): time text in format "hh:mm:ss"
            message (str): message to send
            amount (int): bits of the donation
        """
        
        # Wait random seconds
        sleep (randint (0, 15))
                
        # Donation time
        donation_time = datetime.strptime (time_str, "%H:%M:%S")
        now = datetime.now ()
        donation_time = donation_time.replace (year=now.year, month=now.month, day=now.day)
        
        # Validate lost donation times
        if now > donation_time:
            self.__show_message__ ("time lost", id, is_error=True)
            self.running = False
            return None
                
        # Wait until donation time
        while donation_time > now:
            sleep (15)
            now = datetime.now ()
            
        # Update status or wait until other donations are send
        if not self.running: 
            self.running = True
        else:
            while self.running:
                sleep (randint (0, 5))
        
        # Show start donation status 
        self.__show_message__ ("starting...", id)
        
        # Connect to chrome
        scraper = ChromDevWrapper(
            chrome_path=CHROME_PATH,
            port=PORT
        )
        
        # Login in twitch and validate
        logged = self.__login__ (id, user, scraper)
        if not logged:
            self.running = False
            return None
                    
        # Go to chat page
        scraper.set_page (stream_chat_link)
        sleep (10)
        
        # Validate inputs
        inputs_valid = self.__validate_inputs__ (id, scraper)
        if not inputs_valid:
            self.running = False
            return None
        
        # Write message
        donation_text = f"cheer{amount} {message}"
        scraper.send_data (self.selectors["comment_textarea"], donation_text)
        sleep (5)
        
        # Click in accept buttons
        for selector in self.selectors["comment_accept_buttons"]:
            
            accept_elem = scraper.count_elems (selector)
            if accept_elem:
                scraper.click (selector)
                
                # Write message (again)
                donation_text = f"cheer{amount} {message}"
                scraper.send_data (self.selectors["comment_textarea"], donation_text)
                
        # Submit donation
        if not DEBUG_MODE:
            scraper.click (self.selectors["comment_send_btn"])
        
        donation_sent = self.__validate_submit__ (id, scraper)
        if donation_sent:
            self.__show_message__ ("sent", id)
        
        self.running = False
        
        # Update donation status
        if not DEBUG_MODE:
            response = self.api.set_donation_done (id) 
            if response != "Donation updated":
                self.__show_message__ ("not updated", id, is_error=True)

if __name__ == "__main__":
    bot = Bot ()