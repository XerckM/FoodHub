from tkinter import *
from classes.login import Login


def main():
    root = Tk()
    user = StringVar()
    pword = StringVar()
    Login(root, user, pword)
    root.mainloop()


if __name__ == '__main__':
    main()

