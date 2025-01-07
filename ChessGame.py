class Piece:
    """Base class for all chess pieces."""

    def __init__(self, color):
        self.color = color  # 'white' or 'black'

    def valid_moves(self, position, board):
        """Override in child classes to define specific move logic."""
        return []


class Pawn(Piece):
    def valid_moves(self, position, board):
        """Define valid moves for a Pawn."""
        x, y = position
        moves = []
        direction = -1 if self.color == 'white' else 1  # White moves up, black moves down

        # Basic forward move
        if 0 <= x + direction < 8 and board[x + direction][y] is None:
            moves.append((x + direction, y))

        # Capture diagonally
        for dx in [-1, 1]:
            if 0 <= x + direction < 8 and 0 <= y + dx < 8:
                target = board[x + direction][y + dx]
                if target and target.color != self.color:
                    moves.append((x + direction, y + dx))

        return moves


class Rook(Piece):
    def valid_moves(self, position, board):
        """Define valid moves for a Rook."""
        x, y = position
        moves = []

        # Horizontal and vertical moves
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x, y
            while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                nx, ny = nx + dx, ny + dy
                if board[nx][ny] is None:
                    moves.append((nx, ny))
                elif board[nx][ny].color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break

        return moves


class Knight(Piece):
    def valid_moves(self, position, board):
        """Define valid moves for a Knight."""
        x, y = position
        moves = []

        # L-shaped moves
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and (board[nx][ny] is None or board[nx][ny].color != self.color):
                moves.append((nx, ny))

        return moves


class Bishop(Piece):
    def valid_moves(self, position, board):
        """Define valid moves for a Bishop."""
        x, y = position
        moves = []

        # Diagonal moves
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x, y
            while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                nx, ny = nx + dx, ny + dy
                if board[nx][ny] is None:
                    moves.append((nx, ny))
                elif board[nx][ny].color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break

        return moves


class Queen(Piece):
    def valid_moves(self, position, board):
        """Define valid moves for a Queen."""
        # Combines Rook and Bishop moves
        return Rook.valid_moves(self, position, board) + Bishop.valid_moves(self, position, board)


class King(Piece):
    def valid_moves(self, position, board):
        """Define valid moves for a King."""
        x, y = position
        moves = []

        # One square in any direction
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and (board[nx][ny] is None or board[nx][ny].color != self.color):
                moves.append((nx, ny))

        return moves


class Board:
    """Class to represent the chessboard."""

    def __init__(self):
        self.grid = self.initialize_board()

    def initialize_board(self):
        """Set up the chessboard with pieces in their starting positions."""
        board = [[None for _ in range(8)] for _ in range(8)]

        # Add pawns
        for col in range(8):
            board[1][col] = Pawn('white')
            board[6][col] = Pawn('black')

        # Add Rooks (example)
        board[0][0] = Rook('white')
        board[0][7] = Rook('white')
        board[7][0] = Rook('black')
        board[7][7] = Rook('black')

        # Add other pieces as needed...

        return board

    def display(self):
        """Print the current state of the board."""
        for row in self.grid:
            print(" ".join([piece.__class__.__name__[0] if piece else '.' for piece in row]))
        print()


from board import Board


def game_loop():
    """Main game loop."""
    board = Board()
    board.display()

    while True:
        # Alternate between white and black players
        for player in ['white', 'black']:
            print(f"{player}'s turn")
            move = input("Enter your move (e.g., e2 to e4): ")
            print(f"Processing move: {move}")
            board.display()  # Placeholder for move execution


if __name__ == "__main__":
    game_loop()