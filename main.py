import tkinter as tk
import tkinter.font as font
import random


class Square(tk.Button):
    def __init__(self, master, width, height, type=None, value=0,
                 x=None, y=None):
        super().__init__(master.master, bg="black", fg="black",
                         background="white", command=self.open_square)
        self.bind('<Button-3>',self.flip_status)
        self.value = value
        self.type = type
        self.status = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.master = master
        myFont = font.Font(size=20)
        self["font"] = myFont


    def open_square(self, deep=True):
        "to check if the square is clean or hold a Mine"
        if self.status:
            return 1
        self.status = 1
        if self.type == "Clean":
            value = self.get_neitherboard(deep=deep)
            if deep:
                self.master.check_game()
            if value:
                self.value = value
                self['text'] = str(value)
            return True
        elif deep:
            self.master.game_over()

    def get_neitherboard(self, deep=True):
        "return tupe of neitherboard value"
        value = 0
        neitherboards = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif i + self.x < 0 or j + self.y < 0:
                    continue
                elif (i+self.x >= len(self.master.squares) or
                      j+self.y >= len(self.master.squares)):
                    continue
                if self.master.squares[self.x+i][self.y+j].type == "Bomb":
                    value += 1
                else:
                    neitherboards += [self.master.squares[self.x+i][self.y+j]]
        self["background"] = "green"
        if not value and deep:
            for neitherboard in neitherboards:
                if not neitherboard.status:
                    neitherboard.open_square()
        else:
            return value
    
    def flip_status(self, *args):
        if self.status == 1:
            return
        if self.status & 2:
            self.status = 0
            self["background"] = "white"
        elif not self.status:
            self.status = 2
            self["background"] = "blue"


class App(tk.Frame):
    def __init__(self, master, width, height, title,
                 mine_numbers, square_numbers):
        super().__init__(master)
        self.status = True
        self.width = width
        self.height = height
        self.master.geometry("{}x{}".format(width, height))
        self.master.title(title)
        self.square_numbers = square_numbers
        self.mine_numbers = mine_numbers
        self.squares = []
        self.mine = []
        self.clean_squares = 0
        self.pack()

    def new_game(self):
        squares_per_line = int(self.square_numbers**0.5)
        square_with = int(self.width/squares_per_line)
        for i in range(squares_per_line):
            squares = []
            for j in range(squares_per_line):
                square = Square(self, square_with, square_with,
                                "Clean", 0, i, j)
                square.place(x=square_with*i, y=square_with*j,
                             width=square_with, height=square_with)
                squares += [square]
            self.squares += [squares]
        self.mines = [random.choice(random.choice(self.squares))
                      for i in range(self.mine_numbers)]
        for mine in self.mines:
            mine.type = "Bomb"

    def check_game(self):
        self.clean_squares += 1
        if self.clean_squares == self.square_numbers - self.mine_numbers:
            self.status = False
            self.clear_game(False)
            return True
        return False

    def game_over(self):
        self.clear_game()
        # result = tk.Label(self,"game_over")
        # result.place(x=0, y=self.height//2, width=self.width,
        # height = self.height)

    def clear_game(self, over=True):
        if over:
            print("game over")
        else:
            print("great job")
        for mine in self.mines:
            if over:
                mine["background"] = "red"
            else:
                mine["background"] = "blue"
        
        for row in self.squares:
            for square in row:
                # square['state'] = 'disabled'
                square.open_square(False)


width = 400
height = 400
mine_numbers = 10
squares_numbers = 100
title = "Minesweeper"
root = tk.Tk()
myapp = App(root, width, height, title, mine_numbers, squares_numbers)
myapp.new_game()
myapp.mainloop()
