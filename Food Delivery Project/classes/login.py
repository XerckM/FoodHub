from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from classes.admin import Admin
from classes.customer import Customer
from classes.restaurant import Restaurant
from classes.driver import Driver
import mysql.connector

# database connector
sql_db = mysql.connector.connect(host='localhost',
                                 port='3307',
                                 user='root',
                                 passwd='',
                                 database='delivery_database')
sql_cursor = sql_db.cursor()


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
        frame_width = 320
        frame_height = 460

        # calculate x and y coordinates for window position in screen
        screen_pos_x = (frame.winfo_screenwidth() / 2) - (frame_width / 2)
        screen_pos_y = (frame.winfo_screenheight() / 2) - (frame_height / 2)

        # frame title, color, and size
        frame.title("Login")
        frame.resizable(False, False)
        frame.configure(bg='#FF8000')
        frame.geometry('%dx%d+%d+%d' % (frame_width, frame_height, screen_pos_x, screen_pos_y))

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
        user_entry = Entry(rlbl_frame, textvariable=self.user, fg='grey')
        user_entry.config(relief='flat', highlightcolor='grey',
                          highlightbackground='grey', highlightthickness=2)
        user_entry.insert(0, "Username")
        user_entry.place(relx=0.5, rely=0.45, anchor=CENTER)
        user_entry.bind('<FocusIn>', self.user_entry_onclick)
        user_entry.bind('<FocusOut>', self.user_entry_focusout)

        # password entry box
        pwd_entry = Entry(rlbl_frame, textvariable=self.pwd, fg='grey')
        pwd_entry.config(relief='flat', highlightcolor='grey',
                         highlightbackground='grey', highlightthickness=2)
        pwd_entry.insert(0, 'Password')
        pwd_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
        pwd_entry.bind('<FocusIn>', self.pwd_entry_onclick)
        pwd_entry.bind('<FocusOut>', self.pwd_entry_focusout)

        # login button
        log_button = Button(rlbl_frame, command=self.login_connect)
        log_button.config(text='Login', width=17, height=1, relief='flat', bg='green', fg='white')
        log_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        create_customer_label = Label(frame, text='Not an existing customer?', bg='white')
        create_customer_label.place(relx=0.5, rely=0.75, anchor=CENTER)

        create_customer = Label(frame, text='Create an account', cursor='hand2', bg='white')
        create_customer.config(fg='blue')
        create_customer.place(relx=0.49, rely=0.79, anchor=CENTER)
        create_customer.bind('<Button-1>', lambda event: self.sign_up(event))

        frame.bind('<Return>', lambda event: self.login_connect(event))
        frame.protocol('WM_DELETE_WINDOW', self.on_clickx)
        # frame.overrideredirect(True)

    def create_customer_frame(self, root):
        global new_user_entry, new_pword_entry, new_fname_entry, \
               new_lname_entry, new_month_entry, new_day_entry, \
               new_year_entry, new_ssn_entry, new_email_entry, \
               new_address_entry, new_city_entry, new_state_entry, new_phone_entry, cframe

        cframe = Toplevel(root)
        frame.iconbitmap('win_ico.ico')

        # set frame width and height
        frame_width = 360
        frame_height = 480

        # calculate x and y coordinates for window position in screen
        screen_pos_x = (cframe.winfo_screenwidth() / 2) - (frame_width / 2)
        screen_pos_y = (cframe.winfo_screenheight() / 2) - (frame_height / 2)

        # frame title, color, and size
        cframe.title("Login")
        cframe.resizable(False, False)
        cframe.configure(bg='#FF8000')
        cframe.geometry('%dx%d+%d+%d' % (frame_width, frame_height, screen_pos_x, screen_pos_y))

        new_uname_label = Label(cframe)
        new_uname_label.config(text="Enter Username", bg='#FF8000')
        new_uname_label.place(relx=0.15, rely=0.2, anchor='w')

        new_pword_label = Label(cframe)
        new_pword_label.config(text="Enter Password", bg='#FF8000')
        new_pword_label.place(relx=0.15, rely=0.25, anchor='w')

        new_fname_label = Label(cframe)
        new_fname_label.config(text="First Name", bg='#FF8000')
        new_fname_label.place(relx=0.15, rely=0.3, anchor='w')

        new_lname_label = Label(cframe)
        new_lname_label.config(text="Last Name", bg='#FF8000')
        new_lname_label.place(relx=0.15, rely=0.35, anchor='w')

        new_dob_label = Label(cframe)
        new_dob_label.config(text="Date of Birth", bg='#FF8000')
        new_dob_label.place(relx=0.15, rely=0.4, anchor='w')

        new_ssn_label = Label(cframe)
        new_ssn_label.config(text="Enter Ssn", bg='#FF8000')
        new_ssn_label.place(relx=0.15, rely=0.45, anchor='w')

        new_email_label = Label(cframe)
        new_email_label.config(text="Enter Email", bg='#FF8000')
        new_email_label.place(relx=0.15, rely=0.5, anchor='w')

        new_address_label = Label(cframe)
        new_address_label.config(text="Enter Address", bg='#FF8000')
        new_address_label.place(relx=0.15, rely=0.55, anchor='w')

        new_city_label = Label(cframe)
        new_city_label.config(text="Enter City", bg='#FF8000')
        new_city_label.place(relx=0.15, rely=0.6, anchor='w')

        new_state_label = Label(cframe)
        new_state_label.config(text="Enter State", bg='#FF8000')
        new_state_label.place(relx=0.15, rely=0.65, anchor='w')

        new_phone_label = Label(cframe)
        new_phone_label.config(text="Enter Phone", bg='#FF8000')
        new_phone_label.place(relx=0.15, rely=0.7, anchor='w')

        new_user_entry = Entry(cframe)
        new_user_entry.config(bg='white')
        new_user_entry.place(relx=0.5, rely=0.18)

        new_pword_entry = Entry(cframe)
        new_pword_entry.config(bg='white')
        new_pword_entry.place(relx=0.5, rely=0.23)

        new_fname_entry = Entry(cframe)
        new_fname_entry.config(bg='white')
        new_fname_entry.place(relx=0.5, rely=0.28)

        new_lname_entry = Entry(cframe)
        new_lname_entry.config(bg='white')
        new_lname_entry.place(relx=0.5, rely=0.33)

        new_month_entry = Entry(cframe)
        new_month_entry.insert(0, 'MM')
        new_month_entry.config(fg='grey', bg='white', width=5)
        new_month_entry.place(relx=0.5, rely=0.38)

        new_day_entry = Entry(cframe)
        new_day_entry.insert(0, 'DD')
        new_day_entry.config(fg='grey', bg='white', width=5)
        new_day_entry.place(relx=0.6, rely=0.38)

        new_year_entry = Entry(cframe)
        new_year_entry.insert(0, 'YYYY')
        new_year_entry.config(fg='grey', bg='white', width=8)
        new_year_entry.place(relx=0.7, rely=0.38)

        new_ssn_entry = Entry(cframe)
        new_ssn_entry.config(bg='white')
        new_ssn_entry.place(relx=0.5, rely=0.43)

        new_email_entry = Entry(cframe)
        new_email_entry.config(bg='white')
        new_email_entry.place(relx=0.5, rely=0.48)

        new_address_entry = Entry(cframe)
        new_address_entry.config(bg='white')
        new_address_entry.place(relx=0.5, rely=0.53)

        new_city_entry = Entry(cframe)
        new_city_entry.config(bg='white')
        new_city_entry.place(relx=0.5, rely=0.58)

        new_state_entry = Entry(cframe)
        new_state_entry.config(bg='white')
        new_state_entry.place(relx=0.5, rely=0.63)

        new_phone_entry = Entry(cframe)
        new_phone_entry.config(bg='white')
        new_phone_entry.place(relx=0.5, rely=0.68)

        register_button = Button(cframe, command=self.register_account_button)
        register_button.config(text='Register', width=25)
        register_button.place(relx=0.25, rely=0.83)

        cframe.protocol('WM_DELETE_WINDOW', lambda: self.on_clickx_create(cframe))

    def sign_up(self, event=None):
        return self.create_customer_frame(self.root)

    @staticmethod
    def register_account_button(event=None):
        user = new_user_entry.get()
        pword = new_pword_entry.get()
        fname = new_fname_entry.get()
        lname = new_lname_entry.get()
        month = new_month_entry.get()
        day = new_day_entry.get()
        year = new_year_entry.get()
        ssn = new_ssn_entry.get()
        email = new_email_entry.get()
        address = new_address_entry.get()
        city = new_city_entry.get()
        state = new_state_entry.get()
        phone = new_phone_entry.get()

        try:
            if (user, pword, fname, lname, month, day, year, ssn, email, address, city, state, phone) != "":
                insert_user_query = "INSERT INTO users (uname, pword, perm) " \
                                     "VALUES (%s, %s, 'customer')"
                sql_cursor.execute(insert_user_query, [user, pword])
                sql_db.commit()

                insert_person_query = f'INSERT INTO person (fname, lname, email, Ssn, Bod, P_uid)' \
                                      f'VALUES (%s, %s, %s, %s, "{year}-{month}-{day}", ' \
                                      f'(SELECT Uid FROM users WHERE Uname = %s))'
                sql_cursor.execute(insert_person_query, [fname, lname, email, ssn, user])
                sql_db.commit()

                insert_cus_query = "INSERT INTO customer (Cssn, Street, City, State, Phone, dateJoined) " \
                                   "VALUES (%s, %s, %s, %s, %s, (CURDATE()))"
                sql_cursor.execute(insert_cus_query, [ssn, address, city, state, phone])
                sql_db.commit()

                new_user_entry.delete(0, END)
                new_pword_entry.delete(0, END)
                new_fname_entry.delete(0, END)
                new_lname_entry.delete(0, END)
                new_month_entry.delete(0, END)
                new_day_entry.delete(0, END)
                new_year_entry.delete(0, END)
                new_ssn_entry.delete(0, END)
                new_email_entry.delete(0, END)
                new_address_entry.delete(0, END)
                new_city_entry.delete(0, END)
                new_state_entry.delete(0, END)
                new_phone_entry.delete(0, END)

                messagebox.showinfo("", "Successfully Added!")
                cframe.destroy()
        except BaseException:
            messagebox.showinfo("", "Failed to Add!")

    def login_connect(self, event=None):
        """
        Event that initiates when logging in the database
        """
        try:
            uname = user_entry.get()
            pword = pwd_entry.get()
            user_query = "SELECT Uname, Pword FROM users WHERE Uname = %s AND Pword = %s"
            sql_cursor.execute(user_query, [uname, pword])
            result = sql_cursor.fetchall()
            if result:
                messagebox.showinfo("", "Login Successful!")
                frame.destroy()
                permission_query = "SELECT Perm FROM users WHERE Uname = %s AND Pword = %s"
                sql_cursor.execute(permission_query, [uname, pword])
                permission = sql_cursor.fetchone()
                if permission[0] == "admin":
                    return Admin(self.root)
                elif permission[0] == "manage":
                    owner_id_query = f'SELECT restowner.ownerId from restowner, users where users.Uname = %s AND ' \
                                     f'restowner.Ossn = (SELECT Ssn from person where person.P_uid = users.Uid);'
                    sql_cursor.execute(owner_id_query, [uname])
                    owner_id = sql_cursor.fetchone()
                    print(owner_id[0])
                    return Restaurant(self.root, owner_id[0])
                elif permission[0] == "driver":
                    driver_id_query = "SELECT driver.driverId FROM driver, users WHERE users.Uname = %s AND " \
                                   "driver.dSsn = (SELECT Ssn FROM person WHERE person.P_uid = users.Uid)"
                    sql_cursor.execute(driver_id_query, [uname])
                    driver_id = sql_cursor.fetchone()
                    print(driver_id[0])
                    return Driver(self.root, driver_id[0])
                else:
                    cus_id_query = "SELECT customer.customerId FROM customer, users WHERE users.Uname = %s AND " \
                                   "customer.Cssn = (SELECT Ssn FROM person WHERE person.P_uid = users.Uid)"
                    sql_cursor.execute(cus_id_query, [uname])
                    cus_id = sql_cursor.fetchone()
                    print(cus_id[0])
                    return Customer(self.root, cus_id[0])
            else:
                messagebox.showinfo("Error!", "Incorrect username or password.")
        except mysql.connector.errors.InterfaceError:
            messagebox.showinfo("Error!", "Something wrong happened.")
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

    def on_clickx(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    @staticmethod
    def on_clickx_create(iframe, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            iframe.destroy()
