
---

# Scrabblemania

Scrabblemania is a console-based word game that allows players to create high-scoring words from random letters, mimicking aspects of the popular game Scrabble. This project was designed to explore the fundamentals of microservice architecture. The application uses three microservices: `dictionary_lookup`, `randomizer`, and `email` to enhance gameplay and functionality.

## Features

- **7-Letter Rack:** Players are provided with 7 random letters from a "letter bag," and the goal is to form the highest-scoring words possible.
- **Microservices:** 
  - **Randomizer Microservice:** Handles random selection of letters.
  - **Dictionary Lookup Microservice:** Verifies the validity of submitted words and fetches their definitions.
  - **Email Microservice:** Sends an email summary of the player's submitted words and score after the game is complete.
- **Letter Scoring:** The game follows a Scrabble-like letter scoring system, with rare letters like 'Q' and 'Z' scoring higher points.
- **Commands:** Players can shuffle, swap, and submit their letters, look up word definitions, undo submissions, and finish the game.
- **Game Timer:** Players can set a custom time limit for the game, and the timer will track the game duration.

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

1. Start the microservices for `dictionary_lookup`, `randomizer`, and `email`.
2. Run the `Scrabblemania` game by executing the main Python file:
   ```bash
   python scrabblemania.py
   ```
3. Follow the on-screen instructions to play the game. Submit words, shuffle letters, and track your score.

## Microservice Details

- **Randomizer Microservice:** Responsible for providing random letters from the letter bag to players.
- **Dictionary Lookup Microservice:** Validates submitted words using an external dictionary API and retrieves word definitions.
- **Email Microservice:** Sends a summary email to players containing their submitted words and final score.

## Example Gameplay

```text
Welcome to ScrabbleMania!
Use this application to practice your word-finding skills!

Your letters: A B C D E F G
Enter your word submission: BADGE
Your word scored 7 points. Your current total is 7 points.
...
Time is up! Press [ENTER] to view your score.
Thanks for playing! Your total score was 42 points.
```

## Contribution

If you'd like to contribute to Scrabblemania, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

## Author

- **Robert Thom** - [GitHub](https://github.com/rthom9)

---

