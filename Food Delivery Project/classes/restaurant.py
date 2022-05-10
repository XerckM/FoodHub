from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector


class Restaurant(object):
    global sql_db
    # database connector
    sql_db = mysql.connector.connect(host='localhost',
                                     port='3307',
                                     user='root',
                                     passwd='',
                                     database='food_delivery')

    def __init__(self, root):
        self.root = root
        self.name = StringVar()
        self.price = StringVar()
        self.max_quantity = StringVar()
        self.menu_var = StringVar()
        self.restaurant_frame(self.root)

    def restaurant_frame(self, root):
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
        frame.configure(bg='white')
        frame.geometry('%dx%d+%d+%d' % (frame_width, frame_height, screen_pos_x, screen_pos_y))

        # TODO: Add content below here

        load = Image.open('logo.png').resize((210, 100), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        logo = Label(frame, image=render, relief='flat', bg='white')
        logo.image = render
        logo.place(anchor=CENTER)
        logo.grid(row=0, column=0, columnspan=2)

        # Output frames
        add_frame = Frame(frame)
        add_frame.config(width=850, height=565)
        add_frame.grid_propagate(False)
        add_frame.grid(row=1, column=1, rowspan=5)

        remove_frame = Frame(frame)
        remove_frame.config(width=850, height=565)
        remove_frame.grid_propagate(False)
        remove_frame.grid(row=1, column=1, rowspan=5)

        modify_frame = Frame(frame)
        modify_frame.config(width=850, height=565)
        modify_frame.grid(row=1, column=1, rowspan=5)
        modify_frame.grid_propagate(False)

        profile_frame = Frame(frame)
        profile_frame.config(width=850, height=565)
        profile_frame.grid(row=1, column=1, rowspan=5)
        profile_frame.grid_propagate(False)

        view_menu_frame = Frame(frame)
        view_menu_frame.config(width=850, height=565)
        view_menu_frame.grid(row=1, column=1, rowspan=5)
        view_menu_frame.grid_propagate(False)

        self.show_frame(add_frame)

        # add frame activities

        name_label = Label(add_frame)
        name_label.config(text="Name")
        name_label.place(relx=0.35, rely=0.3, anchor=CENTER)

        price_label = Label(add_frame)
        price_label.config(text="Price")
        price_label.place(relx=0.35, rely=0.4, anchor=CENTER)

        max_quantity_label = Label(add_frame)
        max_quantity_label.config(text="Max Quantity")
        max_quantity_label.place(relx=0.35, rely=0.5, anchor=CENTER)

        menu_label = Label(add_frame)
        menu_label.config(text="Menu")
        menu_label.place(relx=0.35, rely=0.6, anchor=CENTER)

        name_entry = Entry(add_frame, textvariable=self.name)
        name_entry.config(width=30)
        name_entry.place(relx=0.55, rely=0.3, anchor=CENTER)

        price_entry = Entry(add_frame, textvariable=self.price)
        price_entry.config(width=30)
        price_entry.place(relx=0.55, rely=0.4, anchor=CENTER)

        max_quantity_entry = Entry(add_frame, textvariable=self.max_quantity)
        max_quantity_entry.config(width=30)
        max_quantity_entry.place(relx=0.55, rely=0.5, anchor=CENTER)

        menu_list = ["Menu 1", "Menu 2", "Menu 3"]
        menu_option = ttk.Combobox(add_frame, textvariable=self.menu_var, state='readonly')
        menu_option.config(width=27, justify=CENTER)
        menu_option.set('---------Select Menu---------')
        menu_option['value'] = [item for item in menu_list]
        menu_option.place(relx=0.55, rely=0.6, anchor=CENTER)

        add_frame_button = Button(add_frame, command=self.add)
        add_frame_button.config(text='Add Item', width=33)
        add_frame_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        # remove frame activities

        table_query = "SELECT * FROM food LIMIT 0, 10"
        sql_cursor = sql_db.cursor()
        table = sql_cursor.execute(table_query)

        view_table = ttk.Treeview(remove_frame, selectmode='extended')
        view_table.place(relx=0.5, rely=0.5, anchor=CENTER)
        view_table['columns'] = ("1", "2", "3", "4", "5")
        view_table['show'] = 'headings'
        view_table.column("1", width=100, anchor='c')
        view_table.column("2", width=100, anchor='c')
        view_table.column("3", width=100, anchor='c')
        view_table.column("4", width=100, anchor='c')
        view_table.column("5", width=100, anchor='c')

        remove_frame_button = Button(remove_frame)
        remove_frame_button.config(text='Remove', width=33)
        remove_frame_button.place(relx=0.355, rely=0.75)

        # Buttons

        add_button = Button(frame, command=lambda: self.show_frame(add_frame))
        add_button.config(text='Add Food', width=33, height=6, relief='flat', bg='#ff5900',
                          activebackground='#c75610', fg='white')
        add_button.bind('<Enter>', lambda event: self.button_on_hover(add_button, event))
        add_button.bind('<Leave>', lambda event: self.button_off_hover(add_button, event))
        add_button.grid(row=1, column=0)

        remove_button = Button(frame, command=lambda: self.show_frame(remove_frame))
        remove_button.config(text='Remove Food', width=33, height=7, relief='flat', bg='#FF8000',
                             activebackground='#c75610', fg='white')
        remove_button.bind('<Enter>', lambda event: self.button_on_hover(remove_button, event))
        remove_button.bind('<Leave>', lambda event: self.button_off_hover(remove_button, event))
        remove_button.grid(row=2, column=0)

        modify_button = Button(frame, command=lambda: self.show_frame(modify_frame))
        modify_button.config(text='Modify Food', width=33, height=7, relief='flat', bg='#ff5900',
                             activebackground='#c75610', fg='white')
        modify_button.bind('<Enter>', lambda event: self.button_on_hover(modify_button, event))
        modify_button.bind('<Leave>', lambda event: self.button_off_hover(modify_button, event))
        modify_button.grid(row=3, column=0)

        profile_button = Button(frame, command=lambda: self.show_frame(profile_frame))
        profile_button.config(text='Edit Profile', width=33, height=7, relief='flat', bg='#FF8000',
                              activebackground='#c75610', fg='white')
        profile_button.bind('<Enter>', lambda event: self.button_on_hover(profile_button, event))
        profile_button.bind('<Leave>', lambda event: self.button_off_hover(profile_button, event))
        profile_button.grid(row=4, column=0)

        view_menu_button = Button(frame, command=lambda: self.show_frame(view_menu_frame))
        view_menu_button.config(text='View Current Menu', width=33, height=7, relief='flat', bg='#ff5900',
                                activebackground='#c75610', fg='white')
        view_menu_button.bind('<Enter>', lambda event: self.button_on_hover(view_menu_button, event))
        view_menu_button.bind('<Leave>', lambda event: self.button_off_hover(view_menu_button, event))
        view_menu_button.grid(row=5, column=0)

        frame.protocol('WM_DELETE_WINDOW', self.on_clickx)

    def add(self, event=None):
        try:
            name = self.name.get()
            quantity = self.max_quantity.get()
            price = self.price.get()
            if name == "" and quantity == "" and price == "":
                messagebox.showinfo("", "Values can not be empty")
            else:
                sql_cursor = sql_db.cursor()
                add_query = "INSERT INTO `food`(`name`, `quantity`, `unitPrice`) " \
                            "VALUES (%s, %s, %s)"
                sql_cursor.execute(add_query, [name, quantity, price])
                sql_db.commit()
                messagebox.showinfo("", "Added!")
        except BaseException:
            messagebox.showinfo("", "Failed to add!")

    def on_clickx(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    @staticmethod
    def show_frame(frame):
        frame.tkraise()

    @staticmethod
    def button_on_hover(button, event=None):
        button['background'] = '#FF9D00'

    @staticmethod
    def button_off_hover(button, event=None):
        if button['text'] in ('Add Food', 'Modify Food', 'View Current Menu'):
            button['background'] = '#ff5900'
        else:
            button['background'] = '#FF8000'
