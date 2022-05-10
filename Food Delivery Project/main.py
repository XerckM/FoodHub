from tkinter import *
from classes.login import Login
from classes.restaurant import Restaurant


def main():
    root = Tk()
    root.iconbitmap('win_ico.ico')
    root.withdraw()
    Login(root)
    # Restaurant(root)
    root.mainloop()


if __name__ == '__main__':
    main()
