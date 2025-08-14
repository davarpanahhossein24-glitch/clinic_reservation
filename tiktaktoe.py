import tkinter as tk
from tkinter import messagebox

from pygame.examples.go_over_there import reset


class TikTakToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TikTakToe")
        self.current_player = "X"
        self.board = [" "] * 9
        self.buttons = []

        for i in range(9):
            btn = tk.Button(
                self.window,
                text=" ",
                font=("Arial", 20),
                width=5,
                height=2,
                command=lambda idx=i: self.on_click(idx)
            )
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

        reset_btn = tk.Button(self.window, text="Reset", command=reset)
        reset_btn.grid(row=3, column=0, columnspan=3, sticky="we")

    def on_click(self, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            self.buttons[idx].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("the end",f"plater {self.current_player} wins!")
                self.reset()
            elif " " not in self.board:
                messagebox.showinfo("mosavy", "the end!")
                self.reset()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != " ":
                return True
        return False

    def reset(self):
        self.current_player = "X"
        self.board = [" "] * 9
        for btn in self.buttons:
            btn.config(text=" ")

if __name__ == "__main__":
    game = TikTakToe
    game.window.mainloop()