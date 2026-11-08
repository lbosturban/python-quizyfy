# Quizify

Quizify is a command-line trivia game written in Python. Players answer multiple-choice and true/false questions, adjust quiz settings, and save their scores. Questions can be downloaded from the Open Trivia Database (OpenTDB).

## Features

- Play multiple-choice and true/false quizzes.
- Choose a question category, difficulty, question type, and number of questions.
- View high-score leaderboards overall and by category.
- View the Hall of Fame, with saved users and their scores grouped by category.
- Save user scores in a JSON file and export leaderboard results to a CSV file.

## Technologies Used

- Python 3.10 or later
- `requests` for communicating with the OpenTDB API
- JSON for quiz settings, questions, and saved user scores
- CSV for exported leaderboard data

## Project Initialization

1. Install Python 3.10 or later.
2. Clone or download this project.
3. Open a terminal in the project’s root directory.
4. Install the required dependency:

```bash
python3 -m pip install requests
```

## Project Data

The project uses files in the `data/` directory:

 - `opentdb.json` stores the quiz configuration (mimics openTriviaDB API request).
 - `questions.json` stores the questions used by the game (downloaded from openTriviaDB).
 - `utilisateurs.json` stores player names and their scores (no anonymous).
 - `scoreboard.csv` backups the leaderboard results when seen.
 - `categories.json` contains openTriviaDB category data (updated as needed).

Make sure the `data/` directory exists and that the JSON files contain valid JSON. The game needs an internet connection when downloading questions from OpenTDB.
## Launching the Project

From the project’s root directory, run:
```bash
python3 main.py
```

Follow the on-screen menu to play, view high scores or the Hall of Fame, configure a quiz, or quit, CTRL-D interrupts the game at any input.

Scores are saved for named players. Leaving the name blank starts the game as anonymous, whose scores are not saved.

## Project Author

Laurent BOST URBAN
