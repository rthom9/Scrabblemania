import client
import json
import requests
from userUI import set_timer, start_timer, pause_timer, cancel_timer


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
    
    def new_letters(self, letter_bag, number_of_letters):
        self.letters = client.randomize_request(letter_bag, number_of_letters)

    def shuffle_player_letters(self):
        number_of_letters = len(self.letters)
        self.letters = client.randomize_request(self.letters, number_of_letters)
    
    def user_word_submission(self):
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
                score += letter_points[letter.upper()]
            print(f"Your word scored {score} points")
            self.score += score

def introduction():
    print("Welcome to ScrabbleMania!")
    print("Use this application to practice your word finding skills!")


def send_email(email_address, subject, content):
    req = {"email": email_address, 
           "subject": subject, 
           "content": content
    }
    requests.post("http://127.0.0.1:5000", json=req)

g1 = Game(letter_frequency_dict, letter_points)
g1.make_letter_bag()
p1 = Player()


p1.new_letters(g1.letter_bag, 7)
print(p1.letters)
p1.shuffle_player_letters()
print(p1.letters)
p1.user_word_submission()
p1.user_word_submission()
print(p1.score)






# send_email("thomrobert9@gmail.com", "Yoyoboy!", "It's your time shawty")
# set_timer("000006","000005","000002")
# start_timer()
# print(user_current_letters)


