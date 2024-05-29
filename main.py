import client
import json
import requests
from userUI import set_timer, start_timer, pause_timer, cancel_timer


letter_frequency_dict = {
    "A": 9, "B": 2,} 
    
#     "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, 
#     "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6, 
#     "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1,
# }

letter_points = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, 
    "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, 
    "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10,
}

commands = {
    "play": "Ready to submit a word.",
    "shuffle": "Shuffle your current letters.",
    "swap": "Swap all of your current letters.",
    "finished": "End your session.",
    "restart": "End current session and restart.",
    "commands": "See this list again."
}

class Game:
    def __init__(self, letter_frequency_dict, letter_points):
        self.letter_frequency_dict = letter_frequency_dict
        self.letter_points = letter_points
        self.letter_bag = []
    
    def make_letter_bag(self):
        letter_bag = []
        for letter in self.letter_frequency_dict:
            frequency = self.letter_frequency_dict[letter]
            while frequency > 0:
                letter_bag.append(letter)
                frequency -= 1
        self.letter_bag = letter_bag
  

class Player:
    def __init__(self):
        self.letters = []
        self.score = 0
        self.submitted_words = []
    
    def new_letters(self, letter_bag, number_of_letters=7):
        if len(letter_bag) < 7:
            number_of_letters = len(letter_bag)
        self.letters = client.randomize_request(letter_bag, number_of_letters)
        print(f"Your letters: {self.letters}")

    def shuffle_player_letters(self):
        number_of_letters = len(self.letters)
        self.letters = client.randomize_request(self.letters, number_of_letters)
        print(f"Your letters: {self.letters}")
    
    def user_word_submission(self, game):
        """Prompts player to submit word. If valid, displays score of word, updates player's total score, removes used letters from letter_bag."""
        valid_word = True
        score = 0
        word_entry = input("Enter your word submission: ")
        for letter in word_entry:
            if letter.upper() not in self.letters:
                valid_word = False
        if not valid_word:
            print("Invalid word submission. Try again.")
            self.user_word_submission()
        else:
            for letter in word_entry:
                letter = letter.upper()
                score += letter_points[letter]
                # remove used letter from current letter bag
                game.letter_frequency_dict[letter] -= 1
            game.make_letter_bag()
            self.score += score
            print(f"Your word scored {score} points. Your current total is {self.score} points.")

            # Display new letters to user
            self.new_letters(game.letter_bag)
            

def introduction():
    print("")
    print("Welcome to ScrabbleMania!")
    print("Use this application to practice your word finding skills!")
    print("")

    print("You have been given a set of 7 letters from the letter bag. Enter your best word. Once the bag is near empty, you will be given only the remaining letters.")
    print("")

def command_display(commands):
    print("")
    print("COMMANDS:")
    for command in commands:
        print(f"{command}: {commands[command]}")
    print("")

def send_email(email_address, subject, content):
    req = {"email": email_address, 
           "subject": subject, 
           "content": content
    }
    requests.post("http://127.0.0.1:5000", json=req)

def finished(player):
    print("")
    print(f"Thanks for playing! Your total score was {player.score}")
    send_email_response = input("Would you like an email containing your submmitted words (yes/no)? ")
    if send_email_response == "yes":
        email_address = input("What is your email address? ")
        subject = "Scrabble Mania - Your submitted words!"
        content = "Words played: "
        for word in player.submitted_words:
            content += f" {word} "
        send_email(email_address, subject, content)
    elif send_email_response == "no":
        print("No email sent. Goodbye.")
    exit()

def command_controller(command_type, game, player):
    match command_type:
            case "play":
                player.user_word_submission(game)
            case "shuffle":
                player.shuffle_player_letters()
            case "swap":
                player.new_letters(game.letter_bag)
            case "finished":
                finished(player)
            case "restart":
                print("restart entry")
            case "commands":
                command_display(commands)
                print(f"Your letters: {player.letters}")




g1 = Game(letter_frequency_dict, letter_points)
g1.make_letter_bag()
p1 = Player()
introduction()
command_display(commands)

p1.new_letters(g1.letter_bag)

while True:
    command_type = input("Command: ")
    command_controller(command_type, g1, p1)
        
# send_email("thomrobert9@gmail.com", "Yoyoboy!", "It's your time shawty")
# set_timer("000006","000005","000002")
# start_timer()
# print(user_current_letters)


