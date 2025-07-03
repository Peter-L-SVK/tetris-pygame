# Tetris Game with Pygame

A classic Tetris implementation built with Python and Pygame, featuring modern enhancements like high score tracking and multiple game screens.

## Features

- 🎮 Classic Tetris gameplay with all 7 tetromino pieces
- 🏆 Persistent high score tracking (top 10 scores)
- 📛 Player name entry for high scores
- 📊 Dedicated high score viewing screen
- 🎨 Clean, responsive interface
- ⚙️ Modular code structure for easy maintenance

## Requirements

- Python 3.6+
- Pygame 2.0+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pygame-tetris.git
   cd pygame-tetris
   ```

2. Install dependencies:
   ```bash
   pip install pygame
   ```

## How to Play

### Controls
- **Left/Right Arrow**: Move piece horizontally
- **Up Arrow**: Rotate piece
- **Down Arrow**: Accelerate piece downward
- **ESC**: Return to previous screen (from high scores)

### Game Screens
1. **Main Menu**:  
   '1.' - Play Game  
   '2.' - View High Scores  
   '3.' - Quit  

2. **Game Screen**:
   - Current score display
   - Next piece preview
   - Standard Tetris gameplay

3. **Game Over Screen**:
   - Enter your name for high scores
   - Options to play again, view scores, or quit

4. **High Scores Screen**:
   - Displays top 10 scores
   - Press ESC to return

## File Structure

```
tetris/
├── tetris.py         # Main game logic
├── tetromino.py      # Tetromino class definition
├── lib.py            # Helper functions and screens
└── highscores.json   # Auto-generated high score storage
```

## Running the Game

Execute the main script:
```bash
python tetris.py
```

## Customization

You can modify these game constants in `tetris.py`:
- `BLOCK_SIZE`: Change the size of blocks
- `GRID_WIDTH/HEIGHT`: Adjust playing field dimensions
- `fall_speed`: Change the initial falling speed

## Troubleshooting

If you encounter issues:
1. Ensure you have the latest version of Pygame:
   ```bash
   pip install --upgrade pygame
   ```
2. Verify Python version (3.6+ required)
3. Delete `highscores.json` if you experience score-related issues

## Contributing

Contributions are welcome! Please open an issue or pull request for any:
- Bug fixes
- New features
- Code improvements
- Documentation updates

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
