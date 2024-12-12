import copy

# piece-wise board points
PAWN_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

class ChessPiece: # parent class for chess pieces
    def __init__(self, color):
        self.color = color
        self.has_moved = False # used for castling/pawns' initial moves etc.

# all the child piece classes of the ChessPiece parent class
class Pawn(ChessPiece):
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'

    def valid_moves(self, board, row, col):
        moves = []
        direction = 1 if self.color == 'white' else -1
        
        #forward move
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            
            # initial two-step move
            if (self.color == 'white' and row == 1) or (self.color == 'black' and row == 6):
                if board[row + 2*direction][col] is None:
                    moves.append((row + 2*direction, col))
        
        # capturing pieces diagonally
        for c in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + c < 8:
                if board[row + direction][col + c] and board[row + direction][col + c].color != self.color:
                    moves.append((row + direction, col + c))
        
        return moves

class Rook(ChessPiece):
    def __str__(self):
        return 'R' if self.color == 'white' else 'r'

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        # add sqaures to the list of moves until a piece is encountered or board ends
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + i*dr, col + i*dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        
        return moves

class Knight(ChessPiece):
    def __str__(self):
        return 'N' if self.color == 'white' else 'n'

    # 2 squares in 1 direction and 1 square perpendicularly
    def valid_moves(self, board, row, col):
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        
        return moves

class Bishop(ChessPiece):
    def __str__(self):
        return 'B' if self.color == 'white' else 'b'

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + i*dr, col + i*dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        
        return moves

class Queen(ChessPiece):
    def __str__(self):
        return 'Q' if self.color == 'white' else 'q'

    def valid_moves(self, board, row, col):
        moves = []
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + i*dr, col + i*dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        
        return moves

