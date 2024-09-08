# Author: Robert Thom
# GitHub username: rthom9
# Description: Scrabblemania is a console application that allows users to create high-scoring words
# from random letters. This project was used to explore the fundamental ideas of microservice architecture and 
# uses dictionary_lookup, randomizer, and email microservices.
# This application mimics aspects of Scrabble including a 7-letter player rack, use of 
# a letter bag, and similar letter scoring sytem.  

import randomizer_client
import dictionary_client
import requests
import threading
import copy
import time

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


class Game:
    """A class to represent a ScrabbleMania Game. Class contains start_game, make_letter_bag, and
    definition_lookup, command_controller, game_loop, and finished methods."""
    
    def __init__(self, letter_frequency_dict, letter_points, commands):
        self.letter_frequency_dict = letter_frequency_dict
        self.letter_points = letter_points
        self.commands = commands
        self.letter_bag = []
        self.game_time = None
        self.game_state = "OFF"
        self.stop_timer = False
        self.player = None
    
    def game_timer(self):
        
        hours_int = int(self.game_time[0:2])
        minutes_int = int(self.game_time[2:4])
        seconds_int = int(self.game_time[4:6])
        t = (hours_int * 3600) + (minutes_int * 60) + seconds_int
        while t and self.game_state == "ON":
            time.sleep(1)
            t -= 1
        if not self.stop_timer:
            print("\n\nTime is up! Press [ENTER] to view your score.")
            self.game_state = "OFF"

    def start_game(self):
        """Starts game by making a letter bag, creating a player object, generating player's random starting
         letters and settting game state to "ON". """
        
        self.introduction()
        self.make_letter_bag()
        p1 = Player()
        self.player = p1
        p1.new_letters(self.letter_bag)
        self.game_state = "ON"
    
    def introduction(self):
        """Displays initial instructions to user."""
    
        print("")
        print("Welcome to ScrabbleMania!")
        print("Use this application to practice your word finding skills!")
        print("")
        print("You will be given a set of 7 letters from the letter bag. Enter your best word. \nOnce the bag is near "
            "empty, you will be given only the remaining letters.")
        print("Enter the commands listed below to navigate this game.")
        print("")
        command_display(self.commands)
        print("")
        self.game_time = input("Set a time limit for your game. Please use HHMMSS format: ")

    def make_letter_bag(self):
        """Creates letter bag represented as list by adding letters based upon frequency detailed in 
        letter_frequency_dict."""
        
        letter_bag = []
        for letter in self.letter_frequency_dict:
            frequency = self.letter_frequency_dict[letter]
            while frequency > 0:
                letter_bag.append(letter)
                frequency -= 1
        self.letter_bag = letter_bag
    
    def definition_lookup(self, player):
        """Uses dictionary microservice to obtain definitions of most recently submitted word."""
        if not player.submitted_words:
            print("No words yet played.")
            print("")
        else:
            definitions = dictionary_client.dictionary_lookup(player.submitted_words[-1][0], 2)
            print("")
            for definition in definitions:
                print(definition)
                print("")
            print(f"Your letters: ", " ".join(self.player.letters))
    
    def undo(self):
        
        if not self.player.submitted_words:
            print("No words yet played.")
        else:
            last_played = self.player.submitted_words[-1]
            last_played_word = last_played[0]
            last_played_letters = last_played[1]
            last_played_score = last_played[2]

            "Display player's last entered word."
            print(f"Undid [{last_played_word}] entry.")
            print("")

            "Remove last played word score from player's score."
            self.player.score -= last_played_score

            "Restore player's previous letter selection."
            self.player.letters = last_played_letters
            print(f"Your letters: ", " ".join(self.player.letters))


    def command_controller(self, command_type):
        """Executes appropriate functions based upon user's command entry."""
        
        match command_type:
                case "play":
                    self.player.user_word_submission(self)
                case "shuffle":
                    self.player.shuffle_player_letters()
                case "swap":
                    self.player.swap_letters(self.letter_bag)
                case "definition":
                    self.definition_lookup(self.player)
                case "finished":
                    self.finished()
                case "undo":
                    self.player.undo()
                case "commands":
                    command_display(commands)
                    print(f"Your letters: ", " ".join(self.player.letters))

    def game_loop(self):
        """Will prompt user for command entry until game is finished."""
        
        while self.game_state == "ON":
            command_type = input("Enter command: ")
            self.command_controller(command_type)
        self.player.farewell()
    
    def finished(self):
        """Updates game_state to "OFF", stops timer."""
        
        self.game_state = "OFF"
        self.stop_timer = True
        print("")
  

