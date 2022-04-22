from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import sys
import os


class Login(object):
    def __init__(self, root, user, pwd):
        self.root = root
        self.user = user
        self.pwd = pwd
        self.login_frame(root)

    @staticmethod
    def frame_hide(fr):
        """
        hides window
        """
        fr.withdraw()

    @staticmethod
    def frame_show(fr):
        """
        shows window
        """
        fr.deiconify()

    def login_frame(self, root):
        """
        Creates the login window for database login
        """

        # global variables for login_connect
        global user_entry
        global pwd_entry
        global frame

        # hide main window and show TopLevel window first
        self.frame_hide(root)
        frame = Toplevel(root)

        # set frame width and height
        lframe_width = 360
        lframe_height = 480

        # calculate x and y coordinates for window position in screen
        screen_pos_x = (frame.winfo_screenwidth() / 2) - (lframe_width / 2)
        screen_pos_y = (frame.winfo_screenheight() / 2) - (lframe_height / 2)

        # frame title, color, and size
        frame.title("Login")
        frame.resizable(False, False)
        frame.configure(bg='#FF8000')
        frame.geometry('%dx%d+%d+%d' % (lframe_width, lframe_height, screen_pos_x, screen_pos_y))

        # inner frame
        rlbl_frame = LabelFrame(frame, width=230, height=340, bg='white', relief='flat')
        rlbl_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # logo
        load = Image.open('logo.png').resize((210, 100), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        logo = Label(rlbl_frame, image=render, relief='flat', bg='white')
        logo.image = render
        logo.place(relx=0.5, rely=0.15, anchor=CENTER)

        # username entry box
        user_entry = Entry(rlbl_frame, textvariable=self.user, fg='grey')
        user_entry.insert(0, "Username")
        user_entry.place(relx=0.5, rely=0.45, anchor=CENTER)
        user_entry.bind('<FocusIn>', self.user_entry_onclick)
        user_entry.bind('<FocusOut>', self.user_entry_focusout)

        # password entry box
        pwd_entry = Entry(rlbl_frame, textvariable=self.pwd, fg='grey')
        pwd_entry.insert(0, 'Password')
        pwd_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
        pwd_entry.bind('<FocusIn>', self.pwd_entry_onclick)
        pwd_entry.bind('<FocusOut>', self.pwd_entry_focusout)

        # login button
        log_button = Button(rlbl_frame, text='Login', width=10, height=1, command=self.login_connect)
        log_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        frame.bind('<Return>', lambda event: self.login_connect(event))

    def login_connect(self, event=None):
        """
        Event that initiates when logging in the database
        """
        try:
            db = mysql.connector.connect(host='localhost',
                                         user=user_entry.get(),
                                         passwd=pwd_entry.get(),
                                         database='food_delivery')
            if db:
                messagebox.showinfo("Login", "Login Successful!")
                self.frame_hide(frame)
                self.frame_show(self.root)
                self.root.state('zoomed')
        except mysql.connector.errors.ProgrammingError:
            messagebox.showinfo("Error!", "Incorrect username or password.")

    @staticmethod
    def user_entry_onclick(event):
        if user_entry.get() == 'Username':
            user_entry.delete(0, "end")
            user_entry.insert(0, '')
            user_entry.config(fg='black')

    @staticmethod
    def user_entry_focusout(event):
        if user_entry.get() == '':
            user_entry.insert(0, 'Username')
            user_entry.config(fg='grey')

    @staticmethod
    def pwd_entry_onclick(event):
        if pwd_entry.get() == 'Password':
            pwd_entry.delete(0, 'end')
            pwd_entry.insert(0, '')
            pwd_entry.config(fg='black', show='*')

    @staticmethod
    def pwd_entry_focusout(event):
        if user_entry.get() == '':
            user_entry.insert(0, 'Password')
            user_entry.config(fg='grey')