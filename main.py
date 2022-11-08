import tkinter as tk
import random


class Square(tk.Button):
    def __init__(self, master, width, height, type=None, value=0, 
                 x=None, y=None):
        super().__init__(master.master, bg="black",fg="black", background="white",
                         command=self.open_square)
        self.value = value
        self.type = type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.master = master
    
    def open_square(self):
        "to check if the square is clean or hold a Mine"
        if self.type == "Clean":
            value = self.get_neitherboard()
            if value:
                self.value = value
                self['text'] = str(value)
                self["background"]="green"
            return True
        else:
            print("game over")
            self.master.game_over()

    def get_neitherboard(self):
        "return tupe of neitherboard value"
        value = 0
        neitherboards = []
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                elif i + self.x < 0 or j + self.y<0:
                    continue
                elif i+self.x >= len(self.master.squares) or \
                j+self.y >= len(self.master.squares):
                    continue
                if self.master.squares[self.x+i][self.y+j].type == "Bomb":
                    value += 1
                else:
                    neitherboards += [self.master.squares[self.x+i][self.y+j]]
        if not(value):
            self["background"]="green"
            for neitherboard in neitherboards:
                neitherboard.open_square()
        else:
            return value


class App(tk.Frame):
    def __init__(self, master, width, height, title,
                 mine_numbers, square_numbers):
        super().__init__(master)
        self.width = width
        self.height = height
        self.master.geometry("{}x{}".format(width, height))
        self.master.title(title)
        self.square_numbers = square_numbers
        self.mine_numbers = mine_numbers
        self.squares = []
        self.mine = []
        self.pack()
    
    def new_game(self):
        squares_per_line = int(self.square_numbers**0.5)
        square_with = int(self.width/squares_per_line)
        for i in range(squares_per_line):
            squares = []
            for j in range(squares_per_line):
                square = Square(self, square_with, square_with, "Clean", 0, i, j)
                square.place(x=square_with*i, y=square_with*j, width = square_with, height = square_with)
                squares += [square]
            self.squares += [squares]
        self.mines = [random.choice(random.choice(self.squares)) for i in range(self.mine_numbers)]
        for mine in self.mines:
            mine.type = "Bomb"      

    def game_over(self):
        for row in self.squares:
            for square in row:
                square.destroy()


width = 400
height = 400
mine_numbers = 5
squares_numbers = 36
title = "Minesweeper"
root = tk.Tk()
myapp = App(root, width, height, title, mine_numbers, squares_numbers)
myapp.new_game()
myapp.mainloop()