class Player:
    """A class to represent a player. Contains letters, score and submitted_words as data members. 
    Class contains new_letters, swap_letters, shuffle_player_letters, word_validation, user_word_submission, 
    undo, and farewell methods."""
    
    def __init__(self):
        self.letters = []
        self.score = 0
        self.submitted_words = []
    
    def new_letters(self, letter_bag, number_of_letters=7):
        """Utilizes randomizer microservice to update player's letters with random assortment from letter_bag."""
        
        if len(letter_bag) < 7:
            number_of_letters = len(letter_bag)
        new_letters = randomizer_client.randomize_request(letter_bag, number_of_letters)
        self.letters += new_letters
        print("")
        print("Your letters: ", " ".join(self.letters))

    def swap_letters(self, letter_bag):
        """Swaps all of player's current letters for same number of new letters from letter_bag."""
        
        # Add letters back to letter_bag
        letter_bag += self.letters
        
        num_letters_to_swap = len(self.letters)        
        self.letters = randomizer_client.randomize_request(letter_bag, num_letters_to_swap)
        print("")
        print("Your letters: ", " ".join(self.letters))

    def shuffle_player_letters(self):
        """Shuffles display of player's existing letters. For the purpose of this project, uses randomizer microservice."""
        
        number_of_letters = len(self.letters)
        self.letters = randomizer_client.randomize_request(self.letters, number_of_letters)
        print("")
        print("Your letters: ", " ".join(self.letters))
    
    def word_validation(self, word):
        """Validates player's word submission. Ensures only letters present in player's letters are used. Determines if word
        is present in Merriam Webster API using the dictionary_lookup microservice. Removes used letters from player's letters."""
        
        if dictionary_client.dictionary_lookup(word) == "Invalid word":
            return False
        # Same length
        players_letters = copy.deepcopy(self.letters)
        for letter in word:
            if letter.upper() not in players_letters:
                return False
            
        return True

    def user_word_submission(self, game):
        """Prompts player to submit a word. If word is valid, displays score of word, updates player's total score, 
        removes used letters from letter_bag, updates player's letters."""
        
        score = 0
        word_entry = input("Enter your word submission: ").upper()
        if self.word_validation(word_entry):
            players_letters = copy.deepcopy(self.letters)
            
            for letter in word_entry:
                score += letter_points[letter]
                    # remove used letter from current letter bag
                game.letter_frequency_dict[letter] -= 100
                    # remove letter from player's current letters
                players_letters.remove(letter)

            print("letters after play; ", players_letters)
            game.make_letter_bag()
            self.score += score
            print(f"Your word scored {score} points. Your current total is {self.score} points.")
            self.submitted_words.append([word_entry, self.letters, score])
            self.letters = players_letters
            self.new_letters(game.letter_bag, len(word_entry))
        else:
            if game.game_state == "OFF":
                return
            else:
                print("Invalid word submission. Try again.")
                print("")
    
    def undo(self):
        
        if not self.submitted_words:
            print("No words yet played.")
        else:
            last_played = self.submitted_words[-1]
            last_played_word = last_played[0]
            last_played_letters = last_played[1]
            last_played_score = last_played[2]

            "Remove last played word score from player's score."
            self.score -= last_played_score

            "Display player's last entered word."
            print(f"Undid [{last_played_word}] entry. Your current total is {self.score} points.")
            print("")

            "Restore player's previous letter selection."
            self.letters = last_played_letters
            print(f"Your letters: ", " ".join(self.letters))
    
    def farewell(self):
        """Displays farewell message with player's score. Prompts to send email."""

        print(f"Thanks for playing! Your total score was {self.score}")
        send_email_response = input("Would you like an email containing your submmitted words (yes/no)? ")
        if send_email_response == "yes":
            email_address = input("What is your email address? ")
            subject = "Scrabble Mania - Your submitted words!"
            content = "Words played: "
            for word in self.submitted_words:
                content += f" {word[0]} "
            send_email(email_address, subject, content)
            print("Email sent. Goodbye.")
            print("")
        elif send_email_response == "no":
            print("No email sent. Goodbye.")
            print("") 

        
def introduction():
    """Displays initial instructions to user."""
    
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
    """Displays all commands detailed in commands variable."""
    
    print("COMMANDS:")
    for command in commands:
        print(f"{command}: {commands[command]}")
    print("")

def send_email(email_address, subject, content):
    """Uses email microservice to send an email to the user containing subject and email content."""
    
    req = {"email": email_address, 
           "subject": subject, 
           "content": content
    }
    requests.post("http://127.0.0.1:5000", json=req)


def game_loop(game):
    """Will prompt user for command entry until game is finished."""

    while game.game_state == "ON":
        command_type = input("Enter command: ")
        game.command_controller(command_type)


# Begin game
g1 = Game(letter_frequency_dict, letter_points, commands)
game_timer_thread = threading.Thread(target=g1.game_timer)
g1.start_game()
game_timer_thread.start()

# Run game
g1.game_loop()

# End thread once game complete
game_timer_thread.join()

