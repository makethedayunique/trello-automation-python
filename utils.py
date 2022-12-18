import requests
from settings import API_KEY, API_TOKEN

class Requester:
    """A class wrap up the get and post function
    
    This is the class which will handle get and post requests to Trello endpoint
    """
    def __init__(self):
        # Initiate the key and token from the .env file
        self.key = API_KEY
        self.token = API_TOKEN
        self.headers = {"Accept": "application/json"}
        self.query = {
          'key': self.key,
          'token': self.token
        }
    
    def send_get_request(self, url, params={}):
        result = {}
        # Append the initialized params into the query
        for key in self.query:
            params[key] = self.query[key]
        # Send the request and get the response
        res = requests.get(url, params=params, headers=self.headers, timeout=5)
        if 200 <= res.status_code < 300:
            result["status"] = True
        else:
            result["status"] = False
            result["error"] = res.text
            return result
        # If successfully, send out the json retrieved
        try:
            result["json_content"] = res.json()
        except:
            # If the result can not be transfered into json, return None
            result["json_content"] = None
        return result
    
    def send_post_request(self, url, params={}):
        result = {}
        # Append the key, token parameters into the query
        for key in self.query:
            params[key] = self.query[key]
        # Send the request and get the response
        res = requests.post(url, params=params, headers=self.headers, timeout=5)
        if 200 <= res.status_code < 300:
            result["status"] = True
        else:
            result["status"] = False
            result["error"] = res.text
        # Return the result
        return result