# 8-Puzzle and Tic-Tac-Toe Game Suite

## Overview

This is a simple Python app that lets you play two classic games: **8-Puzzle** and **Tic-Tac-Toe**. It has an easy-to-use interface made with `customtkinter`. In 8-Puzzle, you move tiles to arrange numbers 1-8 in order, and an AI can solve it for you. In Tic-Tac-Toe, you play against a smart AI. You can choose a game from a menu and switch between light and dark themes.

## Algorithms Used

- *A Algorithm*\* (8-Puzzle): Finds the fastest way to solve the puzzle using a method called Manhattan distance.
- **Minimax Algorithm** (Tic-Tac-Toe): Makes the AI very smart by thinking ahead to pick the best moves.

## Features

- **8-Puzzle**:
  - Move tiles on a 3x3 grid to get numbers 1-8 in order.
  - Play by clicking tiles or let the AI solve it for you.
  - AI tells you how many moves and how much time it took.
  - Creates random puzzles that can always be solved.
- **Tic-Tac-Toe**:
  - Play as "X" against the AI’s "O" on a 3x3 grid.
  - AI is hard to beat because it plans its moves carefully.
  - Shows if you win, lose, or tie at the end.
- **Game Menu**:
  - Choose 8-Puzzle or Tic-Tac-Toe from a clear menu.
  - Switch between light and dark themes easily.
- **Extras**:
  - Start a new game with a "Play Again" button.
  - Go back to the menu with a "Back" button.
  - Get messages when the game ends or the AI finishes.

## Requirements

You need this library to run the app:

```bash
pip install customtkinter
```

## How to Run

1. Make sure Python 3.x is installed on your computer.

2. Install `customtkinter` using the command above.

3. Save the code in a file (e.g., `game_suite.py`).

4. Run the file with:

   ```bash
   python game_suite.py
   ```

5. Pick a game from the menu to start playing.

## Screenshots

Below are screenshots showing how the app looks. Save these images in a `screenshots/` folder in your project directory and make sure the filenames match the ones listed.

### Game Menu

### 8-Puzzle

### Tic-Tac-Toe

*Note*: The following images are included: `game_menu.png`, `8puzzle_solved.png`, `8puzzle_gameover.png`, `tictactoe_win_1.png`, and `tictactoe_win_2.png`. You can add the missing screenshots (`8puzzle_initial.png`, `8puzzle_solving.png`, `tictactoe_initial.png`, `tictactoe_progress.png`) later by saving them in the `screenshots/` folder.

## Project Structure

- `game_suite.py`: The main code with the games and interface.
- `screenshots/`: Folder for your screenshots (create this folder).
- `README.md`: This file, explaining the project.

## Notes

1. 8-Puzzle makes sure every puzzle can be solved.
2. Tic-Tac-Toe AI is very smart and hard to beat.
3. The app looks nice with `customtkinter` and theme options.
4. You can add more games or features easily.

## Future Ideas

- Add an easier mode for Tic-Tac-Toe with a simpler AI.
- Let users watch the 8-Puzzle AI solve step by step.
- Add sounds or animations to make it more fun.
- Save scores or track how many games you play.

## License

This project is open-source under the MIT License.
