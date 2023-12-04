import pygame
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Enter the server IP to connect: ")
port = 8080

playerOne = 1
playerTwo = 2
currentPlayer = 0

msg1 = "Waiting for other player"
msg2 = ""
allow = 0
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def thead_creation(target):
    t = threading.Thread(target= target)
    t.daemon = True
    t.start()

pygame.init()

Width = 500
Height = 500
Cell = Width // 3

White = (255, 255, 255)
Lines = (0,0,0)

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe CSCI 156 Group 4")
font = pygame.font.Font(pygame.font.get_default_font(), 20) 

def player_start():
    global currentPlayer
    global mssg
    try:
        client.connect((host, port))
        print("Connected to : ", host)
        data_received = client.recv(2048*10)
        player_message = data_received.decode()
        if "1" in player_message:
            currentPlayer = 1
        else:
            currentPlayer = 2
        start_game()
        client.close()        
    except socket.error as e:
        print("Connection error: ", e)

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

def start_player():
    global currentPlayer
    global msg2
    try:
        client.connect((host, port))
        data_received = client.recv(2048*10)
        msg2 = data_received.decode()
        if "1" in msg2:
            currentPlayer = 1
        else:
            currentPlayer = 2
        start_game()
        client.close()
    except socket.error as e:
        print ("Connection error", e)

def start_game():  
    running = True
    global msg1
    global msg2
    global board
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                move = player_input(board, mouseX, mouseY)
                if move:
                    client.send(f"{move[0]},{move[1]}".encode())
                    """
                    if check_win(board):
                        screen_board(board)
                        screen_board(board, "Congratulations: You won the game!", 3000)
                        running = False
                    elif all(cell != 0 for row in board for cell in row):
                        screen_board(board)
                        screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
                        running = False
                    else:
                        computer_move(board)
                        if check_win(board):
                            screen_board(board)
                            screen_board(board, "Computer won the game. Better luck next time.", 3000)
                            running = False
                        elif all(cell != 0 for row in board for cell in row):
                            screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
                            running = False
                    screen_board(board)
                """
        
        if msg1 == "":
            break

        screen_board(board)
        pygame.display.update()

def msg_accept():
    global board
    global msg1
    global msg2
    global allow
    while True:
        data_received = client.recv(2048*10)
        data_decoded = data_received.decode()
        

        if data_decoded == "Matrix":
            matrix_received = client.recv(2048*100)
            matrix_received_decoded = matrix_received.decode("utf-8")
            board = eval(matrix_received_decoded)
            screen_board(board)
        
        elif data_decoded == "Over":
            message_received = client.recv(2048*100)
            message_received_decoded = message_received.decode("utf-8")
            msg2 = message_received_decoded
            msg1 = "Game Over"
            break
        else:
            msg1 = message_received_decoded

start_player()
