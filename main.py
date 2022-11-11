import tkinter as tk
import tkinter.font as font
import tkinter.messagebox
import random


class Square(tk.Button):
    def __init__(self, master, width, height, type=None, value=0,
                 x=None, y=None):
        super().__init__(master.master, bg="black", fg="black",
                         background="white", command=self.open_square)
        self.bind('<Button-3>', self.flip_status)
        self.value = value
        self.type = type
        self.status = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.master = master
        self["font"] = master.myFont

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
            self.master.clear_game()

    def get_neitherboard(self, deep=True):
        "return tupe of neitherboard value"
        value = 0
        neitherboards = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                elif x + self.x < 0 or y + self.y < 0:
                    continue
                elif (x+self.x >= self.master.width or
                      y+self.y >= self.master.height):
                    continue
                if self.master.squares[self.y+y][self.x+x].type == "Bomb":
                    value += 1
                else:
                    neitherboards += [self.master.squares[self.y+y][self.x+x]]
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
                 mine_numbers, square_with):
        super().__init__(master)
        self.status = True
        self.width = width
        self.height = height
        self.master.geometry("{}x{}".format(width*square_with,
                                            height*square_with))
        self.master.title(title)
        self.square_with = square_with
        self.mine_numbers = mine_numbers
        self.square_numbers = width*height
        self.myFont = font.Font(size=int(.8*square_with))
        self.pack()

    def new_game(self):
        """start a new game and choice a rancom x places for the mines"""
        self.squares = []
        self.mine = []
        self.clean_squares = 0
        for y in range(self.height):
            squares = []
            for x in range(self.width):
                square = Square(self, self.square_with, self.square_with,
                                "Clean", 0, x, y)
                square.place(x=self.square_with*x, y=self.square_with*y,
                             width=self.square_with,
                             height=self.square_with)
                #square['text'] = "{}-{}".format(y, x)
                squares += [square]
            self.squares += [squares]
        self.mines = [random.choice(random.choice(self.squares))
                      for i in range(self.mine_numbers)]
        for mine in self.mines:
            mine.type = "Bomb"

    def check_game(self):
        """check the game status if the player win/lose/game still open"""
        self.clean_squares += 1
        if self.clean_squares == self.square_numbers - self.mine_numbers:
            self.status = False
            self.clear_game(False)
            return True
        return False

    def clear_game(self, over=True):
        """show the content of all boxes,
           and ask the player for one more game"""
        for mine in self.mines:
            mine.status = 1
            if over:
                mine["background"] = "red"
            else:
                mine["background"] = "blue"

        for row in self.squares:
            for square in row:
                square.open_square(False)

        if over:
            res = tkinter.messagebox.askokcancel(title="Game Over!",
                                                 message="Try again?")
            if res:
                self.new_game()
        else:
            res = tkinter.messagebox.askokcancel(title="Nice Job!",
                                                 message="Play again?")
            if res:
                self.new_game()

width = 20
height = 10
mine_numbers = 30
square_with = 30
title = "Minesweeper"
root = tk.Tk()
myapp = App(root, width, height, title, mine_numbers, square_with)
myapp.new_game()
myapp.mainloop()
