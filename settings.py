"""
Settings for this program

Some useful settings used to interact with the Trello object
"""
from dotenv import load_dotenv, find_dotenv
import os

# Useful urls to the apis
LISTS_URL = "https://api.trello.com/1/boards/{}/lists"
LABELS_URL = "https://api.trello.com/1/boards/{}/labels"
CARDS_URL = "https://api.trello.com/1/lists/{}/cards"
ADD_CARD_URL = "https://api.trello.com/1/cards"
BOARDS_URL = "https://api.trello.com/1/members/me/boards"

# Read from .env about key and token
find_dotenv(raise_error_if_not_found=True)
load_dotenv()
API_KEY = os.getenv("apikey")
API_TOKEN = os.getenv("apitoken")
