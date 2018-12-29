import numpy as np
import pygame
import os
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))
    print("\n")

def winning_move(board, row, col, piece):
    if (vertical(board, row, col, piece, set()) or
         horizontal(board, row, col, piece, set()) or
         mainDiagonal(board, row, col, piece, set()) or
         leadingDiagonal(board, row, col, piece, set())
    ):
        return True
    else:
        return False

def vertical(board, row, col, piece, visited):
    if row >= ROW_COUNT or col >= COLUMN_COUNT or board[row][col] != piece or (str(row) + "," + str(col)) in visited:
        return False
    visited.add(str(row) + "," + str(col))
    if len(visited) == 4:
        return True

    if(vertical(board, row + 1, col, piece, visited) or
        vertical(board, row - 1, col, piece, visited)
    ):
        return True
    return False

def horizontal(board, row, col, piece, visited):
    if row >= ROW_COUNT or col >= COLUMN_COUNT or board[row][col] != piece or (str(row) + "," + str(col)) in visited:
        return False
    visited.add(str(row) + "," + str(col))
    if len(visited) == 4:
        return True

    if(horizontal(board, row, col + 1, piece, visited) or
        horizontal(board, row, col - 1, piece, visited)
    ):
        return True
    return False

def mainDiagonal(board, row, col, piece, visited):
    if row >= ROW_COUNT or col >= COLUMN_COUNT or board[row][col] != piece or (str(row) + "," + str(col)) in visited:
        return False
    visited.add(str(row) + "," + str(col))
    if len(visited) == 4:
        return True

    if(mainDiagonal(board, row + 1, col + 1, piece, visited) or
        mainDiagonal(board, row - 1, col -1, piece, visited)
    ):
        return True
    return False

def leadingDiagonal(board, row, col, piece, visited):
    if row >= ROW_COUNT or col >= COLUMN_COUNT or board[row][col] != piece or (str(row) + "," + str(col)) in visited:
        return False
    visited.add(str(row) + "," + str(col))
    if len(visited) == 4:
        return True

    if(leadingDiagonal(board, row + 1, col - 1, piece, visited) or
        leadingDiagonal(board, row - 1, col + 1, piece, visited)
    ):
        return True
    return False

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQAURE_SIZE, r * SQAURE_SIZE + SQAURE_SIZE, SQAURE_SIZE, SQAURE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQAURE_SIZE + SQAURE_SIZE/2), int(r * SQAURE_SIZE + SQAURE_SIZE + SQAURE_SIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQAURE_SIZE + SQAURE_SIZE/2), height - int(r * SQAURE_SIZE + SQAURE_SIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQAURE_SIZE + SQAURE_SIZE/2), height - int(r * SQAURE_SIZE + SQAURE_SIZE/2)), RADIUS)

    pygame.display.update()


board = create_board()
print("Game Start")
print_board(board)
game_over = False
turn = 0

pygame.init()

SQAURE_SIZE = 100

width = COLUMN_COUNT * SQAURE_SIZE
height = (ROW_COUNT + 1) * SQAURE_SIZE

size = (width, height)

RADIUS = int(SQAURE_SIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 50)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(1)

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQAURE_SIZE))
            posX = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posX, int(SQAURE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posX, int(SQAURE_SIZE/2)), RADIUS)
        pygame.display.update() 

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQAURE_SIZE))
            if turn == 0:
                print("Player 1's Turn")
                posX = event.pos[0]
                col = int(math.floor(posX / SQAURE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, row, col, 1):
                        print("Player 1 Won The Game!")
                        label = myFont.render("Player 1 Won The Game!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            else:
                print("Player 2's Turn")
                posX = event.pos[0]
                col = int(math.floor(posX / SQAURE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, row, col, 2):
                        print("Player 2 Won The Game!")
                        label = myFont.render("Player 2 Won The Game!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(5000)