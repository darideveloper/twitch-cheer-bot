import os
import requests
from credentials import API_HOST, TOKEN


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

    def get_donations(self) -> dict:
        """ Get donations of the current live streams in comunidad mc, using the API

        Returns:
            dict: donations data.

            Example:
            [
                {
                    'id': 20,
                    'user': 'soyunfarsantee', 
                    'admin': 'daridev-admin', 
                    'stream_chat_link': 'https://www.twitch.tv/popout/blue_rebel_/chat?popout=', 
                    'time': '00:21:51', 
                    'amount': 1, 
                    'message': 'Holaaaaa', 
                    'cookies': [...] 
                }
                ...
            ]
        """

        print("getting donations...")

        # Get data from api
        res = self.__requests_url__("donations")
        return res.json()
        
if __name__ == "__main__":
    api = Api()
    data = api.get_donations()
    print (data)