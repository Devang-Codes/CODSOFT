import tkinter as tk
from tkinter import messagebox

# --------------------------
# Game Logic
# --------------------------

board = [" " for _ in range(9)]

human = "X"
ai = "O"

def check_winner(brd, player):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for condition in win_conditions:
        if all(brd[i] == player for i in condition):
            return True

    return False


def is_draw(brd):
    return " " not in brd


def minimax(brd, depth, maximizing):

    if check_winner(brd, ai):
        return 1

    if check_winner(brd, human):
        return -1

    if is_draw(brd):
        return 0

    if maximizing:

        best_score = -float("inf")

        for i in range(9):
            if brd[i] == " ":
                brd[i] = ai
                score = minimax(brd, depth + 1, False)
                brd[i] = " "
                best_score = max(score, best_score)

        return best_score

    else:

        best_score = float("inf")

        for i in range(9):
            if brd[i] == " ":
                brd[i] = human
                score = minimax(brd, depth + 1, True)
                brd[i] = " "
                best_score = min(score, best_score)

        return best_score


def best_move():

    best_score = -float("inf")
    move = None

    for i in range(9):

        if board[i] == " ":

            board[i] = ai

            score = minimax(board, 0, False)

            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    return move


# --------------------------
# GUI Functions
# --------------------------

def ai_turn():

    move = best_move()

    if move is not None:
        board[move] = ai
        buttons[move]["text"] = ai
        buttons[move]["state"] = "disabled"

    if check_winner(board, ai):
        messagebox.showinfo("Game Over", "AI Wins!")
        disable_board()
        return

    if is_draw(board):
        messagebox.showinfo("Game Over", "It's a Draw!")
        disable_board()


def player_move(index):

    if board[index] == " ":

        board[index] = human

        buttons[index]["text"] = human
        buttons[index]["state"] = "disabled"

        if check_winner(board, human):
            messagebox.showinfo("Game Over", "You Win!")
            disable_board()
            return

        if is_draw(board):
            messagebox.showinfo("Game Over", "It's a Draw!")
            disable_board()
            return

        ai_turn()


def disable_board():

    for btn in buttons:
        btn["state"] = "disabled"


def reset_game():

    global board

    board = [" " for _ in range(9)]

    for btn in buttons:
        btn["text"] = ""
        btn["state"] = "normal"


# --------------------------
# GUI Window
# --------------------------

root = tk.Tk()

root.title("Tic Tac Toe AI")
root.geometry("400x500")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Unbeatable Tic Tac Toe AI",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

buttons = []

for row in range(3):

    for col in range(3):

        index = row * 3 + col

        btn = tk.Button(
            frame,
            text="",
            font=("Arial", 24, "bold"),
            width=5,
            height=2,
            command=lambda idx=index: player_move(idx)
        )

        btn.grid(row=row, column=col)

        buttons.append(btn)

reset_btn = tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 14),
    command=reset_game
)

reset_btn.pack(pady=20)

root.mainloop()