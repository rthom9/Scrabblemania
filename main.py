import client
import dictionary_client
import requests
import threading
import copy
import sys
from userUI import set_timer, start_timer, cancel_timer, monitor_timer


letter_frequency_dict = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1,
    "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6,
    "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1,
}

letter_points = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, 
    "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, 
    "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10,
}

commands = {
    "play": "Ready to submit a word.",
    "shuffle": "Shuffle your current letters.",
    "swap": "Swap all of your current letters.",
    "definition": "Lookup definition of last submitted word.",
    "finished": "End your session.",
    "undo": "Undo most recent word submission.",
    "commands": "See this list again."
}


def game_timer(game, time_limit):
    cancel_timer()              # in cases where timer is already running
    set_timer(time_limit)
    start_timer()
    monitor_timer()
    game.game_state = "OFF"


class Game:
    def __init__(self, letter_frequency_dict, letter_points):
        self.letter_frequency_dict = letter_frequency_dict
        self.letter_points = letter_points
        self.letter_bag = []
        self.game_time = None
        self.reminder_time_1 = None
        self.reminder_time_2 = None
        self.game_state = "OFF"
        self.player = None
    
    def start_game(self):
        self.make_letter_bag()
        p1 = Player()
        self.player = p1
        p1.new_letters(self.letter_bag)
        self.game_state = "ON"

    def make_letter_bag(self):
        letter_bag = []
        for letter in self.letter_frequency_dict:
            frequency = self.letter_frequency_dict[letter]
            while frequency > 0:
                letter_bag.append(letter)
                frequency -= 1
        self.letter_bag = letter_bag
    
    def definition_lookup(self, player):
        definitions = dictionary_client.dictionary_lookup(player.submitted_words[-1][0], 2)
        for definition in definitions:
            print(definition)
            print("")
  

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
        print("")

    def shuffle_player_letters(self):
        number_of_letters = len(self.letters)
        self.letters = client.randomize_request(self.letters, number_of_letters)
        print(f"Your letters: {self.letters}")
        print("")
    
    def word_validation(self, word):
        # Same length
        players_letters = copy.deepcopy(self.letters)
        for letter in word:
            if letter.upper() not in players_letters:
                return False
            players_letters.remove(letter)
        if dictionary_client.dictionary_lookup(word) == "Invalid word":
            return False
        
        return True

    def user_word_submission(self, game):
        """Prompts player to submit word. If valid, displays score of word, updates player's total score, removes used letters from letter_bag."""
        score = 0
        word_entry = input("Enter your word submission: ").upper()
        if self.word_validation(word_entry):
            for letter in word_entry:
                score += letter_points[letter]
                # remove used letter from current letter bag
                game.letter_frequency_dict[letter] -= 1
            game.make_letter_bag()
            self.score += score
            print(f"Your word scored {score} points. Your current total is {self.score} points.")
            self.submitted_words.append([word_entry, self.letters, score])
            self.new_letters(game.letter_bag)
        else:
            print("Invalid word submission. Try again.")
            print("")

          

def introduction():
    print("")
    print("Welcome to ScrabbleMania!")
    print("Use this application to practice your word finding skills!")
    print("")
    print("You will be given a set of 7 letters from the letter bag. Enter your best word. \nOnce the bag is near "
          "empty, you will be given only the remaining letters.")
    print("Enter the commands listed below to navigate this game.")
    print("")
    command_display(commands)
    

def command_display(commands):
    # print("")
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

def finished(game):
    game.game_state = "OFF"
    cancel_timer()
    print("")
    

def command_controller(command_type, game):
    match command_type:
            case "play":
                game.player.user_word_submission(game)
            case "shuffle":
                game.player.shuffle_player_letters()
            case "swap":
                game.player.new_letters(game.letter_bag)
            case "definition":
                game.definition_lookup(game.player)
            case "finished":
                finished(game)
            case "undo":
                last_played = game.player.submitted_words[-1]
                last_played_word = last_played[0]
                last_played_letters = last_played[1]
                last_played_score = last_played[2]

                # update player's socre
                print(f"Undid [{last_played_word}] entry.")
                print("")
                game.player.score -= last_played_score
                game.player.letters = last_played_letters
                print(f"Your letters: {game.player.letters}")
            case "commands":
                command_display(commands)
                print(f"Your letters: {game.player.letters}")


def game_loop(game, player):
    while game.game_state == "ON":
        command_type = input("Enter command: ")
        command_controller(command_type, g1)

    print(f"Thanks for playing! Your total score was {player.score}")
    send_email_response = input("Would you like an email containing your submmitted words (yes/no)? ")
    if send_email_response == "yes":
        email_address = input("What is your email address? ")
        subject = "Scrabble Mania - Your submitted words!"
        content = "Words played: "
        for word in player.submitted_words:
            content += f" {word[0]} "
        send_email(email_address, subject, content)
        print("Email sent. Goodbye.")
        print("")
    elif send_email_response == "no":
        print("No email sent. Goodbye.")
        print("")
    # sys.exit()


#Start Game
introduction()
g1 = Game(letter_frequency_dict, letter_points)

time_limit = input("Set a time limit for your game. Please use HHMMSS format: ")
game_timer_thread = threading.Thread(target=game_timer, args=(g1, time_limit))
game_loop_thread = threading.Thread(target=game_loop)

g1.start_game()
game_timer_thread.start()
game_loop(g1, g1.player)
game_timer_thread.join()

