import os
from time import sleep
from datetime import datetime
from threading import Thread
from random import randint

from api import Api
from credentials import PORT
from chrome_dev.chrome_dev import ChromDevWrapper

class Bot (ChromDevWrapper):
    
    def __init__ (self): 
        """ Start threads to send donations to twitch chat
        """
         
        # variables
        self.api = Api()
        self.selectors = {
            'twitch-login-btn': 'button[data-a-target="login-button"]',
            'comment_textarea': '[role="textbox"]',
            'comment_send_btn': 'button[data-a-target="chat-send-button"]',
            'comment_accept_btn': 'button[data-test-selector="chat-rules-ok-button"]',
            'comment_warning_before': '.chat-input-tray__clickable',
            'comment_warning_after': '[data-test-selector="full-error"]',
        }
        
        # Connect to chrome
        super().__init__(port=PORT)
        
        # Get data from api
        donations = self.api.get_donations()
        print ()
        
        if not donations:
            self.__show_message__ ("No donations to send")
        
        # Submit each donation
        for donation in donations:
            
            # Format data
            id = donation["id"]
            user = donation["user"]
            stream_chat_link = donation["stream_chat_link"]
            time = donation["time"]
            message = donation["message"]
            amount = donation["amount"]
            cookies = donation["cookies"]
            
            # Get streamer name
            streamer = stream_chat_link.split("/")[4]
            
            # Show donation data       
            self.__show_message__ (f"bot: '{user}', time: {time}, stramer: '{streamer}', message: '{message}', amount: {amount}", donation["id"]) 
            
            # Submit donation with thread
            thread = Thread (target=self.submit_donation, args=(id, user, stream_chat_link, time, message, amount, cookies))
            thread.start()
        
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
            
        if id != 0:
            prefix += f"Donation {id}: "
        
        print (f"{prefix}{message}")
        
    def __login__ (self, cookies:list, id:int)-> bool:
        """ Set cookies to login in twitch

        Args:
            cookies (list): cookies to login in twitch with the bot
            id (int): donation id

        Returns:
            bool: True if the login was successful
        """
        
        logged = True
        
        # Set cookies
        self.delete_cookies ()
        self.set_page ("https://www.twitch.tv/login")
        self.set_cookies (cookies)
        
        # Validate login
        self.set_page ("https://www.twitch.tv/login")    
        login_button_visible = self.count_elems (self.selectors["twitch-login-btn"])
        if login_button_visible:
            
            # Show error and update status
            self.__show_message__ ("cookies error", id, is_error=True)
            logged = False
            
            # TODO: Disable user in backend
            # self.api.disable_user (self.username)
            
        return logged 
    
    def __validate_inputs__ (self, id:int) -> bool:
        """ Validate if inputs are visible and available

        Args:
            id (int): donation id

        Returns:
            bool: True if inputs are visible and available
        """
        
        inputs_valid = True
        
        # Validate if constrols are visible
        comment_textarea_visible = self.count_elems (self.selectors["comment_textarea"])
        comment_send_btn_visible = self.count_elems (self.selectors["comment_send_btn"])
        if not comment_textarea_visible or not comment_send_btn_visible:
            self.__show_message__ ("inputs not visible", id, is_error=True)
            inputs_valid = False
            
        # Validate error messages
        errors = [
            "Followers-Only Chat",
            "Verified Accounts Only Chat",
        ]
        warning_text = self.get_text (self.selectors["comment_warning_before"])
        if warning_text in errors:
            self.__show_message__ (f"Inputs not available: {warning_text}", id, is_error=True)
            inputs_valid = False
            
        return inputs_valid
    
    def __validate_submit__ (self, id:int) -> bool:
        """ Validate if donation was send

        Args:
            id (int): donation id
            
        Returns:
            bool: True if donation was send
        """
        
        donation_sent = True
        
        warning_text = self.get_text (self.selectors["comment_warning_after"])
        if warning_text:
            self.__show_message__ (f"Donation not send: {warning_text}", id, is_error=True)
            donation_sent = False
            
        return donation_sent
        
    def submit_donation (self, id:int, user:str, stream_chat_link:str, 
                         time_str:str, message:str, amount:int, cookies:list):
        """ Send donation to twitch chat

        Args:
            id (int): donation id
            user (str): user that send the donation (bot)
            stream_chat_link (str): link to the chat of the stream
            time (str): time text in format "hh:mm:ss"
            message (str): message to send
            amount (int): bits of the donation
            cookies (list): cookies to login in twitch with the bot
        """
        
        # Wait random seconds
        sleep (randint (0, 60))
        
        # Donation time
        donation_time = datetime.strptime (time_str, "%H:%M:%S")
        now = datetime.now ()
        donation_time = donation_time.replace (year=now.year, month=now.month, day=now.day)
        
        # Validate lost donation times
        if now > donation_time:
            self.__show_message__ ("Donation time lost", id, is_error=True)
            return None
        
        # Wait until donation time
        while donation_time > now:
            sleep (60)
            now = datetime.now ()
            self.__show_message__ (f"Waiting for next donation...")
        
        # Login in twitch and validate
        logged = self.__login__ (cookies, id)
        if not logged:
            return None
                    
        # Go to chat page
        self.set_page (stream_chat_link)
        sleep (5)
        
        # Validate inputs
        inputs_valid = self.__validate_inputs__ (id)
        if not inputs_valid:
            return None
        
        # Write message
        donation_text = f"cheer{amount} {message}"
        self.send_data (self.selectors["comment_textarea"], donation_text)
        
        # # Accept chat rules and submit donation
        # comment_accept_elem = self.count_elems (self.selectors["comment_accept_btn"])
        # if comment_accept_elem:
        #     self.click (self.selectors["comment_accept_btn"])
            
        #     # Write message (again)
        #     donation_text = f"cheer{amount} {message}"
        #     self.send_data (self.selectors["comment_textarea"], donation_text)
            
        # # Submit donation
        # self.click (self.selectors["comment_send_btn"])
        
        # donation_sent = self.__validate_submit__ (id)
        # if donation_sent:
        #     self.__show_message__ ("Donation sent", id)
        


if __name__ == "__main__":
    bot = Bot ()