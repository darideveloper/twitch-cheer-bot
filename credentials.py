import os
from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv("API_HOST")
TOKEN = os.getenv("TOKEN")
PORT = os.getenv("PORT")
CHROME_PATH = os.getenv("CHROME_PATH")
DEBUG_USERS = os.getenv("DEBUG_USERS")
if DEBUG_USERS:
    DEBUG_USERS = DEBUG_USERS.split(",")
else:
    DEBUG_USERS = []
