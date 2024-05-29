import client
import json
import requests

letter_bag = []

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

def introduction():
    print("Welcome to ScrabbleMania!")
    print()
    print("Use this application to practice your word finding skills!")

def make_letter_bag(letter_dict = letter_frequency_dict):
    letter_bag = []
    for letter in letter_dict:
        frequency = letter_dict[letter]
        while frequency > 0:
            letter_bag.append(letter)
            frequency -= 1
    return letter_bag

def get_letters(letter_bag, number_of_letters):
    """Returns random letters from letter bag"""
    letters = client.randomize_request(letter_bag, number_of_letters)
    return letters

def shuffle_letters(letters):
    number_of_letters = len(letters)
    letters = client.randomize_request(letters, number_of_letters)
    return letters

def word_score(word):
    score = 0
    for letter in word:
        score += letter_points[letter.upper()]
    return score

def send_email(email_address, subject, content):
    req = {"email": email_address, 
           "subject": subject, 
           "content": content
    }
    requests.post("http://127.0.0.1:5000", json=req)

letterBag = make_letter_bag()
print(client.randomize_request(letterBag, 3))
print(get_letters(letterBag, 18))
print(shuffle_letters(["a","b","c","d"]))
print(word_score("HELlO"))
send_email("thomrobert9@gmail.com", "Yoyoboy!", "It's your time shawty")

