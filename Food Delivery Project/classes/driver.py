from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector

# database connector
sql_db = mysql.connector.connect(host='localhost',
                                 port='3307',
                                 user='root',
                                 passwd='',
                                 database='delivery_database',
                                 buffered=True)
sql_cursor = sql_db.cursor()


class Driver(object):
    def __init__(self, root, identity):
        self.root = root
        self.id = identity
        self.res_menu_var = StringVar()
        self.driver_frame(self.root)

    def driver_frame(self, root):
        global view_table, tree_order_frame, restaurant_menu, view_table, \
            tree_view_frame, view_orders_table

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
        logo.place(relx=0.5, rely=0.08, anchor=CENTER)

        # Output frames
        pickup_frame = Frame(frame)
        pickup_frame.config(width=850, height=565)
        pickup_frame.place(relx=0.51, rely=0.55, anchor=CENTER)
        pickup_frame.grid_propagate(False)

        profile_frame = Frame('')
        profile_frame.config(width=850, height=565)
        profile_frame.place(relx=0.61, rely=0.55, anchor=CENTER)
        profile_frame.grid_propagate(False)

        # pickup frame activities

        tree_view_frame = Frame(pickup_frame)
        tree_view_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        tree_view_scroll = Scrollbar(tree_view_frame)
        tree_view_scroll.pack(side=RIGHT, fill=Y)

        view_orders_table = ttk.Treeview(tree_view_frame, selectmode='extended')
        view_orders_table.config(columns=("1", "2", "3", "4", "5", "6"), show='headings',
                                 yscrollcommand=tree_view_scroll.set)
        tree_view_scroll.config(command=view_orders_table.yview)
        view_orders_table.pack()
        view_orders_table.column("1", width=80, anchor='c')
        view_orders_table.column("2", width=80, anchor='c')
        view_orders_table.column("3", width=130, anchor='c')
        view_orders_table.column("4", width=130, anchor='c')
        view_orders_table.column("5", width=130, anchor='c')
        view_orders_table.column("6", width=130, anchor='c')
        view_orders_table.heading("1", text="Order Id")
        view_orders_table.heading("2", text="First Name")
        view_orders_table.heading("3", text="Last Name")
        view_orders_table.heading("4", text="Street")
        view_orders_table.heading("5", text="City")
        view_orders_table.heading("6", text="State")

        refresh_orders_button = Button(pickup_frame, command=self.refresh_button)
        refresh_orders_button.config(text='Refresh', width=33)
        refresh_orders_button.place(relx=0.355, rely=0.75)

        pickup_orders_button = Button(pickup_frame, command=self.pickup_orders)
        pickup_orders_button.config(text='Pickup', width=33)
        pickup_orders_button.place(relx=0.355, rely=0.8)

        delivered_button = Button(pickup_frame, command=self.delivered_order)
        delivered_button.config(text='Delivered', width=33)
        delivered_button.place(relx=0.355, rely=0.85)

        # Buttons

        pickup_button = Button('', command=lambda: self.show_frame(pickup_frame))
        pickup_button.config(text='Pickup Order', width=33, height=7, relief='flat', bg='#ff5900',
                            activebackground='#c75610', fg='white')
        pickup_button.bind('<Enter>', lambda event: self.button_on_hover(pickup_button, event))
        pickup_button.bind('<Leave>', lambda event: self.button_off_hover(pickup_button, event))
        pickup_button.place(relx=0, rely=0.159)

        profile_button = Button('', command=lambda: self.show_frame(profile_frame))
        profile_button.config(text='Edit Profile', width=33, height=7, relief='flat', bg='#ff5900',
                              activebackground='#c75610', fg='white')
        profile_button.bind('<Enter>', lambda event: self.button_on_hover(profile_button, event))
        profile_button.bind('<Leave>', lambda event: self.button_off_hover(profile_button, event))
        profile_button.place(relx=0, rely=0.32)

        self.show_frame(pickup_frame)

        frame.protocol('WM_DELETE_WINDOW', self.on_clickx)

    @staticmethod
    def pickup_orders(event=None):
        try:
            item_list = None
            for dt in view_orders_table.selection():
                item_list = view_orders_table.item(dt, 'values')
            order_id = item_list[0]
            picked_up_query = "UPDATE orderstatus SET oStatus = 'On the way' WHERE orderstatus.orderId = %s"
            sql_cursor.execute(picked_up_query, [order_id])
            sql_db.commit()
            messagebox.showinfo("", "Order updated!")
        except BaseException:
            messagebox.showinfo("", "Something went wrong!")

    @staticmethod
    def delivered_order(event=None):
        try:
            item_list = None
            for dt in view_orders_table.selection():
                item_list = view_orders_table.item(dt, 'values')
            order_id = item_list[0]
            picked_up_query = "UPDATE orderstatus SET oStatus = 'Delivered' WHERE orderstatus.orderId = %s"
            sql_cursor.execute(picked_up_query, [order_id])
            sql_db.commit()

            messagebox.showinfo("", "Order updated!")
        except BaseException:
            messagebox.showinfo("", "Something went wrong!")

    @staticmethod
    def refresh_button(event=None):
        view_orders_table.delete(*view_orders_table.get_children())
        tree_view_frame.update()

        view_order_query = "SELECT orders.orderId, person.fname, person.lname, customer.Street, customer.City, " \
                           "customer.state FROM orders INNER JOIN person INNER JOIN customer WHERE orders.customerId " \
                           "= customer.customerId AND customer.Cssn = person.Ssn"
        sql_cursor.execute(view_order_query)
        table_items = sql_cursor.fetchall()

        for dt in table_items:
            view_orders_table.insert(parent='', index='end', values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]))

    def on_clickx(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    @staticmethod
    def view_res_food_table(event=None):
        view_table.delete(*view_table.get_children())
        tree_order_frame.update()

        table_var = restaurant_menu.get()
        get_all_food = "SELECT foodId, foodName, calories, price, food.menuId FROM food, menu WHERE " \
                       "food.menuId = menu.menuId AND menu.restaurantId = (SELECT restaurant.restaurantId FROM " \
                       "restaurant WHERE restaurant.resName = %s)"
        sql_cursor.execute(get_all_food, [table_var])
        table_items = sql_cursor.fetchall()

        for dt in table_items:
            view_table.insert(parent='', index='end', iid=dt[0], values=(dt[0], dt[1], dt[2], dt[3], dt[4]))

    @staticmethod
    def show_frame(frame):
        frame.tkraise()

    @staticmethod
    def button_on_hover(button, event=None):
        button['background'] = '#FF9D00'

    @staticmethod
    def button_off_hover(button, event=None):
        if button['text'] in ('Order Food', 'Edit Profile'):
            button['background'] = '#ff5900'
        else:
            button['background'] = '#FF8000'
