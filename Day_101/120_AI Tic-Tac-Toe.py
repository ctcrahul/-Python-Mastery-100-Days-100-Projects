# AI Tic-Tac-Toe (Minimax)

board = [" " for _ in range(9)]

def print_board():
    print("\n")
    for i in range(0, 9, 3):
        print(board[i], "|", board[i+1], "|", board[i+2])
    print("\n")

def is_winner(b, player):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(b[x]==b[y]==b[z]==player for x,y,z in wins)

def is_full(b):
    return " " not in b

def minimax(b, depth, is_max):
    if is_winner(b, "O"):
        return 10 - depth
    if is_winner(b, "X"):
        return depth - 10
    if is_full(b):
        return 0
    if is_max:
        best = -100
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                best = max(best, minimax(b, depth+1, False))
                b[i] = " "
        return best
    else:
        best = 100
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                best = min(best, minimax(b, depth+1, True))
                b[i] = " "
        return best

def best_move():
    best_val = -100
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            val = minimax(board, 0, False)
            board[i] = " "
            if val > best_val:
                best_val = val
                move = i
    return move
