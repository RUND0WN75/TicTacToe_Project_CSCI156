import pygame
import random

pygame.init()

Width = 500
Height = 500
Cell = Width // 3

White = (255, 255, 255)
Lines = (0,0,0)

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe CSCI 156 Group 4")
font = pygame.font.Font(pygame.font.get_default_font(), 20)

def screen_board(board, message = None, delay = None):
    screen.fill(White)

    for i in range(1, 4):
        pygame.draw.line(screen, Lines, (i * Cell, 0), (i * Cell, Height), 2)
        pygame.draw.line(screen, Lines, (0, i* Cell), (Width, i * Cell), 2)

    for i in range(3):
        for j in range(3):
            if board[i][j] == 1:
                pygame.draw.line(screen, Lines, (j * Cell, i * Cell), ((j + 1) * Cell, (i + 1) * Cell), 2)
                pygame.draw.line(screen, Lines, ((j + 1) * Cell, i * Cell), (j * Cell, (i + 1) * Cell), 2)
            elif board[i][j] == 2:
                pygame.draw.circle(screen, Lines, (j * Cell + Cell // 2, i * Cell + Cell // 2), Cell // 2 - 2, 2)

    if message:
        sentence = font.render(message, True, Lines)
        alignment = sentence.get_rect(center = (Width //2, Height // 10))
        screen.blit(sentence, alignment)
    
    pygame.display.flip()

    if delay is not None:
        pygame.time.delay(delay)
    else:
        pygame.time.delay(0)


def player_input(board, mouseX, mouseY):
    row = mouseY // Cell
    col = mouseX // Cell

    # Check that the cell is not already in use
    if board[row][col] == 0:
        board[row][col] = 1
        return True

    return False

def computer_move(board):
    # Randomly generated
    while True:
        row, col = random.randint(0, 2), random.randint(0, 2)
        if board[row][col] == 0:
            board[row][col] = 2
            return

def player_in(board):
    r = int(input("Enter row:\n")) 
    c= int(input("Enter column:\n"))

    # check that cell is not is use
    while board[r-1][c-1] != 0:
        print("Cell already taken. Please try again.")
        r = int(input("Enter row:\n")) 
        c= int(input("Enter column:\n"))

    # place
    board[r-1][c-1] = 1

def computer_move(board):
    #randomly generated
    r, c = random.randint(0, 2), random.randint(0, 2)

    while board[r][c] != 0:
        r, c = random.randint(0, 2), random.randint(0, 2)

    board[r][c] = 2
    print(f"Computer played O at Row: {r + 1} Column: {c + 1}")

def check_win(board):
    # check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return True

    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return True

    # check negative diagonal
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return True

    #check positive diagonal
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return True

    return False

def reset_board(board):
    for i in range(3):
        for j in range(3):
            board[i][j] = 0

def display_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                print(' ', end='')
            elif board[i][j] == 1:
                print('X', end='')
            elif board[i][j] == 2:
                print('O', end='')

            if j < 2:
                print('|', end='')
            else:
                print()

        if i < 2:
            print("-----")

def main():
    # board uses a 2D array implementation
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    screen_board(board)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if player_input(board, mouseX, mouseY):
                    if check_win(board):
                        screen_board(board)
                        #print("Congratulations: You won the game!")
                        screen_board(board, "Congratulations: You won the game!", 3000)
                        running = False
                    elif all(cell != 0 for row in board for cell in row):
                        screen_board(board)
                        #print("Game ended in a draw. Better luck next time.")
                        screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
                        running = False
                    else:
                        computer_move(board)
                        if check_win(board):
                            screen_board(board)
                            #print("Computer won the game. Better luck next time.")
                            screen_board(board, "Computer won the game. Better luck next time.", 3000)
                            running = False
                        elif all(cell != 0 for row in board for cell in row):
                            #print("Game ended in a draw. Better luck next time.")
                            screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
                            running = False
                    screen_board(board)

    pygame.quit()  

if __name__ == "__main__":
    main()
