import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv("API_HOST")
TOKEN = os.getenv("TOKEN")


class Api ():

    def __requests_url__(self, endpoint: str) -> requests.get:
        """ Request data from specific endpoint and and quit if error happens

        Args:
            endpoint (str): endpoint to request, like "users" or "settings"

        Returns:
            requests.get: response of requests to the endpoint
        """

        # Request data to specific url
        url = f"{API_HOST}/{endpoint}/?token={TOKEN}"
        res = requests.get(url)

        if res.status_code == 200:
            return res
        else:
            print("Error requesting data from API. Check your token.")
            quit()

    def get_users(self) -> list:
        """ Get twitch user for the bot, using the API

        Returns:
            list: list of dictionaries with user data

            Example: 
            [
                {
                    "name": "DariDeveloper",
                    "cookies": [...],
                    "is_active": True,
                    "last_update": "2023-04-17T23:29:07.083Z"
                }
                ...
            ]
        """

        print("getting users...")

        # Get data from api
        res = self.__requests_url__("users")
        users = res.json()

        # filter active users
        users = list(filter(lambda user: user["fields"]["is_active"], users))

        # Format users
        users = list(map(lambda user: user["fields"], users))

        return users

    def get_settings(self) -> list:
        """ Get settings for the bot, using the API

        Returns:
            list: dictionary with settings data

            Example: {"viwers_stream": 20}
        """

        print("getting settings...")

        # Get data from api
        res = res = self.__requests_url__("settings")
        settings = res.json()

        # Format settings
        setting_formatted = {}
        for setting in settings:
            key = setting["fields"]["name"]
            value = setting["fields"]["value"].lower().strip()

            # Convert values to int if possible
            if value.isdigit():
                value = int(value)

            # Convert to bool if is possible
            if value == "true":
                value = True

            if value == "false":
                value = False

            setting_formatted[key] = value

        return setting_formatted

    def get_proxies(self) -> list:
        """ Get proxies for the bot, using the API

        Returns:
            list: list of dictionaries with proxy data

            Example:
            [
                {
                    "host": "123.123.123.123",
                    "port": 80,
                    "user": "my user",
                    "password": "my password",
                    "location": 1
                }
                ...
            ]
        """

        print("getting proxies...")

        # Get data from api
        res = res = self.__requests_url__("proxies")
        proxies = res.json()

        # Format proxies
        proxies = list(map(lambda proxy: proxy["fields"], proxies))

        return proxies

    def get_streams(self) -> list:
        """ Get current live streams in comunidad mc, using the API

        Returns:
            list: streamer names.

            Example:  ["DariDeveloper", "darideveloper2"]
        """

        print("getting streams...")

        # Get data from api
        res = self.__requests_url__("streams")
        return res.json()

    def get_donations(self) -> dict:
        """ Get donations of the current live streams in comunidad mc, using the API

        Returns:
            dict: donations data.

            Example:
            [
                {
                    "user": "SoyUnFarsantee",
                    "streamer": "pipevillanu3va",
                    "minute": 10,
                    "amount": 1,
                    "message": "eres un pro",
                    "status": false
                }
                ...
            ]
        """

        print("getting donations...")

        # Get data from api
        res = self.__requests_url__("donations")
        return res.json()
    
    def disable_user (self, username:str): 
        """ Disable user in the API

        Args:
            username (str): user name to disable
        """
        
        res = self.__requests_url__("disable-user/" + username)
        print (f"\t{username}: {res.text}")
        
if __name__ == "__main__":
    api = Api()
    api.disable_user("vegetta_pelon")