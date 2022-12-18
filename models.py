from utils import Requester
from settings import LISTS_URL, LABELS_URL, CARDS_URL, ADD_CARD_URL

class Label:
    """This is the label class storing the label info"""

    def __init__(self, meta_data):
        self.label_id = meta_data["id"]
        self.label_name = meta_data["name"]
        self.label_color = meta_data["color"]
    
    def get_id(self):
        return self.label_id
    
    def __str__(self):
        return "Label Name: {0}\n   Label Color: {1}".format(self.label_name, self.label_color)

class Card:
    """This is the card class storing the card info"""

    def __init__(self, meta_data):
        self.card_id = meta_data["id"]
        self.card_name = meta_data["name"]
        self.card_desc = meta_data["desc"]
        self.card_labels = [label["color"] for label in meta_data["labels"]]
    
    def get_id(self):
        return self.card_id
    
    def __str__(self):
        return "Card Name: {0} -- With Labels {1}".format(self.card_name, ", ".join(self.card_labels))

class Column:
    """This is the class of the list in a board"""

    def __init__(self, meta_data, requester: Requester):
        self.col_id = meta_data["id"]
        self.col_name = meta_data["name"]
        self.col_closed = meta_data["closed"]
        self.col_cards = {} # List of the cards objects in the column
        self.requester = requester
    
    def __retrieve_cards(self):
        # This function will retrieve the current cards in this column and update
        labels_url = CARDS_URL.format(self.col_id)
        res = self.requester.send_get_request(labels_url)
        if not res["status"]:
            print("====== Oops, there seems to have something wrong: {}".format(res["error"]))
            return
        # Otherwise, update the current cards
        for card_info in res["json_content"]:
            new_card = Card(card_info)
            self.col_cards[new_card.get_id()] = new_card
    
    def add_card(self, labels, name, desc=""):
        # This function will create a new card on the column
        label_ids = []
        if type(labels) == Label:
            label_ids.append(labels.get_id())
        else:
            for label in labels:
                if type(label) == Label:
                    label_ids.append(label.get_id())
                elif type(label) == str:
                    label_ids.append(label)
        
        params = {
            "name": name,
            "desc": desc,
            "idList": self.col_id,
            "idLabels": label_ids
        }
        add_card_url = ADD_CARD_URL
        # Send the post request
        res = self.requester.send_post_request(add_card_url, params)
        if not res["status"]:
            print("Failed! {}".format(res["error"]))
        else:
            print("Successfully inserted a card to column {0}".format(self.col_name))
    
    def get_cards(self):
        # This function will return the cards objects of the column
        self.__retrieve_cards()
        return list(self.col_cards.values())
    
    def get_name(self):
        return self.col_name
    
    def get_id(self):
        return self.col_id
    
    def is_close(self):
        return self.col_closed
    
    def __str__(self):
        return "Column Name: {0}\n   Status: {1}".format(self.col_name,
                                                         "Active" if not self.col_closed else "Closed")
    
class Board:
    """This is the board class
    
    This is the class of the board which provides functions to list the cards
    and insert cards and save it to the endpoint
    """
    def __init__(self, meta_data, requester: Requester):
        self.board_id = meta_data["id"]
        self.board_name = meta_data["name"]
        self.board_desc = meta_data["desc"]
        self.board_closed = meta_data["closed"]
        self.lists = {} # List of the list objects in this board
        self.labels = {} # List of the label objects in this board
        self.requester = requester
    
    def __retrieve_cols(self):
        # This function will retrieve about the latest lists
        lists_url = LISTS_URL.format(self.board_id)
        res = self.requester.send_get_request(lists_url)
        if not res["status"]:
            print("====== Oops, there seems to have something wrong")
            return
        # Otherwise, update the current lists
        for list_info in res["json_content"]:
            new_col = Column(list_info, self.requester)
            self.lists[new_col.get_id()] = new_col
        
    def __retrieve_labels(self):
        # This function will retrieve all the latest labels and update
        labels_url = LABELS_URL.format(self.board_id)
        res = self.requester.send_get_request(labels_url)
        if not res["status"]:
            print("====== Oops, there seems to have something wrong")
            return
        # Otherwise, update the current labels
        for label_info in res["json_content"]:
            new_label = Label(label_info)
            self.labels[new_label.get_id()] = new_label
    
    def get_cols(self):
        # This function will update columns first and then return the latest columns
        self.__retrieve_cols()
        return list(self.lists.values())

    def get_labels(self):
        # This function will update labels first and then return the latest labels
        self.__retrieve_labels()
        return list(self.labels.values())
    
    def is_close(self):
        # This function will return whether the board is close
        return self.board_closed
    
    def get_name(self):
        # This function will return the name of the board
        return self.board_name
    
    def __str__(self):
        return "Board Name: {0}\n   Description: {1}\n   Status: {2}".format(self.board_name, 
                                                                              self.board_desc, 
                                                                              "Active" if not self.board_closed else "Closed")
    
    