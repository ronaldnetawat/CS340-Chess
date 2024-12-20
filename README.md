# Chess Engine for CS 340: Artificial Intelligence class at OWU

A Python-based chess engine implementation featuring player vs. player gameplay and AI opponents using minimax and alpha-beta pruning algorithms.

## Features

- Complete chess rule implementation including:
  - All standard piece movements
  - Special moves (castling, en passant, pawn promotion)
  - Check and checkmate detection
  - Stalemate detection
- Multiple game modes:
  - Player vs Player
  - Player vs AI (Basic Minimax)
  - Player vs Enhanced AI (Alpha-Beta Pruning)
- Console-based chess board visualization
- Piece-position evaluation tables for intelligent AI gameplay
- Advanced board evaluation with multiple heuristics

## Implementation Details

### Chess Pieces
The engine uses an object-oriented approach with a `ChessPiece` parent class and individual classes for each piece type:
- `Pawn`
- `Rook`
- `Knight`
- `Bishop`
- `Queen`
- `King`

Each piece implements its own `valid_moves()` method defining legal movements according to chess rules.

### Board Representation
- 8x8 grid implemented as a 2D array
- Algebraic notation support (e.g., "e2 e4")
- Piece positions tracked with coordinate system (0-7, 0-7)

### AI Implementation

#### Basic Chess Bot
- Uses Minimax algorithm
- Configurable depth for move searching
- Basic position evaluation

#### Improved Chess Bot
- Implements Alpha-Beta Pruning
- Deeper search depth capability
- Enhanced evaluation function including:
  - Piece-square tables
  - Material value
  - Position evaluation
  - Special bonuses/penalties for:
    - Doubled pawns
    - Isolated pawns
    - Bishop pairs
    - Knight positioning

### Evaluation Function
The engine uses sophisticated position evaluation including:
- Base piece values
- Position-dependent scoring using piece-square tables
- Tactical considerations:
  - Pawn structure analysis
  - Bishop pair bonus
  - Knight positioning relative to pawn structure

## Usage

### Starting the Game
```python
if __name__ == "__main__":
    play_chess_with_improved_ai()  # For AI game
    # or
    play_chess()  # For PvP game
```

### Making Moves
Moves are input using algebraic notation:
```
Enter your move (e.g., 'e2 e4'): e2 e4
```

### Game Modes
1. Player vs Player:
```python
play_chess()
```

2. Player vs Basic AI:
```python
play_chess_with_ai()
```

3. Player vs Improved AI:
```python
play_chess_with_improved_ai()
```

## Technical Details

### Move Validation
- Legal move checking for all pieces
- Check detection and prevention
- Move simulation for check prevention
- Special move validation

### Board Evaluation Metrics
- Piece Values:
  - Pawn: 100
  - Knight: 320
  - Bishop: 330
  - Rook: 500
  - Queen: 900
  - King: 20000

### Position Tables
The engine uses piece-square tables for position evaluation, considering:
- Pawn advancement and structure
- Knight centralization
- Bishop diagonal control
- Rook positioning
- Queen mobility
- King safety

## Future Improvements
Potential enhancements could include:
- GUI implementation
- Opening book integration
- Endgame tablebase support
- Move time control
- ELO rating system
- PGN game notation support

## Dependencies
- Python 3.x
- Standard library modules:
  - copy (for board state management)