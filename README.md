
# Connect 4 Game - Player vs AI

A Python implementation of the classic Connect 4 game featuring a human player versus an AI opponent using the minimax algorithm with alpha-beta pruning.

## Features

- Interactive GUI using Pygame
- AI opponent with configurable difficulty
- Visual feedback with hover effects
- Automatic game end detection
- Clean, colorful interface

## Requirements

- Python 3.7+
- numpy
- pygame

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MathumithaE/connect4-ai-pygame.git
cd connect4-ai-pygame
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python connect4_game.py
```

2. **Player Turn (Red pieces)**: Click on any column to drop your piece
3. **AI Turn (Yellow pieces)**: The AI will automatically make its move
4. **Objective**: Get 4 pieces in a row (horizontally, vertically, or diagonally) to win!

## Game Rules

- Players take turns dropping colored pieces into a 7-column, 6-row grid
- Pieces fall to the lowest available space within the column
- The first player to form a horizontal, vertical, or diagonal line of 4 pieces wins
- If the board fills up with no winner, the game is a draw

## AI Algorithm

The AI uses the **minimax algorithm** with **alpha-beta pruning**:
- **Search Depth**: 5 levels
- **Evaluation Function**: Considers piece positioning, potential wins, and blocking strategies
- **Optimization**: Alpha-beta pruning reduces search time significantly

## Technical Details

- **Language**: Python 
- **Graphics**: Pygame
- **AI Algorithm**: Minimax with Alpha-Beta Pruning
- **Board Representation**: NumPy array (6x7)

## Customization

You can modify these constants in the code:
- `ROWS, COLS`: Change board size
- `SQUARESIZE`: Adjust visual scale
- Minimax depth (line with `minimax(board, 5, ...)`)
- Colors and styling

## Controls

- **Mouse Movement**: Preview piece placement
- **Left Click**: Drop piece in column
- **Close Window**: Exit game

## Screenshots

The game features:
- Blue board with black holes
- Red pieces for the player
- Yellow pieces for the AI
- Visual hover effects
- Win/draw notifications



