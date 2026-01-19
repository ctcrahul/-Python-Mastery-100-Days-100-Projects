# AI Tic-Tac-Toe (Minimax)

board = [" " for _ in range(9)]

def print_board():
    print("\n")
    for i in range(0, 9, 3):
        print(board[i], "|", board[i+1], "|", board[i+2])
    print("\n")