class King(ChessPiece):
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'

    def valid_moves(self, board, row, col):
        moves = []
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        
        return moves

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)] #initialize the board
        self.initialize_board()
        self.en_passant_target = None

    def initialize_board(self):
        # Set up  the pawns
        for col in range(8):
            self.board[1][col] = Pawn('white')
            self.board[6][col] = Pawn('black')

        # set the other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.board[0][col] = piece_order[col]('white')
            self.board[7][col] = piece_order[col]('black')

    def print_board(self):
        print("  a b c d e f g h")
        for row in range(7, -1, -1):
            print(f"{row + 1}", end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(str(piece), end=" ")
                else:
                    print(".", end=" ")
            print(f"{row + 1}")
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        piece = self.board[start_row][start_col]
        if piece is None:
            return False

        if (end_row, end_col) not in piece.valid_moves(self.board, start_row, start_col):
            return False

        # Check if the move puts the player in check
        temp_board = copy.deepcopy(self.board)
        temp_board[end_row][end_col] = piece
        temp_board[start_row][start_col] = None
        if self.is_in_check(piece.color, temp_board):
            return False

        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        piece.has_moved = True

        # pawn promotion at the last rank
        if isinstance(piece, Pawn) and (end_row == 0 or end_row == 7):
            self.board[end_row][end_col] = Queen(piece.color)

        #en passant
        if isinstance(piece, Pawn) and abs(start_row - end_row) == 2:
            self.en_passant_target = ((start_row + end_row) // 2, start_col)
        elif self.en_passant_target:
            if isinstance(piece, Pawn) and end == self.en_passant_target:
                self.board[start_row][end_col] = None  # Remove the captured pawn
        else:
            self.en_passant_target = None

        # castling
        if isinstance(piece, King) and abs(start_col - end_col) == 2:
            if end_col > start_col:  # Kingside
                rook = self.board[start_row][7]
                self.board[start_row][5] = rook
                self.board[start_row][7] = None
                rook.has_moved = True
            else:  # Queenside
                rook = self.board[start_row][0]
                self.board[start_row][3] = rook
                self.board[start_row][0] = None
                rook.has_moved = True

        return True

    def is_in_check(self, color, board=None):
        if board is None:
            board = self.board

        # get king's position king
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        # Check if any opponent's piece can attack the king
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == opponent_color:
                    if king_position in piece.valid_moves(board, row, col):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        # check valid moves for the king to get out of the chekc
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.valid_moves(self.board, row, col):
                        temp_board = copy.deepcopy(self.board)
                        temp_board[move[0]][move[1]] = piece
                        temp_board[row][col] = None
                        if not self.is_in_check(color, temp_board):
                            return False
        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False

        # Check if any legal move is available
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.valid_moves(self.board, row, col):
                        temp_board = copy.deepcopy(self.board)
                        temp_board[move[0]][move[1]] = piece
                        temp_board[row][col] = None
                        if not self.is_in_check(color, temp_board):
                            return False
        return True

    def get_all_pieces(self, color):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append((piece, (row,col)))
        return pieces


# Evaluation Function
def evaluate_board(board):
    score = 0
    piece_values = {
        'P': 100,   # Increased base values to make position scoring more meaningful
        'N': 320,
        'B': 330,
        'R': 500,
        'Q': 900,
        'K': 20000
    }
    
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                # Base piece value
                value = piece_values[str(piece).upper()]
                
                # Position value
                position_value = 0
                if isinstance(piece, Pawn):
                    position_value = PAWN_TABLE[row][col]
                elif isinstance(piece, Knight):
                    position_value = KNIGHT_TABLE[row][col]
                elif isinstance(piece, Bishop):
                    position_value = BISHOP_TABLE[row][col]
                elif isinstance(piece, Rook):
                    position_value = ROOK_TABLE[row][col]
                elif isinstance(piece, Queen):
                    position_value = QUEEN_TABLE[row][col]
                elif isinstance(piece, King):
                    position_value = KING_TABLE[row][col]
                
                # Flip table for black pieces
                if piece.color == 'black':
                    position_value = -position_value
                    row_display = 7 - row
                else:
                    row_display = row
                
                total_value = value + position_value
                
                if piece.color == 'white':
                    score += total_value
                else:
                    score -= total_value
                
                # Additional positional bonuses/penalties
                if isinstance(piece, Pawn):
                    # Doubled pawns penalty
                    for i in range(8):
                        if i != row and board.board[i][col] and isinstance(board.board[i][col], Pawn) and board.board[i][col].color == piece.color:
                            if piece.color == 'white':
                                score -= 50
                            else:
                                score += 50
                    
                    # Isolated pawns penalty
                    isolated = True
                    for adjacent_col in [col-1, col+1]:
                        if 0 <= adjacent_col < 8:
                            for r in range(8):
                                if board.board[r][adjacent_col] and isinstance(board.board[r][adjacent_col], Pawn) and board.board[r][adjacent_col].color == piece.color:
                                    isolated = False
                    if isolated:
                        if piece.color == 'white':
                            score -= 30
                        else:
                            score += 30
                
                elif isinstance(piece, Bishop):
                    # Bishop pair bonus
                    bishop_count = 0
                    for r in range(8):
                        for c in range(8):
                            if board.board[r][c] and isinstance(board.board[r][c], Bishop) and board.board[r][c].color == piece.color:
                                bishop_count += 1
                    if bishop_count >= 2:
                        if piece.color == 'white':
                            score += 50
                        else:
                            score -= 50
                
                elif isinstance(piece, Knight):
                    # Knights are better with more pawns on the board
                    pawn_count = sum(1 for r in range(8) for c in range(8) 
                                   if board.board[r][c] and isinstance(board.board[r][c], Pawn))
                    if piece.color == 'white':
                        score += pawn_count * 2
                    else:
                        score -= pawn_count * 2
    
    return score


# writing the minimax function
def minimax(board, depth, maximizing_player):
    if depth == 0:
        return evaluate_board(board.board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for piece, (row, col) in board.get_all_pieces('white'):
            for move in piece.valid_moves(board.board, row, col):
                new_board = copy.deepcopy(board)
                if new_board.move_piece((row, col), move):
                    evaluation = minimax(new_board, depth - 1, False)
                    max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = float('inf')
        for piece, (row, col) in board.get_all_pieces('black'):
            for move in piece.valid_moves(board.board, row, col):
                new_board = copy.deepcopy(board)
                if new_board.move_piece((row, col), move):
                    evaluation = minimax(new_board, depth - 1, True)
                    min_eval = min(min_eval, evaluation)
        return min_eval
    

def alphabeta(board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for piece, (row, col) in board.get_all_pieces('white'):
            for move in piece.valid_moves(board.board, row, col):
                new_board = copy.deepcopy(board)
                if new_board.move_piece((row, col), move):
                    evaluation = alphabeta(new_board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, evaluation)
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for piece, (row, col) in board.get_all_pieces('black'):
            for move in piece.valid_moves(board.board, row, col):
                new_board = copy.deepcopy(board)
                if new_board.move_piece((row, col), move):
                    evaluation = alphabeta(new_board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, evaluation)
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return min_eval


# the chess bot class
class ChessBot:
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth
    
    def choose_move(self, board):
        best_move = None
        best_score = float('-inf') if self.color == 'white' else float('inf')
        
        for piece, (row, col) in board.get_all_pieces(self.color):
            for move in piece.valid_moves(board.board, row, col):
                new_board = copy.deepcopy(board)
                if new_board.move_piece((row, col), move):
                    score = minimax(new_board, self.depth - 1, self.color == 'black')
                    if (self.color == 'white' and score > best_score) or (self.color == 'black' and score < best_score):
                        best_score = score
                        best_move = ((row, col), move)
        return best_move


class ImprovedChessBot:
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth
    
    def choose_move(self, board):
        best_move = None
        best_score = float('-inf') if self.color == 'white' else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for piece, (row, col) in board.get_all_pieces(self.color):
            for move in piece.valid_moves(board.board, row, col):
                new_board = copy.deepcopy(board)
                if new_board.move_piece((row, col), move):
                    score = alphabeta(new_board, self.depth - 1, alpha, beta, self.color == 'black')
                    
                    if self.color == 'white':
                        if score > best_score:
                            best_score = score
                            best_move = ((row, col), move)
                        alpha = max(alpha, score)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = ((row, col), move)
                        beta = min(beta, score)
                    
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
                
        return best_move


# P v P game loop
def play_chess():
    board = ChessBoard()
    current_player = 'white'

    while True:
        board.print_board()
        print(f"{current_player.capitalize()}'s turn")
        
        if board.is_in_check(current_player):
            print(f"{current_player.capitalize()} is in check!")
            if board.is_checkmate(current_player):
                print(f"Checkmate! {current_player.capitalize()} loses.")
                break
        elif board.is_stalemate(current_player):
            print("Stalemate! The game is a draw.")
            break

        move = input("Enter your move (e.g., 'e2 e4'): ")
        start, end = move.split()
        start = (int(start[1]) - 1, ord(start[0]) - ord('a'))
        end = (int(end[1]) - 1, ord(end[0]) - ord('a'))

        if board.move_piece(start, end):
            current_player = 'black' if current_player == 'white' else 'white'
        else:
            print("Invalid move. Try again.")


# chess bot game loop
def play_chess_with_ai():
    board = ChessBoard()
    bot_player = ChessBot('black', depth=3)
    current_player = 'white'

    while True:
        board.print_board()
        print(f"{current_player.capitalize()}'s turn")
        
        if board.is_in_check(current_player):
            print(f"{current_player.capitalize()} is in check!")
            if board.is_checkmate(current_player):
                print(f"Checkmate! {current_player.capitalize()} loses.")
                break
        elif board.is_stalemate(current_player):
            print("Stalemate! The game is a draw.")
            break

        if current_player == 'white':
            move = input("Enter your move (e.g., 'e2 e4'): ")
            start, end = move.split()
            start = (int(start[1]) - 1, ord(start[0]) - ord('a'))
            end = (int(end[1]) - 1, ord(end[0]) - ord('a'))
        else:
            start, end = bot_player.choose_move(board)
            print(f"Bot's move: {chr(start[1] + ord('a'))}{start[0] + 1} {chr(end[1] + ord('a'))}{end[0] + 1}")

        if board.move_piece(start, end):
            current_player = 'black' if current_player == 'white' else 'white'
        else:
            print("Invalid move. Try again.")

def play_chess_with_improved_ai():
    board = ChessBoard()
    bot_player = ImprovedChessBot('black', depth=4)  # Increased depth due to better pruning
    current_player = 'white'

    while True:
        board.print_board()
        print(f"{current_player.capitalize()}'s turn")
        
        if board.is_in_check(current_player):
            print(f"{current_player.capitalize()} is in check!")
            if board.is_checkmate(current_player):
                print(f"Checkmate! {current_player.capitalize()} loses.")
                break
        elif board.is_stalemate(current_player):
            print("Stalemate! The game is a draw.")
            break

        if current_player == 'white':
            move = input("Enter your move (e.g., 'e2 e4'): ")
            start, end = move.split()
            start = (int(start[1]) - 1, ord(start[0]) - ord('a'))
            end = (int(end[1]) - 1, ord(end[0]) - ord('a'))
        else:
            print("Bot is thinking...")
            start, end = bot_player.choose_move(board)
            print(f"Bot's move: {chr(start[1] + ord('a'))}{start[0] + 1} {chr(end[1] + ord('a'))}{end[0] + 1}")

        if board.move_piece(start, end):
            current_player = 'black' if current_player == 'white' else 'white'
        else:
            print("Invalid move. Try again.")


if __name__ == "__main__":
    play_chess_with_improved_ai()
