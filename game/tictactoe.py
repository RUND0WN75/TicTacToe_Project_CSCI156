import random

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

    print("Player is X, Computer is O")

    reset_board(board)

    for i in range(9):
        player_in(board)

        if check_win(board):
            display_board(board)
            print("Congratulations: You won the game!")
            break

        computer_move(board)

        if check_win(board):
            display_board(board)
            print("Computer won the game. Better luck next time.")
            break

        display_board(board)

if __name__ == "__main__":
    main()
