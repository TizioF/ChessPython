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



class Board:
    def __init__(self):
        # Create an 8x8 board, initially empty (None)
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def get_piece_at(self, position):
        col, row = position
        return self.board[row][col]

    def set_piece_at(self, position, piece):
        col, row = position
        self.board[row][col] = piece

    def move_piece(self, piece, new_position):
        old_position = piece.position
        self.set_piece_at(old_position, None)
        self.set_piece_at(new_position, piece)
        piece.position = new_position



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

    def valid_moves(self, position, board):
        """Override in child classes to define specific move logic."""
        return []


class Pawn(Piece):
    def valid_moves(self, position, board):
        """Define valid moves for a Pawn."""
        col, row = position
        moves = []
        direction = 1 if self.color == 'white' else -1  # White moves down, black moves up


        if 0 <= row + direction < 8:
            forward_piece = board.get_piece_at((col, row + direction))
            if forward_piece is None:
                moves.append((col, row + direction))

                if (self.color == 'white' and row == 1) or (self.color == 'black' and row == 6):
                    two_step_piece = board.get_piece_at((col, row + 2 * direction))
                    if two_step_piece is None:
                        moves.append((col, row + 2 * direction))

        for dx in [-1, 1]:
            if 0 <= col + dx < 8 and 0 <= row + direction < 8:
                target = board.get_piece_at((col + dx, row + direction))
                if target and target.color != self.color:
                    moves.append((col + dx, row + direction))

        print(f"Valid moves for Pawn at {position}: {moves}")
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
                if board.get_piece_at((nx,ny)) is None:
                    moves.append((nx, ny))
                elif board.get_piece_at((nx, ny)).color != self.color:
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
    Rook('Rook', 'white', (0, 0)), Knight('Knight', 'white', (1, 0)), Bishop('Bishop', 'white', (2, 0)),
    Queen('Queen', 'white', (3, 0)), King('King', 'white', (4, 0)), Bishop('Bishop', 'white', (5, 0)),
    Knight('Knight', 'white', (6, 0)), Rook('Rook', 'white', (7, 0)),
    Pawn('Pawn', 'white', (0, 1)), Pawn('Pawn', 'white', (1, 1)), Pawn('Pawn', 'white', (2, 1)),
    Pawn('Pawn', 'white', (3, 1)), Pawn('Pawn', 'white', (4, 1)), Pawn('Pawn', 'white', (5, 1)),
    Pawn('Pawn', 'white', (6, 1)), Pawn('Pawn', 'white', (7, 1)),
]

# Initialize black pieces
black_pieces = [
    Rook('Rook', 'black', (0, 7)), Knight('Knight', 'black', (1, 7)), Bishop('Bishop', 'black', (2, 7)),
    Queen('Queen', 'black', (3, 7)), King('King', 'black', (4, 7)), Bishop('Bishop', 'black', (5, 7)),
    Knight('Knight', 'black', (6, 7)), Rook('Rook', 'black', (7, 7)),
    Pawn('Pawn', 'black', (0, 6)), Pawn('Pawn', 'black', (1, 6)), Pawn('Pawn', 'black', (2, 6)),
    Pawn('Pawn', 'black', (3, 6)), Pawn('Pawn', 'black', (4, 6)), Pawn('Pawn', 'black', (5, 6)),
    Pawn('Pawn', 'black', (6, 6)), Pawn('Pawn', 'black', (7, 6)),
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

selected_piece = None
selected_pos = None

# Handle Mouse Clicks and Piece Capture
def handle_click(pos):
    global selected_piece, selected_pos, current_player
   # print(current_player)
   # print(pos)
    col, row = pos[0] // 100, pos[1] // 100
    print(col)
    print(row)
    print(board.get_piece_at((col,row)))
    #print(board.get_piece_at((col,row)))
    if selected_piece is None:
        piece = board.get_piece_at((col, row))
        if piece and piece.color == current_player:
            selected_piece = piece
            selected_pos = piece.position
            print('clicked piece!')
            print(selected_piece.type)
    else:
        print('enter the else to move')

        if (col, row) in selected_piece.valid_moves(selected_pos, board):
            # Capture the opponent's piece
            print('enter the if')
            target_piece = board.get_piece_at((col, row)) #if there is no piece target_piece is None
            print(target_piece)
            if target_piece and target_piece.color != current_player:
                if target_piece.color=='white':
                    white_pieces.remove(target_piece)
                else:
                    black_pieces.remove(target_piece)
            board.move_piece(selected_piece, (col, row))
            print('piece moved')
            if current_player=='white':
                current_player='black'
            else:
                current_player='white'
        selected_piece = None
        selected_pos = None

#game loop and close window on quit
run=True

current_player='white'

board = Board()
for piece in white_pieces:
    board.set_piece_at(piece.position, piece)
for piece in black_pieces:
    board.set_piece_at(piece.position, piece)

while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    visualize_piece()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())
            # After you click the piece, before doing anything, call this debug function:

    pygame.display.flip() #displays on screen
pygame.quit()
