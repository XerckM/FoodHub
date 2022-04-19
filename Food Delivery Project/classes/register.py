from tkinter import *
from tkinter import messagebox
import mysql.connector


class Register(object):
    def __init__(self, root):
        self.root = root
        self.fname = StringVar()
        self.lname = StringVar()
        self.uname = StringVar()
        self.email = StringVar()
        self.pword = StringVar()
        self.pword_verify = StringVar()

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

    def reg_frame(self, root):
        # global variables
        global fname_entry, lname_entry, uname_entry, email_entry, pword_entry, rframe

        # hide main window and show TopLevel window first
        rframe = Toplevel(root)

        # set frame width and height
        rframe_width = 300
        rframe_height = 250

        # calculate x and y coordinates for window position in screen
        screen_pos_x = (rframe.winfo_screenwidth() / 2) - (rframe_width / 2)
        screen_pos_y = (rframe.winfo_screenheight() / 2) - (rframe_height / 2)

        # frame title, color, and size
        rframe.title("Register")
        rframe.resizable(False, False)
        rframe.configure(bg='gray12')
        rframe.geometry('%dx%d+%d+%d' % (rframe_width, rframe_height, screen_pos_x, screen_pos_y))

        # first name
        fname_lbl = Label(rframe, text='First Name', bg='gray12', fg='#FFFFFF')
        fname_lbl.place(relx=0.25, rely=0.25, anchor=CENTER)
        fname_entry = Entry(rframe, textvariable=self.fname)
        fname_entry.place(relx=0.65, rely=0.25, anchor=CENTER)

        # last name
        lname_lbl = Label(rframe, text='Last Name', bg='gray12', fg='#FFFFFF')
        lname_lbl.place(relx=0.25, rely=0.35, anchor=CENTER)
        lname_entry = Entry(rframe, textvariable=self.lname)
        lname_entry.place(relx=0.65, rely=0.35, anchor=CENTER)

        # username
        uname_lbl = Label(rframe, text='Username', bg='gray12', fg='#FFFFFF')
        uname_lbl.place(relx=0.25, rely=0.45, anchor=CENTER)
        uname_entry = Entry(rframe, textvariable=self.uname)
        uname_entry.place(relx=0.65, rely=0.45, anchor=CENTER)

        # email address
        email_lbl = Label(rframe, text='Email', bg='gray12', fg='#FFFFFF')
        email_lbl.place(relx=0.25, rely=0.55, anchor=CENTER)
        email_entry = Entry(rframe, textvariable=self.email)
        email_entry.place(relx=0.65, rely=0.55, anchor=CENTER)

        # password
        pword_lbl = Label(rframe, text='Password', bg='gray12', fg='#FFFFFF')
        pword_lbl.place(relx=0.25, rely=0.65, anchor=CENTER)
        pword_entry = Entry(rframe, textvariable=self.pword)
        pword_entry.place(relx=0.65, rely=0.65, anchor=CENTER)

        # verify password
        pword_verify_lbl = Label(rframe, text='Verify Password', bg='gray12', fg='#FFFFFF')
        pword_verify_lbl.place(relx=0.25, rely=0.75, anchor=CENTER)
        pword_verify_entry = Entry(rframe, textvariable=self.pword_verify)
        pword_verify_entry.place(relx=0.65, rely=0.75, anchor=CENTER)

        # register button
        reg_button = Button(rframe, text='Register', width=10, height=1, command=self.register_connect)
        reg_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    def register_connect(self, event=None):
        try:
            fname = fname_entry.get()
            lname = lname_entry.get()
            uname = uname_entry.get()
            email = email_entry.get()
            pword = pword_entry.get()
            if fname == '' or lname == '' or uname == '' or email == '' or pword == '':
                messagebox.showinfo("", "Fields can not be empty!")
            else:
                db = mysql.connector.connect(host='localhost',
                                             user='root',
                                             passwd='Jollyrancher09!',
                                             database='food_delivery')

                query = f'INSERT INTO users (Fname, Lname, Uname, Email, Pword)\n' \
                        f'VALUES ("{fname_entry.get()}", "{lname_entry.get()}", "{uname_entry.get()}", ' \
                        f'"{email_entry.get()}", "{pword_entry.get()}") '
                cursor = db.cursor()
                cursor.execute(query)
                db.commit()
                self.frame_hide(rframe)
                messagebox.showinfo("", "Success!")
        except mysql.connector.errors.ProgrammingError:
            messagebox.showinfo("", "Failed!")