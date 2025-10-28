import tkinter as tk

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]
current_player = "X"

#Create Main Window
window = tk.Tk()
window.title("Tic-Tac-Toe")
window.geometry("400x400")

# Create Result Label
result_label = tk.Label(window, text="Player X's Turn", font=("Arial", 16))
result_label.grid(row=0, column=0, columnspan=3)

buttons = [[None for _ in range(3)] for _ in range(3)]

def reset_game():
    global current_player, board
    current_player = "X"
    board = [["", "", ""],["", "", ""],["", "", ""]]
    result_label.config(text="Player X's Turn")
    for row in buttons:
        for button in row:
            button.config(text="", state="normal")


def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state="disabled")

def on_click(row, col):
    global current_player

    # Check if the cell is empty
    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = current_player
        board[row][col] = current_player

        # Check for Winner or Draw
        winner = check_winner(board)
        if winner:
            result_label.config(text=f"Plater {winner} Wins!")
            disable_buttons()
        elif is_draw(board):
            result_label.config(text="Its a Draw!")
        else:
            current_player = "0" if current_player == "X" else "X"
            result_label.config(text=f"Player {current_player}'s Turn")


def create_board():
    for row in range(3):
        for col in range(3):
            buttons[row][col] = tk.Button(window, text="", font=("Arial", 24), height=2, width=5,
                                    command=lambda r=row, c=col: on_click(r,c))
            buttons[row][col].grid(row=row+1, column=col)


def check_winner(board):
    # Check Rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]

    # Check Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]

    # Check Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[1][1]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[1][1]

    return None

def is_draw(board):
    for row in board:
        if "" in row:
            return False
    return True

create_board()
reset_button = tk.Button(window, text="Reset", font=("Arial", 14), command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3)

window.mainloop()



