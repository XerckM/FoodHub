from tkinter import *
from classes.login import Login
import mysql.connector


class Delivery(object):
    def __init__(self):
        self.root = Tk()
        self.user = StringVar()
        self.pwd = StringVar()
        Login(self.root, self.user, self.pwd)
        self.output_frame(self.root)
        self.root.mainloop()

    @staticmethod
    def output_frame(root):
        # Main window settings
        rframe_width = 1080
        rframe_height = 720
        screen_pos_x = (root.winfo_screenwidth() / 2) - (rframe_width / 2)
        screen_pos_y = (root.winfo_screenheight() / 2) - (rframe_height / 2)
        root.title("Food Delivery")
        root.configure(bg='gray12')
        root.geometry('%dx%d+%d+%d' % (rframe_width, rframe_height, screen_pos_x, screen_pos_y))
