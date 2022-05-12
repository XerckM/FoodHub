from tkinter import *
from classes.login import Login
from classes.restaurant import Restaurant
from classes.customer import Customer
from classes.driver import Driver


def main():
    root = Tk()
    root.iconbitmap('win_ico.ico')
    root.withdraw()
    Login(root)
    # Restaurant(root, "1")
    # Customer(root, "1")
    # Driver(root, "1")
    root.mainloop()


if __name__ == '__main__':
    main()
