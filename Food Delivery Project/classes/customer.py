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


class Customer(object):
    def __init__(self, root, identity):
        self.root = root
        self.id = identity
        self.res_menu_var = StringVar()
        self.customer_frame(self.root)

    def customer_frame(self, root):
        global view_table, tree_order_frame, restaurant_menu, view_table, \
            tree_view_order_frame, view_order_table, pay_frame, total_entry, pay_name_entry, \
            credit_card_entry, exp_date_entry, sec_code_entry, order_frame, view_order_status_frame, \
            tree_view_order_status_frame, view_order_status_table

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
        order_frame = Frame(frame)
        order_frame.config(width=850, height=565)
        order_frame.place(relx=0.61, rely=0.55, anchor=CENTER)
        order_frame.grid_propagate(False)

        view_order_status_frame = Frame(frame)
        view_order_status_frame.config(width=850, height=565)
        view_order_status_frame.place(relx=0.61, rely=0.55, anchor=CENTER)
        view_order_status_frame.grid_propagate(False)

        profile_frame = Frame('')
        profile_frame.config(width=850, height=565)
        profile_frame.place(relx=0.61, rely=0.55, anchor=CENTER)
        profile_frame.grid_propagate(False)

        pay_frame = Frame(frame)
        pay_frame.config(width=850, height=565)
        pay_frame.place(relx=0.61, rely=0.55, anchor=CENTER)
        pay_frame.grid_propagate(False)

        # order food activities

        tree_order_frame = Frame(order_frame)
        tree_order_frame.place(relx=0.3, rely=0.5, anchor=CENTER)

        tree_order_scroll = Scrollbar(tree_order_frame)
        tree_order_scroll.pack(side=RIGHT, fill=Y)

        cb_restaurant_query = "SELECT resName FROM restaurant"
        sql_cursor.execute(cb_restaurant_query)
        get_restaurant_names = sql_cursor.fetchall()
        restaurant_names = [name for name in get_restaurant_names]
        restaurant_menu = ttk.Combobox(order_frame, textvariable=self.res_menu_var, state='readonly')
        restaurant_menu.config(width=27, justify=CENTER, values=restaurant_names)
        restaurant_menu.set('---------Select Restaurant---------')
        restaurant_menu.place(relx=0.2, rely=0.2, anchor=CENTER)

        view_button = Button(order_frame, command=self.view_res_food_table)
        view_button.config(text='View', width=20)
        view_button.place(relx=0.42, rely=0.2, anchor=CENTER)

        view_table = ttk.Treeview(tree_order_frame, selectmode='browse')
        view_table.config(columns=("1", "2", "3", "4", "5"), show='headings',
                          yscrollcommand=tree_order_scroll.set)
        tree_order_scroll.config(command=view_table.yview)
        view_table.pack()
        view_table.column("1", width=80, anchor='c')
        view_table.column("2", width=80, anchor='c')
        view_table.column("3", width=80, anchor='c')
        view_table.column("4", width=80, anchor='c')
        view_table.column("5", width=80, anchor='c')
        view_table.heading("1", text="Food Id")
        view_table.heading("2", text="Food Name")
        view_table.heading("3", text="Calories")
        view_table.heading("4", text="Price")
        view_table.heading("5", text="Menu ID")

        tree_view_order_frame = Frame(order_frame)
        tree_view_order_frame.place(relx=0.75, rely=0.5, anchor=CENTER)

        tree_view_order_scroll = Scrollbar(tree_view_order_frame)
        tree_view_order_scroll.pack(side=RIGHT, fill=Y)

        view_order_table = ttk.Treeview(tree_view_order_frame, selectmode='browse')
        view_order_table.config(columns=("1", "2", "3", "4"), show='headings',
                                yscrollcommand=tree_view_order_scroll.set)
        tree_view_order_scroll.config(command=view_order_table.yview)
        view_order_table.pack()
        view_order_table.column("1", width=80, anchor='c')
        view_order_table.column("2", width=80, anchor='c')
        view_order_table.column("3", width=80, anchor='c')
        view_order_table.column("4", width=80, anchor='c')
        view_order_table.heading("1", text="Inorder Id")
        view_order_table.heading("2", text="Menu Id")
        view_order_table.heading("3", text="Food Name")
        view_order_table.heading("4", text="Order Id")

        order_frame_button = Button(order_frame, command=self.order_button)
        order_frame_button.config(text='Order', width=33)
        order_frame_button.place(relx=0.15, rely=0.75)

        delete_frame_button = Button(order_frame, command=self.delete_button)
        delete_frame_button.config(text='Delete', width=33)
        delete_frame_button.place(relx=0.6, rely=0.75)

        pay_frame_button = Button(order_frame, command=self.pay_button)
        pay_frame_button.config(text='Pay', width=33)
        pay_frame_button.place(relx=0.6, rely=0.8)

        # pay frame activities

        total_label = Label(pay_frame)
        total_label.config(text="Total")
        total_label.place(relx=0.35, rely=0.3, anchor='w')

        pay_name_label = Label(pay_frame)
        pay_name_label.config(text="Name")
        pay_name_label.place(relx=0.35, rely=0.4, anchor='w')

        credit_card_label = Label(pay_frame)
        credit_card_label.config(text="Credit Card Number")
        credit_card_label.place(relx=0.35, rely=0.45, anchor='w')

        exp_date_label = Label(pay_frame)
        exp_date_label.config(text="Expiration Date")
        exp_date_label.place(relx=0.35, rely=0.5, anchor='w')

        security_code_label = Label(pay_frame)
        security_code_label.config(text="Enter Security Code")
        security_code_label.place(relx=0.35, rely=0.55, anchor='w')

        total_entry = Entry(pay_frame)
        total_entry.config(width=30, bg='#F0F0F0')
        total_entry.place(relx=0.6, rely=0.3, anchor=CENTER)

        pay_name_entry = Entry(pay_frame)
        pay_name_entry.config(width=30)
        pay_name_entry.place(relx=0.6, rely=0.4, anchor=CENTER)

        credit_card_entry = Entry(pay_frame)
        credit_card_entry.config(width=30)
        credit_card_entry.place(relx=0.6, rely=0.45, anchor=CENTER)

        exp_date_entry = Entry(pay_frame)
        exp_date_entry.config(width=30)
        exp_date_entry.place(relx=0.6, rely=0.5, anchor=CENTER)

        sec_code_entry = Entry(pay_frame)
        sec_code_entry.config(width=30)
        sec_code_entry.place(relx=0.6, rely=0.55, anchor=CENTER)

        confirm_pay_button = Button(pay_frame, command=self.confirm_pay_button)
        confirm_pay_button.config(text="Confirm and Pay", width=33)
        confirm_pay_button.place(relx=0.4, rely=0.6)

        # View order status frame

        tree_view_order_status_frame = Frame(view_order_status_frame)
        tree_view_order_status_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        tree_view_scroll = Scrollbar(tree_view_order_status_frame)
        tree_view_scroll.pack(side=RIGHT, fill=Y)

        view_order_status_table = ttk.Treeview(tree_view_order_status_frame, selectmode='browse')
        view_order_status_table.config(columns=("1", "2", "3"), show='headings',
                                       yscrollcommand=tree_view_scroll.set)
        tree_view_scroll.config(command=view_table.yview)
        view_order_status_table.pack()
        view_order_status_table.column("1", width=100, anchor='c')
        view_order_status_table.column("2", width=100, anchor='c')
        view_order_status_table.column("3", width=100, anchor='c')
        view_order_status_table.heading("1", text="Order Id")
        view_order_status_table.heading("2", text="ETA")
        view_order_status_table.heading("3", text="Order Status")

        refresh_order_button = Button(view_order_status_frame, command=self.refresh_order_button)
        refresh_order_button.config(text='Refresh', width=20)
        refresh_order_button.place(relx=0.49, rely=0.8, anchor=CENTER)

        # Buttons

        order_button = Button(frame, command=lambda: self.show_frame(order_frame))
        order_button.config(text='Order Food', width=33, height=7, relief='flat', bg='#ff5900',
                            activebackground='#c75610', fg='white')
        order_button.bind('<Enter>', lambda event: self.button_on_hover(order_button, event))
        order_button.bind('<Leave>', lambda event: self.button_off_hover(order_button, event))
        order_button.place(relx=0, rely=0.159)

        view_order_status_button = Button(frame, command=lambda: self.show_frame(view_order_status_frame))
        view_order_status_button.config(text='View Order Status', width=33, height=7, relief='flat', bg='#FF8000',
                                        activebackground='#c75610', fg='white')
        view_order_status_button.bind('<Enter>', lambda event: self.button_on_hover(view_order_status_button, event))
        view_order_status_button.bind('<Leave>', lambda event: self.button_off_hover(view_order_status_button, event))
        view_order_status_button.place(relx=0, rely=0.32)

        profile_button = Button('', command=lambda: self.show_frame(profile_frame))
        profile_button.config(text='Edit Profile', width=33, height=7, relief='flat', bg='#ff5900',
                              activebackground='#c75610', fg='white')
        profile_button.bind('<Enter>', lambda event: self.button_on_hover(profile_button, event))
        profile_button.bind('<Leave>', lambda event: self.button_off_hover(profile_button, event))
        profile_button.place(relx=0, rely=0.48)

        self.show_frame(order_frame)

        frame.protocol('WM_DELETE_WINDOW', self.on_clickx)

    def on_clickx(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    def refresh_order_button(self, event=None):
        view_order_status_table.delete(*view_order_status_table.get_children())
        tree_view_order_status_frame.update()

        customer_id = self.id
        order_status_query = "SELECT orderstatus.orderId, ETA, oStatus FROM " \
                             "orderstatus, orders WHERE orders.orderId = (SELECT orders.orderId " \
                             "FROM orders WHERE orders.customerId = %s)"
        sql_cursor.execute(order_status_query, [customer_id])
        table_items = sql_cursor.fetchall()

        for dt in table_items:
            view_order_status_table.insert(parent='', index='end', values=(dt[0], dt[1], dt[2]))

    @staticmethod
    def delete_button(event=None):
        try:
            selected_item = view_order_table.selection()[0]
            inorder_values = view_order_table.item(selected_item, 'values')
            get_inorder_id = inorder_values[0]
            get_menu_id = inorder_values[1]
            get_food_name = inorder_values[2]
            get_order_id = inorder_values[3]
            rmv_query = "DELETE FROM inorder where inOrder_id = %s AND menuId = %s AND " \
                        "inorder.orderId = %s AND inorder.foodId = " \
                        "(SELECT food.foodId FROM food WHERE food.foodName = %s)"
            sql_cursor.execute(rmv_query, [get_inorder_id, get_menu_id, get_order_id, get_food_name])
            view_order_table.delete(selected_item)
            sql_db.commit()
            messagebox.showinfo("", "Deleted!")
        except BaseException:
            messagebox.showinfo("", "Failed to delete!")

    def order_button(self, event=None):
        view_order_table.delete(*view_order_table.get_children())
        tree_view_order_frame.update()

        item_list = None
        for dt in view_table.selection():
            item_list = view_table.item(dt, 'values')
        new_food_id = item_list[0]
        new_food_menu_id = item_list[4]
        customer_id = self.id
        add_to_order_query = "INSERT INTO orders (customerId) " \
                             "SELECT * FROM (SELECT %s) AS tmp " \
                             "WHERE NOT EXISTS (SELECT customerId FROM orders WHERE " \
                             "customerId = %s) LIMIT 1;"
        sql_cursor.execute(add_to_order_query, [customer_id, customer_id])
        sql_db.commit()

        add_to_inorder_query = "INSERT IGNORE INTO inorder (menuId, foodId, orderId)" \
                               "VALUES (%s, %s, (SELECT orders.orderId FROM " \
                               "orders WHERE orders.customerId = %s))"
        sql_cursor.execute(add_to_inorder_query, [new_food_menu_id, new_food_id, customer_id])
        sql_db.commit()

        view_order_query = "SELECT inOrder_id, inorder.menuId, foodName, inorder.orderId FROM inorder, orders " \
                           "INNER JOIN food WHERE inorder.foodId = food.foodId " \
                           "AND orders.orderId = inorder.orderId"
        sql_cursor.execute(view_order_query)
        table_items = sql_cursor.fetchall()

        for dt in table_items:
            view_order_table.insert(parent='', index='end', values=(dt[0], dt[1], dt[2], dt[3]))

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
    def pay_button(event=None):
        total_query = "SELECT ROUND(SUM(price), 2) Total FROM food as f INNER JOIN inorder as " \
                      "io WHERE f.foodId = io.foodId"
        sql_cursor.execute(total_query)
        total = sql_cursor.fetchall()
        total_entry.insert(0, total[0])
        pay_frame.tkraise()

    def confirm_pay_button(self, event=None):
        try:
            customer_id = self.id
            payment_query = "INSERT INTO payment (paymentType, payAccepted, orderId)" \
                            "VALUES ('Visa', 'Yes', (SELECT orders.orderId FROM orders WHERE orders.customerId = %s))"
            sql_cursor.execute(payment_query, [customer_id])
            sql_db.commit()

            total_entry.delete(0, END)
            pay_name_entry.delete(0, END)
            credit_card_entry.delete(0, END)
            exp_date_entry.delete(0, END)
            sec_code_entry.delete(0, END)

            order_status_query = "INSERT INTO orderstatus (orderId, oStatus) VALUES ((SELECT orders.orderId FROM " \
                                 "orders WHERE orders.customerId = %s), 'Processing')"
            sql_cursor.execute(order_status_query, [customer_id])
            sql_db.commit()

            messagebox.showinfo("", "Payment Successful!")
            order_frame.tkraise()
        except BaseException as e:
            messagebox.showinfo("", "Payment Failed!")

    def show_frame(self, frame):
        if frame == view_order_status_frame:
            customer_id = self.id
            order_status_query = "SELECT orderstatus.orderId, ETA, oStatus FROM orderstatus, orders WHERE " \
                                 "orderstatus.orderId = (SELECT orders.orderId WHERE orders.customerId = %s)"

            sql_cursor.execute(order_status_query, [customer_id])
            result = sql_cursor.fetchall()
            print(result)

            view_order_status_table.delete(*view_order_status_table.get_children())
            view_order_status_frame.update()

            frame.tkraise()
        else:
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
