
---

# Scrabblemania

Scrabblemania is a console-based word game that allows players to create high-scoring words from random letters, mimicking aspects of the popular game Scrabble. This project was designed to explore the fundamentals of microservice architecture. The application uses three microservices: `dictionary_lookup`, `randomizer`, and `email` to enhance gameplay and functionality.

## Features

- **7-Letter Player Rack:** Players are provided with 7 random letters from a "letter bag," and the goal is to form the highest-scoring words possible.
- **Microservices:** 
  - **Randomizer Microservice:** Handles random selection of letters. Service is also utilized for shuffling of letters.
  - **Dictionary Lookup Microservice:** Accesses the Merriam-Webster Dictionary API to verify the validity of submitted words and fetch definitions.
  - **Email Microservice:** Sends an email summary of the player's submitted words and score after the game is complete.
- **Letter Scoring:** The game follows a Scrabble-like letter scoring system, with rare letters like 'Q' and 'Z' scoring higher points. The player's current score is displayed following each valid word submission.
- **Commands:** Players can submit words, shuffle letters, swap letters, look up played word definitions, undo submissions, and finish the game early.
- **Game Timer:** Players can set a custom time limit for the game, and the timer will track the game duration. This application uses threading to enable concurrent execution and game and timer processes.

## Commands

- **play:** Ready to submit a word.
- **shuffle:** Shuffle your current letters.
- **swap:** Swap all of your current letters with new ones from the letter bag.
- **definition:** Look up the definition of the last submitted word.
- **finished:** End the game session.
- **undo:** Undo the most recent word submission.
- **commands:** Display a list of available commands.

## Installation

1. Clone the repository to your local machine.
2. For the purposes of this project, microservice server code for the `dictionary` and `randomizer` services is found within their respectively titled folders.

## Usage

1. For ease of use, the starting of microservice servers and the main game script has been automated using the `start_all.py` script.
2. Within the `start_all.py` script, **update `path` to that of which you cloned repository.** 
2. Run the `Scrabblemania` game by executing the start_all.py file. Note that there is a 3-second delay to ensure servers for dictionary and randomizer miroservices have started prior to running the `main.py` game script:
   ```bash
   python start_all.py
   ```
3. Follow the on-screen instructions to play the game.
4. At the completion of your game, you are provided with the option to have all submitted words emailed to a provided email address.

## Microservice Details

- **Randomizer Microservice:** Responsible for providing random letters from the letter bag to players.
- **Dictionary Lookup Microservice:** Validates submitted words using an external dictionary API and retrieves word definitions.
- **Email Microservice:** Sends a summary email to players containing their submitted words and final score.

## Example Gameplay

```text
Welcome to ScrabbleMania!
Use this application to practice your word finding skills!

You will be given a set of 7 letters from the letter bag. Enter your best word.
Once the bag is near empty, you will be given only the remaining letters.
Enter the commands listed below to navigate this game.

COMMANDS:
play: Ready to submit a word.
shuffle: Shuffle your current letters.
swap: Swap all of your current letters.
definition: Lookup definition of last submitted word.
finished: End your session.
undo: Undo most recent word submission.
commands: See this list again.


Set a time limit for your game. Please use HHMMSS format: 001000

Your letters:  A V R R Z N E
Enter command: play
Enter your word submission: zen
Your word scored 12 points. Your current total is 12 points.

Your letters:  A V R R A O U
Enter command: definition

Definition(1): ['a Japanese sect of Mahayana Buddhism that aims at enlightenment by direct intuition through meditation', "a state of calm attentiveness in which one's actions are guided by intuition rather than by conscious effort"]

Definition(2): ['of, relating to, or associated with Zen Buddhism', 'suggestive of the teachings or practice of Zen Buddhism', 'having or showing qualities (such as meditative calmness and an attitude of acceptance) popularly associated with practitioners of Zen Buddhism']

Your letters:  A V R R A O U
Enter command: undo
Undid [ZEN] entry. Your current total is 0 points.

Your letters:  A V R R Z N E
Enter command: swap

Your letters:  O U L I C G A
Enter command: shuffle

Your letters:  U G I O A L C
Enter command:
...
...
Thanks for playing! Your total score was 36.
Would you like an email containing your submmitted words (yes/no)? yes
What is your email address? email_address@gmail.com
Email Sent. Goodbye!
```

## License

This project is licensed under the MIT License.

## Author

- **Robert Thom** - [GitHub](https://github.com/rthom9)

---

