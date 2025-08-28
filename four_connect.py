import numpy as np
import pygame
import sys
import math
import random
from threading import Timer

# Game constants
ROWS, COLS = 6, 7
PLAYER_TURN, AI_TURN = 0, 1
PLAYER_PIECE, AI_PIECE = 1, 2
BLUE, BLACK, RED, YELLOW, WHITE, GREY = (0, 0, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255), (200, 200, 200)

# Pygame initialization
pygame.init()
SQUARESIZE = 100
width, height = COLS * SQUARESIZE, (ROWS + 2) * SQUARESIZE  # Extra row for buttons
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4 - Player vs AI")
circle_radius = SQUARESIZE // 2 - 5
my_font = pygame.font.SysFont("monospace", 75)
button_font = pygame.font.SysFont("monospace", 35)

def create_board():
    return np.zeros((ROWS, COLS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            color = BLACK
            if board[r][c] == PLAYER_PIECE:
                color = RED
            elif board[r][c] == AI_PIECE:
                color = YELLOW
            pygame.draw.circle(screen, color,
                               (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)),
                               circle_radius)
    pygame.display.update()

def evaluate_window(window, piece):
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, COLS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = list(board[r, c:c + 4])
            score += evaluate_window(window, piece)
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = list(board[r:r + 4, c])
            score += evaluate_window(window, piece)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or not get_valid_locations(board)

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1e10)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1e10)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value, column = -math.inf, random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value, column = new_score, col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value, column = math.inf, random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value, column = new_score, col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def draw_buttons():
    pygame.draw.rect(screen, GREY, (100, height - 90, 150, 60))
    pygame.draw.rect(screen, GREY, (width - 250, height - 90, 150, 60))
    replay_label = button_font.render("Replay", 1, BLACK)
    exit_label = button_font.render("Exit", 1, BLACK)
    screen.blit(replay_label, (125, height - 80))
    screen.blit(exit_label, (width - 220, height - 80))
    pygame.display.update()

def wait_for_replay():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 250 and height - 90 <= y <= height - 30:
                    return True  # Replay
                if width - 250 <= x <= width - 100 and height - 90 <= y <= height - 30:
                    pygame.quit()
                    sys.exit()

def main():
    while True:
        board = create_board()
        game_over = False
        turn = random.randint(PLAYER_TURN, AI_TURN)
        draw_board(board)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    if turn == PLAYER_TURN:
                        pygame.draw.circle(screen, RED, (event.pos[0], int(SQUARESIZE / 2)), circle_radius)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER_TURN:
                    col = event.pos[0] // SQUARESIZE
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
                        if winning_move(board, PLAYER_PIECE):
                            label = my_font.render("Player wins!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                        draw_board(board)
                        turn = AI_TURN

            if turn == AI_TURN and not game_over:
                col, _ = minimax(board, 5, -math.inf, math.inf, True)
                if is_valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)
                    if winning_move(board, AI_PIECE):
                        label = my_font.render("AI wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                    draw_board(board)
                    turn = PLAYER_TURN

            if not game_over and not get_valid_locations(board):
                label = my_font.render("It's a draw!", 1, BLACK)
                screen.blit(label, (40, 10))
                game_over = True
                draw_board(board)

            if game_over:
                draw_buttons()
                if wait_for_replay():
                    break  # Replay game

if __name__ == "__main__":
    main()
