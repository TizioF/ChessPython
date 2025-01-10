import pygame

pygame.init() #initialize the package

WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT]) #setting up game display
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()
fps=60



#load images in game
DEFAULT_IMAGE_SIZE=(80,80)
black_pawn= pygame.image.load('images/black pawn.png')
black_pawn=pygame.transform.scale(black_pawn,DEFAULT_IMAGE_SIZE) #load and scale piece image
black_rook= pygame.image.load('images/black rook.png')
black_rook=pygame.transform.scale(black_rook,DEFAULT_IMAGE_SIZE)
black_bishop= pygame.image.load('images/black bishop.png')
black_bishop=pygame.transform.scale(black_bishop,DEFAULT_IMAGE_SIZE)
black_knight= pygame.image.load('images/black knight.png')
black_knight=pygame.transform.scale(black_knight,DEFAULT_IMAGE_SIZE)
black_queen= pygame.image.load('images/black queen.png')
black_queen=pygame.transform.scale(black_queen,DEFAULT_IMAGE_SIZE)
black_king= pygame.image.load('images/black king.png')
black_king=pygame.transform.scale(black_king,DEFAULT_IMAGE_SIZE)
white_pawn=pygame.image.load('images/white pawn.png')
white_pawn=pygame.transform.scale(white_pawn, DEFAULT_IMAGE_SIZE)
white_rook=pygame.image.load('images/white rook.png')
white_rook=pygame.transform.scale(white_rook, DEFAULT_IMAGE_SIZE)
white_bishop=pygame.image.load('images/white bishop.png')
white_bishop=pygame.transform.scale(white_bishop, DEFAULT_IMAGE_SIZE)
white_knight=pygame.image.load('images/white knight.png')
white_knight=pygame.transform.scale(white_knight, DEFAULT_IMAGE_SIZE)
white_queen=pygame.image.load('images/white queen.png')
white_queen=pygame.transform.scale(white_queen, DEFAULT_IMAGE_SIZE)
white_king=pygame.image.load('images/white king.png')
white_king=pygame.transform.scale(white_king, DEFAULT_IMAGE_SIZE)

w_images=[white_pawn,white_queen,white_king,white_knight,white_rook,white_bishop]
b_images=[black_pawn,black_queen,black_king,black_knight,black_rook,black_bishop]
piece_list=['Pawn','Queen','King','Knight','Rook','Bishop'] #list to know the index of the piece



# Check if a King is in Check
def is_in_check(king_pos, color, board):
    # Simplified version: check if any opponent piece can attack the king's position
    opponent_color = 'white' if color == 'black' else 'black'
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == opponent_color:
                if (row, col) in piece.valid_moves(king_pos, board):
                    return True
    return False


# Checkmate condition
def is_checkmate(color, board):
    king_pos = None
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if isinstance(piece, King) and piece.color == color:
                king_pos = (row, col)
                break

    if not king_pos:
        return False  # No king found for some reason, shouldn't happen

    if is_in_check(king_pos, color, board):
        # Check if there are any valid moves to escape the check
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == color:
                    for move in piece.valid_moves((row, col), board):
                        temp_board = [row[:] for row in board]
                        temp_board[move[0]][move[1]] = piece
                        temp_board[row][col] = None
                        if not is_in_check(move, color, temp_board):
                            return False  # There is a move that can escape check
        return True  # No escape moves found, it's checkmate
    return False  # It's not checkmate if the king isn't in check



class Piece:
    """Base class for all chess pieces."""

    def __init__(self,types ,color, position):
        self.type = types
        self.color = color
        self.position = position

    def valid_moves(self, selected_pos, board):
        pass


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

#game variables
white_pieces = [
    Piece('Rook', 'white', (0, 0)), Piece('Knight', 'white', (1, 0)), Piece('Bishop', 'white', (2, 0)),
    Piece('Queen', 'white', (3, 0)), Piece('King', 'white', (4, 0)), Piece('Bishop', 'white', (5, 0)),
    Piece('Knight', 'white', (6, 0)), Piece('Rook', 'white', (7, 0)),
    Piece('Pawn', 'white', (0, 1)), Piece('Pawn', 'white', (1, 1)), Piece('Pawn', 'white', (2, 1)),
    Piece('Pawn', 'white', (3, 1)), Piece('Pawn', 'white', (4, 1)), Piece('Pawn', 'white', (5, 1)),
    Piece('Pawn', 'white', (6, 1)), Piece('Pawn', 'white', (7, 1)),
]

# Initialize black pieces
black_pieces = [
    Piece('Rook', 'black', (0, 7)), Piece('Knight', 'black', (1, 7)), Piece('Bishop', 'black', (2, 7)),
    Piece('Queen', 'black', (3, 7)), Piece('King', 'black', (4, 7)), Piece('Bishop', 'black', (5, 7)),
    Piece('Knight', 'black', (6, 7)), Piece('Rook', 'black', (7, 7)),
    Piece('Pawn', 'black', (0, 6)), Piece('Pawn', 'black', (1, 6)), Piece('Pawn', 'black', (2, 6)),
    Piece('Pawn', 'black', (3, 6)), Piece('Pawn', 'black', (4, 6)), Piece('Pawn', 'black', (5, 6)),
    Piece('Pawn', 'black', (6, 6)), Piece('Pawn', 'black', (7, 6)),
]

def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
    pass


#visualize pieces on board
def visualize_piece():
    for piece in white_pieces:
        x = piece_list.index(piece.type)
        screen.blit(w_images[x], (piece.position[0] * 100 + 10, piece.position[1] * 100 + 10))

    for piece in black_pieces:
        x = piece_list.index(piece.type)
        screen.blit(b_images[x], (piece.position[0] * 100 + 10, piece.position[1] * 100 + 10))


# Handle Mouse Clicks and Piece Capture
def handle_click(pos):
    global selected_piece, selected_pos, current_player
    col, row = pos[0] // 100, pos[1] // 100

    if selected_piece is None:
        for piece in white_pieces if current_player == 'white' else black_pieces:
            if piece.position == (col, row):
                selected_piece = piece
                selected_pos = piece.position
                break
    else:
        if (row, col) in selected_piece.valid_moves(selected_pos, white_pieces + black_pieces): #white + black is to check valid moves knowing where every piece is
            # Capture the opponent's piece
            target_piece = None
            for piece in white_pieces + black_pieces:
                if piece.position == (row, col):
                    target_piece = piece
                    break
            if target_piece and target_piece.color != current_player:
                if target_piece.color=='white':
                    white_pieces.remove(target_piece)
                else:
                    black_pieces.remove(target_piece)
                selected_piece.position = (row, col)
            elif not target_piece:
                selected_piece.position = (row, col)
            current_player = 'black' if current_player == 'white' else 'white'
        selected_piece = None
        selected_pos = None

#game loop and close window on quit
run=True

while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    visualize_piece()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.flip() #displays on screen
pygame.quit()