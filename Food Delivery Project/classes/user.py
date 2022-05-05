from tkinter import *
from tkinter import messagebox
import mysql.connector


class User(object):
    def __init__(self, root):
        self.root = root
        self.user_frame(self.root)

    def user_frame(self, root):
        # database connector
        sql_db = mysql.connector.connect(host='localhost',
                                         port='3307',
                                         user='root',
                                         passwd='',
                                         database='food_delivery')

        # top level frame and window icon
        frame = Toplevel(root)
        frame.iconbitmap('win_ico.ico')

        # set frame width and height
        frame_width = 1080
        frame_height = 720

        # calculate x and y coordinates for window position in screen
        screen_pos_x = (frame.winfo_screenwidth() / 2) - (frame_width / 2)
        screen_pos_y = (frame.winfo_screenheight() / 2) - (frame_height / 2)

        # frame title, color, and size
        frame.title("FoodHub")
        frame.resizable(False, False)
        frame.configure(bg='grey')
        frame.geometry('%dx%d+%d+%d' % (frame_width, frame_height, screen_pos_x, screen_pos_y))

        # TODO: Add content below here

        label = Label(frame, text="USER CONTENT HERE")
        label.config(fg='black', bg='grey')
        label.place(relx=0.5, rely=0.5, anchor=CENTER)

        frame.protocol('WM_DELETE_WINDOW', self.on_clickx)

    def on_clickx(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()
