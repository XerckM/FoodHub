from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from classes.admin import Admin
import mysql.connector


class Login(object):
    def __init__(self, root):
        self.root = root
        self.user = StringVar()
        self.pwd = StringVar()
        self.login_frame(root)

    def login_frame(self, root):
        """
        Creates the login window for database login
        """

        # global variables
        global user_entry, pwd_entry, frame, log_button

        # top level frame and window icon
        frame = Toplevel(root)
        frame.iconbitmap('win_ico.ico')

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
        rlbl_frame = LabelFrame(frame, width=240, height=360, bg='white', relief='flat')
        rlbl_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # logo
        load = Image.open('logo.png').resize((210, 100), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        logo = Label(rlbl_frame, image=render, relief='flat', bg='white')
        logo.image = render
        logo.place(relx=0.5, rely=0.2, anchor=CENTER)

        # username entry box
        user_entry = Entry(rlbl_frame, textvariable=self.user, fg='grey', borderwidth=2)
        user_entry.insert(0, "Username")
        user_entry.place(relx=0.5, rely=0.45, anchor=CENTER)
        user_entry.bind('<FocusIn>', self.user_entry_onclick)
        user_entry.bind('<FocusOut>', self.user_entry_focusout)

        # password entry box
        pwd_entry = Entry(rlbl_frame, textvariable=self.pwd, fg='grey', borderwidth=2)
        pwd_entry.insert(0, 'Password')
        pwd_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
        pwd_entry.bind('<FocusIn>', self.pwd_entry_onclick)
        pwd_entry.bind('<FocusOut>', self.pwd_entry_focusout)

        # login button
        log_button = Button(rlbl_frame, command=self.login_connect)
        log_button.config(text='Login', width=10, height=1, relief='flat', bg='green', fg='white')
        log_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        close = Label(frame, text='Cancel', cursor='hand2', bg='white')
        close.config(fg='blue')
        close.place(relx=0.5, rely=0.701, anchor=CENTER)
        close.bind('<Button-1>', lambda event: self.on_clickx(event))

        # Copyright label
        cr = Label(frame, text='Copyright © 2022 FoodHub Inc.', bg='#FF8000', fg='white')
        cr.place(relx=0.5, rely=0.94, anchor=CENTER)

        frame.bind('<Return>', lambda event: self.login_connect(event))
        frame.protocol('WM_DELETE_WINDOW', self.on_clickx)
        # frame.overrideredirect(True)

    def login_connect(self, event=None):
        """
        Event that initiates when logging in the database
        """
        try:
            sql_db = mysql.connector.connect(host='localhost',
                                             user='root',
                                             passwd='password',
                                             database='food_delivery')
            uname = user_entry.get()
            pword = pwd_entry.get()
            sql_cursor = sql_db.cursor()
            user_query = "SELECT * FROM users WHERE Uname = %s and Pword = %s"
            sql_cursor.execute(user_query, [uname, pword])
            result = sql_cursor.fetchall()
            user_level = str([res[0] for res in result]).strip('[]')
            if result:
                messagebox.showinfo("", "Login Successful!")
                frame.destroy()
                if user_level == '1':
                    return Admin(self.root, uname, pword)
                else:
                    print("No")
            else:
                messagebox.showinfo("Error!", "Incorrect username or password.")
        except mysql.connector.errors.ProgrammingError:
            messagebox.showinfo("Error!", "Incorrect username or password.")
            return False

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

    def on_clickx(self, even=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()
