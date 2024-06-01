import client
import requests
import threading
import time
import tkinter
from tkinter import messagebox
from userUI import set_timer, start_timer


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
    "finished": "End your session.",
    "restart": "End current session and restart.",
    "commands": "See this list again."
}

game_time_limit = "000100"


def game_timer(player):
    root = tkinter.Tk()
    root.withdraw()
    t1 = "000003"
    t2 = "000005"
    t3 = "000000"
    set_timer(t1, t2, t3)
    start_timer()
    while True:
        with open('alerts.txt', 'r+', encoding='utf-8') as alerts_file:
            alert = alerts_file.read()
            if alert == t2:
                messagebox.showinfo("Alert", f"You have {t2} seconds remaining.")
                time.sleep(1.1)
            if alert == t3:
                messagebox.showinfo("Alert", f"You have {t3} seconds remaining.")
                alerts_file.write("")
                time.sleep(1)
            if alert == "0s":
                break
        #time.sleep(1)
    print("\nTime is up!")
    root.wm_attributes("-topmost", 1)
    messagebox.showinfo(title="Alert", message="You are out of time. Game has ended.", parent=root)
    finished(player)



class Game:
    def __init__(self, letter_frequency_dict, letter_points):
        self.letter_frequency_dict = letter_frequency_dict
        self.letter_points = letter_points
        self.letter_bag = []
        self.game_time = None
        self.reminder_time_1 = "000100"
        self.reminder_time_2 = None

    def start_game(self, player):
        self.make_letter_bag()
        player.new_letters(self.letter_bag)

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
            self.user_word_submission(game)
        else:
            for letter in word_entry:
                letter = letter.upper()
                score += letter_points[letter]
                # remove used letter from current letter bag
                game.letter_frequency_dict[letter] -= 1
            game.make_letter_bag()
            self.score += score
            print(f"Your word scored {score} points. Your current total is {self.score} points.")

            # Stop timer thread
            # game_timer_thread.join()

            # Display new letters to user
            self.new_letters(game.letter_bag)
            

def introduction():
    print("")
    print("Welcome to ScrabbleMania!")
    print("Use this application to practice your word finding skills!")
    print("")
    print("You will be given a set of 7 letters from the letter bag. Enter your best word. \nOnce the bag is near "
          "empty, you will be given only the remaining letters.")
    print("Enter the commands listed below to navigate this game.")
    command_display(commands)

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


def game_loop():
    while True:
        command_type = input("Enter command: ")
        command_controller(command_type, g1, p1)


#Start Game
introduction()
#game_time_limit = input("Set a time limit for your game. Please use HHMMSS format. You will be notified when 60s remaining: ")

g1 = Game(letter_frequency_dict, letter_points)
p1 = Player()

input("Set a time limit for your game. Please use HHMMSS format. You will be notified when 60s remaining: ")
game_timer_thread = threading.Thread(target=game_timer, args=([p1]))
game_loop_thread = threading.Thread(target=game_loop)

g1.start_game(p1)
game_timer_thread.start()
game_loop()
#game_loop_thread.start()




