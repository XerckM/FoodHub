from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import CENTER
from tkinter import Button
from tkinter import messagebox
import mysql.connector


class Login(object):
    def __init__(self, root, user, pwd):
        self.root = root
        self.main_frame_hide()
        self.frame = Toplevel(self.root)
        self.user = user
        self.pwd = pwd
        self.login_frame()

    def main_frame_hide(self):
        self.root.withdraw()

    def main_frame_show(self):
        self.root.deiconify()

    def login_frame(self):
        """
        Creates the login window for database login
        """
        global user_entry
        global pwd_entry

        # set frame width and height
        lframe_width = 300
        lframe_height = 250

        # calculate x and y coordinates for Tk window position in screen
        screen_pos_x = (self.frame.winfo_screenwidth()/2) - (lframe_width/2)
        screen_pos_y = (self.frame.winfo_screenheight()/2) - (lframe_height/2)

        self.frame.title("Login Food Delivery")
        self.frame.resizable(False, False)
        self.frame.configure(bg='gray12')
        self.frame.geometry('%dx%d+%d+%d' % (lframe_width, lframe_height, screen_pos_x, screen_pos_y))

        # username entry box
        user_label = Label(self.frame, text='Username', bg='gray12', fg='#FFFFFF')
        user_label.place(relx=0.5, rely=0.25, anchor=CENTER)
        user_entry = Entry(self.frame, textvariable=self.user)
        user_entry.place(relx=0.5, rely=0.35, anchor=CENTER)

        # password entry box
        pwd_label = Label(self.frame, text='Password', bg='gray12', fg='#FFFFFF')
        pwd_label.place(relx=0.5, rely=0.45, anchor=CENTER)
        pwd_entry = Entry(self.frame, textvariable=self.pwd)
        pwd_entry.config(show="*")
        pwd_entry.place(relx=0.5, rely=0.55, anchor=CENTER)

        # login button
        log_button = Button(self.frame, text='Login', width=10, height=1, command=self.login_connect)
        log_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.frame.bind('<Return>', lambda event: self.login_connect(event))

    def login_connect(self, event=None):
        """
        Event that initiates when logging in the database
        """
        self.user = user_entry.get()
        self.pwd = pwd_entry.get()

        try:
            db = mysql.connector.connect(host='localhost',
                                         user=self.user,
                                         passwd=self.pwd,
                                         database='food_delivery')
            if db:
                messagebox.showinfo("Login", "Login Successful!")
                self.frame.withdraw()
                self.main_frame_show()
        except mysql.connector.errors.ProgrammingError:
            messagebox.showinfo("Error!", "Incorrect username or password.")
