from tkinter import *
from classes.login import Login


def main():
    root = Tk()
    root.iconbitmap('win_ico.ico')
    root.withdraw()
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
