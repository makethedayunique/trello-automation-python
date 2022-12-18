"""
This is the trello add-card CLI program

It will prompt the users to create cards to any columns in their boards
step by step. The user will see the most up-to-date options related to
their workspace.
"""
from utils import Requester
from models import Requester, Board, Column
from settings import BOARDS_URL
import sys

def print_values(values):
    # This function will print the iterable along with their indexes
    if len(values) == 0:
        print("There is nothing in this list")
    for i, value in enumerate(values):
        print("{}. {}".format(i + 1, value))

def show_select_boards(requester: Requester):
    # This function will handle the show boards and select from boards
    # It will return a status, a message and the board selected
    # Status: 0 - proceed to next; 1 - error, exit program; 2 - return to main
    
    # Load and display the boards
    print("Loading Boards From Your Work Spaces...")
    boards_res = requester.send_get_request(BOARDS_URL)
    
    if not boards_res["status"]:
        err_msg = "Failed to connect to your Trello space because: {}".format(boards_res["error"])
        return (1, err_msg, None)
    boards = []
    # Render the boards into Board objects
    for board_info in boards_res["json_content"]:
        new_board = Board(board_info, requester)
        boards.append(new_board)
    # If there is no boards
    if len(boards) == 0:
        err_msg = "There is no board in your workspace, please add a board before you can add a card."
        return (1, err_msg, None)
    
    print_values(boards)
    ret_to_main = False # Whether return to the main loop
    board_selection = None # The selection
    
    while True:
        board_selection = input("Select from the above boards by its index, input 'x' to stop: ")
        if board_selection == "x":
            ret_to_main = True
            break
        if not board_selection.isdigit():
            print("Invalid input, you must input a valid integer number")
            continue
        board_selection = int(board_selection)
        if board_selection <= 0 or board_selection > len(boards):
            print("Invalid input, you must select from the above boards")
            continue
        if boards[board_selection - 1].is_close():
            print("The selected board is closed, please select another one")
            continue
        break
    if ret_to_main:
        return (2, "", None)
    # Return the board
    return (0, "", boards[board_selection - 1])

def show_select_cols(board: Board):
    # This function will handle show columns and select from columns
    # Return state, message, column selected
    # 0 - success, 1 - error, 2 - return to main
    
    # Load and display the columns
    print("You are now in board: {}". format(board.get_name()))
    print("Loading Columns From Your Board...")
    
    cols = board.get_cols()
    
    # If there is no cols
    if len(cols) == 0:
        err_msg = "There is no columns in your workspace, please add a column before you can add a card."
        return (1, err_msg, None)
    
    print_values(cols)
    ret_to_main = False # Whether return to the main loop
    col_selection = None # The selection
    
    while True:
        col_selection = input("Select from the above columnss by its index, input 'x' to stop: ")
        if col_selection == "x":
            ret_to_main = True
            break
        if not col_selection.isdigit():
            print("Invalid input, you must input a valid integer number")
            continue
        col_selection = int(col_selection)
        if col_selection <= 0 or col_selection > len(cols):
            print("Invalid input, you must select from the above columns")
            continue
        if cols[col_selection - 1].is_close():
            print("The selected column is closed, please select another one")
            continue
        break
    if ret_to_main:
        return (2, "", None)
    # Return the board
    return (0, "", cols[col_selection - 1])

def show_cards(col: Column):
    # This function will show all the cards in the column
    print("You are in column: {}, with cards:".format(col.get_name()))
    cards = col.get_cards()
    print_values(cards)

def show_and_select_labels(board: Board):
    # This function will prompt for card name and comment, and labels
    # Return status, name, desc, label_ids
    card_name = None
    # Prompt for card name
    while True:
        card_name = input("== Input your card name ('x' to exit): ")
        if card_name == 'x':
            return False, None, None, None
        if card_name is None or card_name.strip() == "":
            print("Card name must not be empty")
            continue
        break
    # Prompt for card description
    card_desc = input("== Input your card description ('x' to exit): ")
    if card_desc == 'x':
        return False, None, None, None
    # It is allowed that the card description be empty
    label_set = set()
    print("== Available Labels are as follows, you may select one or multiple labels:")
    labels = board.get_labels()
    print_values(labels)
    while True:
        label_selection = input("=====Select from the above labels by index (input 'c' to cancel selection, 'x' to exit): ")
        if label_selection == 'x':
            return False, None, None, None
        if label_selection == 'c':
            break
        if not label_selection.isdigit():
            print("============Invalid input, you must input a valid integer number")
            continue
        label_selection = int(label_selection)
        if label_selection <= 0 or label_selection > len(labels):
            print("============Invalid input, you must select from the above labels")
            continue
        label_set.add(labels[label_selection - 1].get_id())
        print("=====Attached label {}".format(label_selection))
    # Check for whether there are labels selected
    return True, card_name, card_desc, label_set

def main():
    # This is the main logic of the CLI program
    welcome_text = """===============================^^==============================\nWelcome to the Trello CLI program!"""
    print(welcome_text)
    requester = None # The request tool used across the program
    try:
        requester = Requester()
    except:
        print("ERROR! Can not find your key and token!")
        sys.exit()
        
    while True:
        start = input("Are you ready to add a card to your board? (y/n)")
        if start == 'n':
            print("======================= Exited program ========================")
            break
        # Select the board
        board_state, board_err, board = show_select_boards(requester)
        if board_state == 1:
            print(board_err)
            break
        if board_state == 2:
            continue
        # Select the list
        print("===============================================================")
        col_state, col_err, col = show_select_cols(board)
        if col_state == 1:
            print(col_err)
            break
        if col_state == 2:
            continue
        # Select from labels
        print("===============================================================")
        show_cards(col)
        # Prompt for name, labels and comment
        print("===============================================================\nStart Create a new card for column: {}".format(col.get_name()))
        card_state, card_name, card_desc, card_labels = show_and_select_labels(board)
        if card_state:
            col.add_card(card_labels, card_name, card_desc)

if __name__ == "__main__":
    main()
