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
    
    # def disable_donation (self, username:str): 
    #     """ Disable user in the API

    #     Args:
    #         username (str): user name to disable
    #     """
        
    #     res = self.__requests_url__("disable-user/" + username)
    #     print (f"\t{username}: {res.text}")
        
if __name__ == "__main__":
    api = Api()
    data = api.get_donations()
    print (data)