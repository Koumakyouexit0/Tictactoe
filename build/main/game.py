import pygame
import sys
import subprocess

pygame.init()

WIDTH, HEIGHT = 600, 700  
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SQUARE_SIZE = WIDTH // 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

icon = pygame.image.load('icon.png')  
pygame.display.set_icon(icon)

font = pygame.font.SysFont('Arial', 30)

player1_name = ""
player2_name = "MaidenTTT AI"
player1_score = 0
player2_score = 0

PLAYER_X = 1
PLAYER_O = 2

board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

def get_player_name(prompt):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BG_COLOR)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        prompt_surface = font.render(prompt, True, WHITE)
        screen.blit(prompt_surface, (WIDTH // 2 - prompt_surface.get_width() // 2, HEIGHT // 2 - 100))
        pygame.display.flip()

    return text

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), 7)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), 7)
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 7)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), 7)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == PLAYER_X:
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 15)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), 15)
            elif board[row][col] == PLAYER_O:
                pygame.draw.circle(screen, BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                  int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 60, 15)

def mark_square(row, col, player):
    board[row][col] = player

def check_win(player):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_board_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                return False
    return True


def minimax(board, depth, alpha, beta, is_maximizing):
    if check_win(PLAYER_X):
        return -10 + depth, None
    if check_win(PLAYER_O):
        return 10 - depth, None
    if is_board_full():
        return 0, None
    
    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = PLAYER_O
                    score, _ = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = PLAYER_X
                    score, _ = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = None
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_move

def get_best_move():
    _, best_move = minimax(board, 0, -float('inf'), float('inf'), True)
    return best_move

def ask_quit():
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    text = font.render("Thoát Game? (Y/N)", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while True:
        screen.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def ask_play_again():
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    text = font.render("Chơi lại? (Y/N)", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while True:
        screen.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def reset_board():
    global board
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]

def main():
    global player1_name, player2_name, player1_score, player2_score

    player1_name = get_player_name("Điền tên user:")
    current_player = PLAYER_X
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if ask_quit():
                    pygame.quit()
                    sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and current_player == PLAYER_X:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] is None:
                    mark_square(clicked_row, clicked_col, current_player)
                    if check_win(current_player):
                        player1_score += 1
                        game_over = True
                    elif is_board_full():
                        game_over = True
                    current_player = PLAYER_O

            if not game_over and current_player == PLAYER_O:
                pygame.time.delay(500)
                move = get_best_move()
                if move is not None:
                    row, col = move
                    mark_square(row, col, current_player)
                    if check_win(current_player):
                        player2_score += 1
                        game_over = True
                    elif is_board_full():
                        game_over = True
                    current_player = PLAYER_X

            if game_over:
                pygame.time.delay(1000)
                if ask_play_again():
                    reset_board()
                    game_over = False
                    current_player = PLAYER_X
                else:
                    if ask_quit():
                        pygame.quit()
                        sys.exit()
                    else:
                        reset_board()
                        game_over = False
                        current_player = PLAYER_X

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()

        text1 = font.render(f"{player1_name}: {player1_score}", True, RED)
        text2 = font.render(f"{player2_name}: {player2_score}", True, BLUE)
        screen.blit(text1, (10, HEIGHT - 50))
        screen.blit(text2, (WIDTH - text2.get_width() - 10, HEIGHT - 50))

        pygame.display.update()

python_script = 'build/main/mail.py'

subprocess.run(['python', python_script])
if __name__ == "__main__":
    draw_lines()
    main()
