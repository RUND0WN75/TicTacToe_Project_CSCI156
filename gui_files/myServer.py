import socket
import time
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 8080
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()

def send_board():
    board_str = str(board)
    for conn in playerConn:
        conn.send("Matrix".encode())
        time.sleep(1)
        conn.send(board_str.encode())

def send_msg(message):
    for conn in playerConn:
        conn.send(message.encode())

def get_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "Player One's Turn"
        conn = playerConn[0]
    else:
        player = "Player Two's Turn"
        conn = playerConn[1]

    print(player)

    send_msg(player)

    try:
        conn.send("Input".encode())
        data = conn.recv(2048*10)
        conn.settimeout(20)
        data_decoded = data.decode().split(",")
        x = int(data_decoded[0])
        y = int(data_decoded[1])

        board[x][y] = currentPlayer
        send_board()
        #send_common_msg("Matrix")
        #send_common_msg(str(board))
    except:
        conn.send("Error".encode())
        print("Error")

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

def start_server():
    try:
        server.bind((host, port))
        print("The server for CSCI 156 Project Group 4 has started")
        server.listen(2)
        accept_players()

    except socket.error as e:
        print("Error", e)

def accept_players():
    try:
        for i in range(2):
            conn, addr = server.accept()
            msg1 = "<<< You are player {} >>>".format(i+1)
            conn.send(msg1.encode())

            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))

        start_game()
        server.close()
    except socket.error as e:
        print("Error", e)

def start_game():
    result = 0
    i = 0
    while result == 0 and i < 9:
        if (i%2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        result = check_win(board)
        i += 1
    
    send_msg("Over")

    if result == 1:
        #screen_board(board)
        #screen_board(board, "Player 1 wins", 3000)
        #running = False
        win_mssg = "Player 1 wins"
    elif result == 2:
        #screen_board(board)
        #screen_board(board, "Player 2 wins", 3000)
        #running = False
        win_mssg = "Player 2 wins"

    elif all(cell != 0 for row in board for cell in row):
        #screen_board(board)
        #screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
        #running = False
        win_mssg = "Game ended in a draw. Better luck next time"
    else:
        win_mssg = "Error"
        #computer_move(board)
        #if check_win(board):
         #   screen_board(board)
          #  screen_board(board, "Computer won the game. Better luck next time.", 3000)
           # running = False
        #elif all(cell != 0 for row in board for cell in row):
         #   screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
          #  running = False
    #screen_board(board)

    send_msg(win_mssg)
    time.sleep(15)

    for conn in playerConn:
        conn.close()


#def send_common_msg(message):
 #   playerConn[0].send(message.encode())
  #  playerConn[1].send(message.encode())
   # time.sleep(15)


start_server()







"""""
import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
#while True:
conn, addr = serv.accept()
from_client = ''
while True:
  data = conn.recv(4096)
  if not data: break
  from_client += data.decode('utf8')
  print (from_client)
  conn.send("I am SERVER\n".encode())
conn.close()
print ('client disconnected and shutdown')

import socket
import threading
import pickle

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 8080
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()  

def game_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "Player One's turn"
        conn = playerConn[1]
    else:
        player = "Player Two's turn"
        conn = playerConn[1]
    print(player)
    common_message(player)
    try:
        conn.send("Input".encode())
        data = conn.recv(2048*10)
        conn.settimeout(20)
        decoded_data = data.decode().split(",")


import socket
import threading
import pickle
import pygame
import random

pygame.init()

Width = 500
Height = 500
Cell = Width // 3

White = (255, 255, 255)
Lines = (0, 0, 0)

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe CSCI 156 Group 4")
font = pygame.font.Font(pygame.font.get_default_font(), 20)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen()

players = [1, 2]
current_player = random.choice(players)

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def screen_board(board, message=None, delay=None):
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
    while True:
        row, col = random.randint(0, 2), random.randint(0, 2)
        if board[row][col] == 0:
            board[row][col] = 2
            return

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

def handle_client(conn, player):
    global current_player
    conn.send(pickle.dumps(player))
    while True:
        try:
            data = pickle.loads(conn.recv(1024))
            if not data:
                print("Disconnected")
                break
            if player == current_player:
                mouseX, mouseY = data
                if player_input(board, mouseX, mouseY):
                    if check_win(board):
                        screen_board(board)
                        screen_board(board, f"Player {player} won the game!", 3000)
                        reset_board(board)
                    elif all(cell != 0 for row in board for cell in row):
                        screen_board(board)
                        screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
                        reset_board(board)
                    else:
                        current_player = 3 - current_player  # Switch player turn
                        screen_board(board)
            conn.sendall(pickle.dumps((board, current_player)))
        except Exception as e:
            print(e)
            break
    conn.close()

def start_server():
    print("Server is listening for connections...")
    global current_player
    current_player = random.choice(players)
    while True:
        conn, addr = server.accept()
        print(f"Connection established with {addr}")
        player_thread = threading.Thread(target=handle_client, args=(conn, current_player))
        player_thread.start()

if __name__ == "__main__":
    start_server()

"""