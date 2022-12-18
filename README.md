# trello-automation-python

This is a Trello automation tool which provides you with approaches to add cards to your Trello workspaces. 

## Instructions

#### Step 1: Get your developer key and token

To run this program, you need to have your own api key and token for authentication.

- Go to [Trello Admin](https://trello.com/power-ups/admin)

- Navigate to "Power-Ups" under "App", if you already have any power-ups that you want to use, you can directly click on that power-up. Otherwise, click "New" to create a new power-up.

- After creating and clicking into the power-up, navigate to "API key". You will see the "API key" and remember it. Then click on the hyperlink "Token" on the right side of API key to generate a token and remember this token.

#### Step 2: Replace the sample.env with your own secrets

You need to rename the "sample.env" with ".env" by deleting prefix "sample". And put your api key and token to the ".env" file as follows:

```python
apikey=yourapikey
apitoken=yourapitoken
```

#### Step3: Install the dependencies

Run the following command in your terminal to install the necessary dependencies. You may replace the "/path/to/" according to your environment.

```shell
pip install -r /path/to/requirements.txt
```

#### Step 4: Run the program

The entry of the program is "trello-automation-python/app.py", you can either run it from an editor with python interpreter or the terminal.

For terminal running, get inside of "trello-automation-python/" and run:

```shell
python3 app.py
```

You will see the welcome message and you can add cards to your Trello workspace following the prompt.

```javadoc
===============================^^==============================
Welcome to the Trello CLI program!
Are you ready to add a card to your board? (y/n)
```

## Next Steps

- Execute tests for the the program. Based on the following tests, add more error checking and fix bugs.
  
  - Write unit tests to test each function by inputting invalid values. 
  
  - Write integration tests to test whether the program can work well under different situations.

- Modify the user interface. Even if it is a CLI program, there could be much modification to make it more user friendly for users.

- Make it tested among users and collect feedbacks. Constantly modify the code based on the feedbacks.

- Add more functions to the program to add more values. Such as adding columns and labels.
