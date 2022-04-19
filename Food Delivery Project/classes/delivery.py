from tkinter import *
from classes.login import Login
import mysql.connector


class Delivery(object):
    def __init__(self):
        self.root = Tk()
        # self.root.overrideredirect(True)
        # self.root.attributes('-fullscreen', True)
        self.user = StringVar()
        self.pwd = StringVar()
        Login(self.root, self.user, self.pwd)
        self.output_frame(self.root)
        self.root.mainloop()

    @staticmethod
    def output_frame(root):
        # set frame width and height
        dframe_width = 960
        dframe_height = 540

        # calculate x and y coordinates for window position in screen
        screen_pos_x = (root.winfo_screenwidth() / 2) - (dframe_width / 2)
        screen_pos_y = (root.winfo_screenheight() / 2) - (dframe_height / 2)

        # frame title, color, and size
        root.title("Food Delivery")
        root.configure(bg='gray12')
        root.geometry('%dx%d+%d+%d' % (dframe_width, dframe_height, screen_pos_x, screen_pos_y))
