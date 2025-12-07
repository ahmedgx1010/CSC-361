import math
import tkinter as tk
from tkinter import messagebox

def check_winner(board):
    winning_lines = [
        (0, 1, 2),  
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),  
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),  
        (2, 4, 6),
    ]
    for a, b, c in winning_lines:
        if board[a] == board[b] == board[c] and board[a] in ['X', 'O']:
            return board[a]
    if all(cell in ['X', 'O'] for cell in board):
        return 'draw'
    return None

def minimax(board, is_maximizing, ai_player, human_player, depth):
    result = check_winner(board)
    if result == ai_player:
        return 10 - depth  
    elif result == human_player:
        return depth - 10  
    elif result == 'draw':
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] not in ['X', 'O']:
                saved = board[i]
                board[i] = ai_player
                score = minimax(board, False, ai_player, human_player, depth + 1)
                board[i] = saved
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] not in ['X', 'O']:
                saved = board[i]
                board[i] = human_player
                score = minimax(board, True, ai_player, human_player, depth + 1)
                board[i] = saved
                best_score = min(best_score, score)
        return best_score

def best_move(board, ai_player, human_player):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] not in ['X', 'O']:
            saved = board[i]
            board[i] = ai_player
            score = minimax(board, False, ai_player, human_player, 0)
            board[i] = saved
            if score > best_score:
                best_score = score
                move = i
    return move

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Minimax)")

        
        self.human_player = 'X'
        self.ai_player = 'O'

        
        self.board = [str(i + 1) for i in range(9)]

       
        self.buttons = []
        self.create_widgets()

       
        self.game_over = False

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        for i in range(9):
            btn = tk.Button(
                frame,
                text="",
                font=("Arial", 32),
                width=3,
                height=1,
                command=lambda idx=i: self.on_cell_clicked(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

    def on_cell_clicked(self, index):
        if self.game_over:
            return

       
        if self.board[index] in ['X', 'O']:
            return

       
        self.board[index] = self.human_player
        self.update_buttons()

        
        if self.check_and_handle_game_over():
            return

       
        self.root.after(200, self.ai_turn) 

    def ai_turn(self):
        if self.game_over:
            return

        move = best_move(self.board, self.ai_player, self.human_player)
        if move is not None:
            self.board[move] = self.ai_player
            self.update_buttons()
            self.check_and_handle_game_over()

    def update_buttons(self):
        for i in range(9):
            value = self.board[i]
            if value in ['X', 'O']:
                self.buttons[i]["text"] = value
                if value == 'X':
                    self.buttons[i]["fg"] = "blue"
                else:
                    self.buttons[i]["fg"] = "red"
            else:
                self.buttons[i]["text"] = ""

    def check_and_handle_game_over(self):
        result = check_winner(self.board)
        if result is None:
            return False

        self.game_over = True
        if result == self.human_player:
            message = "You win!"
        elif result == self.ai_player:
            message = "AI wins"
        else:
            message = "It's a draw!"

        answer = messagebox.askyesno("Game Over", message + "\n\nPlay again?")
        if answer:
            self.reset_game()
        else:
            self.root.destroy()
        return True

    def reset_game(self):
        self.board = [str(i + 1) for i in range(9)]
        self.game_over = False
        self.update_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()