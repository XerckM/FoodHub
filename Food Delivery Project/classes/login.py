from tkinter import *
from tkinter import messagebox
import mysql.connector


class Login:
    def __init__(self, root):
        self.root = root
        self.user = StringVar()
        self.pwd = StringVar()
        self.login_frame()

    def login_frame(self):
        """
        Creates the login window for database login
        """
        global user_entry
        global pwd_entry
        frame = self.root

        # set frame width and height
        lframe_width = 300
        lframe_height = 250

        # calculate x and y coordinates for Tk window position in screen
        pos_x = (frame.winfo_screenwidth()/2) - (lframe_width/2)
        pos_y = (frame.winfo_screenheight()/2) - (lframe_height/2)

        frame.title("Login Food Delivery")
        frame.resizable(FALSE, FALSE)
        frame.configure(bg='gray12')
        frame.geometry('%dx%d+%d+%d' % (lframe_width, lframe_height, pos_x, pos_y))     # set dimensions of frame

        # username entry box
        user_label = Label(frame, text='Username', bg='gray12', fg='#FFFFFF')
        user_label.place(relx=0.5, rely=0.25, anchor=CENTER)
        user_entry = Entry(frame, textvariable=self.user)
        user_entry.place(relx=0.5, rely=0.35, anchor=CENTER)

        # password entry box
        pwd_label = Label(frame, text='Password', bg='gray12', fg='#FFFFFF')
        pwd_label.place(relx=0.5, rely=0.45, anchor=CENTER)
        pwd_entry = Entry(frame, textvariable=self.pwd)
        pwd_entry.config(show="*")
        pwd_entry.place(relx=0.5, rely=0.55, anchor=CENTER)

        # login button
        log_button = Button(frame, text='Login', width=10, height=1, command=self.login_connect)
        log_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        frame.bind('<Return>', lambda event: self.login_connect(event))

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
                self.root.withdraw()
                return True
        except mysql.connector.errors.ProgrammingError:
            messagebox.showinfo("Error!", "Incorrect username or password.")
            return False
