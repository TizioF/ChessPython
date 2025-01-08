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

#game loop and close window on quit
run=True
while run:
    timer.tick(fps)
    screen.fill('dark gray')

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.flip() #displays on screen
pygame.quit()





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


def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', (600 - (column * 200), row * 100, 100, 100))
        else:
            pygame.draw.rect(screen, 'light gray', (700 - (column * 200), row * 100, 100, 100))


