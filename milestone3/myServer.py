import socket
import threading
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 8080
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()

def send_board(conn):
    board_str = str(board)
    conn.send("Matrix".encode())
    conn.send(board_str.encode())

def send_msg(conn, message):
    conn.send(message.encode())

def get_input(conn, currentPlayer):
    try:
        conn.send("Input".encode())
        data = conn.recv(2048*10)
        conn.settimeout(20)
        data_decoded = data.decode().split(",")
        x = int(data_decoded[0])
        y = int(data_decoded[1])

        board[x][y] = currentPlayer
        send_msg(conn, "Matrix")
        time.sleep(0.5)
        send_msg(conn, str(board))
    except:
        send_msg(conn, "Error")
        print("Error")

def check_win(board):
    winner = 0
    # check rows
    for i in range(3):
       if board[i][0] == board[i][1] == board[i][2]:
            winner = board[i][0]
            if winner != 0:
                break
    
    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            winner = board[0][i]
            if winner != 0:
                break

    # check diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        winner = board[0][2]
        
    return winner

def handle_client(conn, addr, player):
    try:
        msg = "<<< You are player {} >>>".format(player)
        conn.send(msg.encode())

        while True:
            send_board(conn)
            get_input(conn, player)
            result = check_win(board)

            if result != 0 or all(cell != 0 for row in board for cell in row):
                break

        if result == 1:
            win_msg = "Game won by Player 1"
        elif result == 2:
            win_msg = "Game won by Player 2"
        elif all(cell != 0 for row in board for cell in row):
            win_msg = "Game ended in a draw. Better luck next time"
        else:
            win_msg = "Error"

        send_msg(conn, win_msg)
        time.sleep(2)
        send_msg(conn, "Over")

        conn.close()
        playerConn.remove(conn)
        playerAddr.remove(addr)
        print("Player {} - [{}:{}] disconnected".format(player, addr[0], str(addr[1])))
    except socket.error as e:
        print("Error", e)

def accept_players():
    try:
        player = 1
        while True:
            conn, addr = server.accept()
            msg1 = "<<< You are player {} >>>".format(player)
            conn.send(msg1.encode())

            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}] connected".format(player, addr[0], str(addr[1])))
            
            # Check if there are enough players to start a game
            if len(playerConn) >= 2:
                thread_creation(start_game)

            player += 1
    except socket.error as e:
        print("Error", e)

def start_game():
    result = 0
    i = 0
    current_player = playerOne

    while result == 0 and i < 9:
        if (i % 2 == 0):
            get_input(playerConn[0], playerOne)
        else:
            get_input(playerConn[1], playerTwo)
        result = check_win(board)
        i += 1
        if current_player == playerOne:
            current_player = playerTwo 
        else:
            current_player = playerOne

    if result == 1:
        win_msg = "Game won by Player 1"
    elif result == 2:
        win_msg = "Game won by Player 2"
    elif all(cell != 0 for row in board for cell in row):
        win_msg = "Game ended in a draw. Better luck next time"
    else:
        win_msg = "Error"

    send_msg(playerConn[0], win_msg)
    time.sleep(2)
    send_msg(playerConn[1], "Over")
    send_msg(playerConn[1], win_msg)
    
    time.sleep(10)

    for conn in playerConn:
        conn.close()

def thread_creation(target):
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()

def start_server():
    try:
        server.bind((host, port))
        print("The server for CSCI 156 Project Group 4 has started")
        server.listen(4)
        accept_players()

    except socket.error as e:
        print("Error", e)

start_server()
