import tkinter as tk


class App(tk.Frame):
    def __init__(self, master, width, height, title):
        super().__init__(master)
        self.master.geometry("{}x{}".format(width, height))
        self.master.title(title)
        self.pack()


width = 400
height = 400
title = "Minesweeper"
root = tk.Tk()
myapp = App(root, width, height, title)
myapp.mainloop()
