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


class Restaurant(object):
    def __init__(self, root, identity):
        self.root = root
        self.id = identity
        self.name = StringVar()
        self.price = StringVar()
        self.calories = StringVar()
        self.menu_var = StringVar()
        self.menu_add_var = StringVar()
        self.menu_rmv_var = StringVar()
        self.menu_mod_var = StringVar()
        self.restaurant_frame(self.root)

    def restaurant_frame(self, root):
        global name_entry, price_entry, calories_entry, \
            menu_entry, menu_option, rmv_table_menu, view_table, \
            tree_rmv_frame, modify_table_menu, mod_view_table, tree_mod_frame, \
            mod_name_entry, mod_price_entry, mod_calories_entry, mod_frame_button, \
            res_name_box, res_city_box, res_phone_box, res_open_box, res_close_box, \
            res_owner_box, res_city_box, res_state_box, profile_frame, apply_profile_button, \
            view_orders_table, tree_view_frame

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

        view_orders_frame = Frame(frame)
        view_orders_frame.config(width=850, height=565)
        view_orders_frame.grid(row=1, column=1, rowspan=5)
        view_orders_frame.grid_propagate(False)

        self.show_frame(add_frame)

        # add frame activities

        name_label = Label(add_frame)
        name_label.config(text="Name")
        name_label.place(relx=0.35, rely=0.3, anchor=CENTER)

        price_label = Label(add_frame)
        price_label.config(text="Price")
        price_label.place(relx=0.35, rely=0.4, anchor=CENTER)

        calories_label = Label(add_frame)
        calories_label.config(text="Calories")
        calories_label.place(relx=0.35, rely=0.5, anchor=CENTER)

        menu_label = Label(add_frame)
        menu_label.config(text="Menu")
        menu_label.place(relx=0.35, rely=0.6, anchor=CENTER)

        name_entry = Entry(add_frame, textvariable=self.name)
        name_entry.config(width=30)
        name_entry.place(relx=0.55, rely=0.3, anchor=CENTER)

        price_entry = Entry(add_frame, textvariable=self.price)
        price_entry.config(width=30)
        price_entry.place(relx=0.55, rely=0.4, anchor=CENTER)

        calories_entry = Entry(add_frame, textvariable=self.calories)
        calories_entry.config(width=30)
        calories_entry.place(relx=0.55, rely=0.5, anchor=CENTER)

        menu_entry = Entry(add_frame, textvariable=self.menu_var, fg='grey', justify=CENTER)
        menu_entry.config(width=30)
        menu_entry.insert(0, "Enter new menu name")
        menu_entry.place(relx=0.55, rely=0.6, anchor=CENTER)
        menu_entry.bind('<FocusIn>', self.menu_entry_onclick)
        menu_entry.bind('<FocusOut>', self.menu_entry_focusout)

        or_label = Label(add_frame)
        or_label.config(text="or")
        or_label.place(relx=0.54, rely=0.65, anchor=CENTER)

        cb_menu_query = "SELECT menuName FROM menu"
        sql_cursor.execute(cb_menu_query)
        get_menu_names = sql_cursor.fetchall()
        menu_names = [name for name in get_menu_names]
        menu_option = ttk.Combobox(add_frame, textvariable=self.menu_add_var, state='readonly')
        menu_option.config(width=27, justify=CENTER, values=menu_names)
        menu_option.set('-----SELECT FROM MENU-----')
        menu_option['value'] = [item for item in menu_names]
        menu_option.place(relx=0.55, rely=0.7, anchor=CENTER)

        add_frame_button = Button(add_frame, command=self.add)
        add_frame_button.config(text='Add Food', width=33)
        add_frame_button.place(relx=0.5, rely=0.8, anchor=CENTER)

        # remove frame activities

        tree_rmv_frame = Frame(remove_frame)
        tree_rmv_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        tree_rmv_scroll = Scrollbar(tree_rmv_frame)
        tree_rmv_scroll.pack(side=RIGHT, fill=Y)

        cb_rmv_menu_query = "SELECT menuName FROM menu"
        sql_cursor.execute(cb_rmv_menu_query)
        get_rmv_menu_names = sql_cursor.fetchall()
        rmv_menu_names = [name for name in get_rmv_menu_names]
        rmv_table_menu = ttk.Combobox(remove_frame, textvariable=self.menu_rmv_var, state='readonly')
        rmv_table_menu.config(width=27, justify=CENTER, values=rmv_menu_names)
        rmv_table_menu.set('---------Select Menu---------')
        rmv_table_menu.place(relx=0.4, rely=0.2, anchor=CENTER)

        view_button = Button(remove_frame, command=self.view_rmv_table)
        view_button.config(text='View', width=20)
        view_button.place(relx=0.65, rely=0.2, anchor=CENTER)

        view_table = ttk.Treeview(tree_rmv_frame, selectmode='browse')
        view_table.config(columns=("1", "2", "3", "4", "5"), show='headings',
                          yscrollcommand=tree_rmv_scroll.set)
        tree_rmv_scroll.config(command=view_table.yview)
        view_table.pack()
        view_table.column("1", width=100, anchor='c')
        view_table.column("2", width=100, anchor='c')
        view_table.column("3", width=100, anchor='c')
        view_table.column("4", width=100, anchor='c')
        view_table.column("5", width=100, anchor='c')
        view_table.heading("1", text="Food Id")
        view_table.heading("2", text="Food Name")
        view_table.heading("3", text="Calories")
        view_table.heading("4", text="Price")
        view_table.heading("5", text="Menu ID")

        remove_frame_button = Button(remove_frame, command=self.rmv_frame_rmv_button)
        remove_frame_button.config(text='Remove', width=33)
        remove_frame_button.place(relx=0.355, rely=0.75)

        # modify frame activities

        tree_mod_frame = Frame(modify_frame)
        tree_mod_frame.place(relx=0.255, rely=0.5, anchor=CENTER)

        tree_mod_scroll = Scrollbar(tree_mod_frame)
        tree_mod_scroll.pack(side=RIGHT, fill=Y)

        cb_mod_menu_query = "SELECT menuName FROM menu"
        sql_cursor.execute(cb_mod_menu_query)
        get_mod_menu_names = sql_cursor.fetchall()
        mod_menu_names = [name for name in get_mod_menu_names]
        modify_table_menu = ttk.Combobox(modify_frame, textvariable=self.menu_mod_var, state='readonly')
        modify_table_menu.config(width=27, justify=CENTER, values=mod_menu_names)
        modify_table_menu.set('---------Select Menu---------')
        modify_table_menu.place(relx=0.15, rely=0.25, anchor=CENTER)

        mod_view_button = Button(modify_frame, command=self.view_mod_table)
        mod_view_button.config(text='View', width=20)
        mod_view_button.place(relx=0.4, rely=0.25, anchor=CENTER)

        mod_view_table = ttk.Treeview(tree_mod_frame, selectmode='browse')
        mod_view_table.config(columns=("1", "2", "3", "4", "5"), show='headings',
                              yscrollcommand=tree_mod_scroll.set)
        tree_mod_scroll.config(command=mod_view_table.yview)
        mod_view_table.pack()
        mod_view_table.column("1", width=80, anchor=CENTER)
        mod_view_table.column("2", width=80, anchor=CENTER)
        mod_view_table.column("3", width=80, anchor=CENTER)
        mod_view_table.column("4", width=80, anchor=CENTER)
        mod_view_table.column("5", width=80, anchor=CENTER)
        mod_view_table.heading("1", text="Food Id")
        mod_view_table.heading("2", text="Food Name")
        mod_view_table.heading("3", text="Calories")
        mod_view_table.heading("4", text="Price")
        mod_view_table.heading("5", text="Menu ID")

        mod_frame_button = Button(modify_frame, command=self.modify_mod)
        mod_frame_button.config(text='Modify', width=33)
        mod_frame_button.place(relx=0.1, rely=0.75)

        mod_name_label = Label(modify_frame)
        mod_name_label.config(text="Name")
        mod_name_label.place(relx=0.6, rely=0.4, anchor=CENTER)

        mod_price_label = Label(modify_frame)
        mod_price_label.config(text="Price")
        mod_price_label.place(relx=0.6, rely=0.5, anchor=CENTER)

        mod_calories_label = Label(modify_frame)
        mod_calories_label.config(text="Calories")
        mod_calories_label.place(relx=0.6, rely=0.6, anchor=CENTER)

        mod_name_entry = Entry(modify_frame, textvariable=self.name, state=DISABLED)
        mod_name_entry.config(width=30)
        mod_name_entry.place(relx=0.8, rely=0.4, anchor=CENTER)

        mod_price_entry = Entry(modify_frame, textvariable=self.price, state=DISABLED)
        mod_price_entry.config(width=30)
        mod_price_entry.place(relx=0.8, rely=0.5, anchor=CENTER)

        mod_calories_entry = Entry(modify_frame, textvariable=self.calories, state=DISABLED)
        mod_calories_entry.config(width=30)
        mod_calories_entry.place(relx=0.8, rely=0.6, anchor=CENTER)

        mod_frame_button = Button(modify_frame, command=self.confirm_mod, state=DISABLED)
        mod_frame_button.config(text='Confirm', width=33)
        mod_frame_button.place(relx=0.75, rely=0.775, anchor=CENTER)

        # edit profile frame

        restaurant_name = Label(profile_frame)
        restaurant_name.config(text="Restaurant Name")
        restaurant_name.place(relx=0.3, rely=0.25, anchor='w')

        restaurant_owner = Label(profile_frame)
        restaurant_owner.config(text="Owner")
        restaurant_owner.place(relx=0.3, rely=0.3, anchor='w')

        restaurant_city = Label(profile_frame)
        restaurant_city.config(text="City")
        restaurant_city.place(relx=0.3, rely=0.35, anchor='w')

        restaurant_state = Label(profile_frame)
        restaurant_state.config(text="State")
        restaurant_state.place(relx=0.3, rely=0.4, anchor='w')

        restaurant_phone = Label(profile_frame)
        restaurant_phone.config(text="Phone Number")
        restaurant_phone.place(relx=0.3, rely=0.45, anchor='w')

        restaurant_open = Label(profile_frame)
        restaurant_open.config(text="Open Hours")
        restaurant_open.place(relx=0.3, rely=0.5, anchor='w')

        restaurant_close = Label(profile_frame)
        restaurant_close.config(text="Closed Hours")
        restaurant_close.place(relx=0.3, rely=0.55, anchor='w')

        res_name_box = Entry(profile_frame)
        res_name_box.config(width=30, bg='#F0F0F0')
        res_name_box.place(relx=0.6, rely=0.25, anchor=CENTER)

        res_owner_box = Entry(profile_frame)
        res_owner_box.config(width=30, bg='#F0F0F0')
        res_owner_box.place(relx=0.6, rely=0.3, anchor=CENTER)

        res_city_box = Entry(profile_frame)
        res_city_box.config(width=30, bg='#F0F0F0')
        res_city_box.place(relx=0.6, rely=0.35, anchor=CENTER)

        res_state_box = Entry(profile_frame)
        res_state_box.config(width=30, bg='#F0F0F0')
        res_state_box.place(relx=0.6, rely=0.4, anchor=CENTER)

        res_phone_box = Entry(profile_frame)
        res_phone_box.config(width=30, bg='#F0F0F0')
        res_phone_box.place(relx=0.6, rely=0.45, anchor=CENTER)

        res_open_box = Entry(profile_frame)
        res_open_box.config(width=30, bg='#F0F0F0')
        res_open_box.place(relx=0.6, rely=0.5, anchor=CENTER)

        res_close_box = Entry(profile_frame)
        res_close_box.config(width=30, bg='#F0F0F0')
        res_close_box.place(relx=0.6, rely=0.55, anchor=CENTER)

        edit_profile_button = Button(profile_frame, command=self.edit_button)
        edit_profile_button.config(text='Edit Profile', width=33)
        edit_profile_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        apply_profile_button = Button(profile_frame, command=self.apply_button)
        apply_profile_button.config(text='Apply', width=33, state=DISABLED)
        apply_profile_button.place(relx=0.5, rely=0.75, anchor=CENTER)

        # view orders frame

        tree_view_frame = Frame(view_orders_frame)
        tree_view_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        tree_view_scroll = Scrollbar(tree_view_frame)
        tree_view_scroll.pack(side=RIGHT, fill=Y)

        view_orders_table = ttk.Treeview(tree_view_frame, selectmode='extended')
        view_orders_table.config(columns=("1", "2", "3", "4"), show='headings',
                                 yscrollcommand=tree_view_scroll.set)
        tree_view_scroll.config(command=view_orders_table.yview)
        view_orders_table.pack()
        view_orders_table.column("1", width=100, anchor='c')
        view_orders_table.column("2", width=100, anchor='c')
        view_orders_table.column("3", width=100, anchor='c')
        view_orders_table.column("4", width=100, anchor='c')
        view_orders_table.heading("1", text="Inorder Id")
        view_orders_table.heading("2", text="Menu Id")
        view_orders_table.heading("3", text="Food Name")
        view_orders_table.heading("4", text="Order Id")

        view_orders_button = Button(view_orders_frame, command=self.order_ready_button)
        view_orders_button.config(text='Order Ready for Pickup', width=33)
        view_orders_button.place(relx=0.355, rely=0.75)

        refresh_orders_button = Button(view_orders_frame, command=self.refresh_button)
        refresh_orders_button.config(text='Refresh', width=33)
        refresh_orders_button.place(relx=0.355, rely=0.8)

        # Left Side Buttons

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

        view_orders = Button(frame, command=lambda: self.show_frame(view_orders_frame))
        view_orders.config(text='View Orders', width=33, height=7, relief='flat', bg='#ff5900',
                           activebackground='#c75610', fg='white')
        view_orders.bind('<Enter>', lambda event: self.button_on_hover(view_orders, event))
        view_orders.bind('<Leave>', lambda event: self.button_off_hover(view_orders, event))
        view_orders.grid(row=5, column=0)

        frame.protocol('WM_DELETE_WINDOW', self.on_clickx)

    def add(self, event=None):
        name = name_entry.get()
        calories = calories_entry.get()
        price = price_entry.get()
        menu = menu_entry.get()
        menu_drop = menu_option.get()
        owner_id = str(self.id)
        if name == "" and calories == "" and price == "":
            messagebox.showinfo("", "Values can not be empty")
        elif menu not in ("Enter new menu name", "") and menu_drop == '-----SELECT FROM MENU-----':
            add_menu_query = "INSERT IGNORE INTO menu (menuName, restaurantId) VALUES (%s, (SELECT restaurantId FROM " \
                             "restaurant WHERE ownerId = %s)) "
            sql_cursor.execute(add_menu_query, [menu, owner_id])
            sql_db.commit()
            add_food_query = "INSERT IGNORE INTO food (foodName, calories, price, menuId) VALUES (%s, %s, %s, (SELECT " \
                             "menuId FROM menu WHERE menuName = %s)) "
            sql_cursor.execute(add_food_query, [name, calories, price, menu])
            sql_db.commit()
            name_entry.delete(0, END)
            calories_entry.delete(0, END)
            price_entry.delete(0, END)
            menu_entry.delete(0, END)
            menu_entry.insert(0, 'Enter new menu name')
            menu_entry.config(fg='grey', justify=CENTER)
            menu_option.set('---------Select Menu---------')
            messagebox.showinfo("", "Added!")
        elif menu_drop != '-----SELECT FROM MENU-----' and menu in ("Enter new menu name", ""):
            add_food_query = "INSERT INTO food (foodName, calories, price, menuId) " \
                             "VALUES (%s, %s, %s, (SELECT menuId FROM menu WHERE menuName = %s))"
            sql_cursor.execute(add_food_query, [name, calories, price, menu_drop])
            sql_db.commit()
            name_entry.delete(0, END)
            calories_entry.delete(0, END)
            price_entry.delete(0, END)
            menu_option.set('---------Select Menu---------')
            messagebox.showinfo("", "Added!")
        else:
            messagebox.showinfo("", "Values can not be empty. Select either from dropdown or create new menu")

    @staticmethod
    def order_ready_button(event=None):
        get_selection = view_orders_table.selection()
        size_of_selection = len(get_selection)
        for item in range(size_of_selection):
            pass

    @staticmethod
    def refresh_button(event=None):
        view_orders_table.delete(*view_orders_table.get_children())
        tree_view_frame.update()

        view_order_query = "SELECT inOrder_id, inorder.menuId, foodName, inorder.orderId FROM inorder, orders " \
                           "INNER JOIN food WHERE inorder.foodId = food.foodId " \
                           "AND orders.orderId = inorder.orderId"
        sql_cursor.execute(view_order_query)
        table_items = sql_cursor.fetchall()

        for dt in table_items:
            view_orders_table.insert(parent='', index='end', values=(dt[0], dt[1], dt[2], dt[3]))

    def on_clickx(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    @staticmethod
    def view_rmv_table(event=None):
        view_table.delete(*view_table.get_children())
        tree_rmv_frame.update()

        table_var = rmv_table_menu.get()
        get_all_food = "SELECT foodId, foodName, calories, price, food.menuId FROM food WHERE food.menuId = (SELECT " \
                       "menu.menuId FROM menu WHERE menu.menuName = %s) "
        sql_cursor.execute(get_all_food, [table_var])
        table_items = sql_cursor.fetchall()

        for dt in table_items:
            view_table.insert(parent='', index='end', iid=dt[0], values=(dt[0], dt[1], dt[2], dt[3], dt[4]))

    @staticmethod
    def rmv_frame_rmv_button(event=None):
        try:
            selected_item = view_table.selection()[0]
            rmv_query = "DELETE FROM food where foodId = %s"
            sql_cursor.execute(rmv_query, [selected_item])
            view_table.delete(selected_item)
            sql_db.commit()
            messagebox.showinfo("", "Deleted")
        except BaseException:
            messagebox.showinfo("", "Failed to delete!")


    @staticmethod
    def view_mod_table(event=None):
        mod_view_table.delete(*mod_view_table.get_children())
        tree_mod_frame.update()

        table_var = modify_table_menu.get()
        get_all_food = "SELECT foodId, foodName, calories, price, food.menuId FROM food WHERE food.menuId = (SELECT " \
                       "menu.menuId FROM menu WHERE menu.menuName = %s) "
        sql_cursor.execute(get_all_food, [table_var])
        table_items = sql_cursor.fetchall()

        for dt in table_items:
            mod_view_table.insert(parent='', index='end', iid=dt[0], values=(dt[0], dt[1], dt[2], dt[3], dt[4]))

    @staticmethod
    def modify_mod(event=None):
        global select_id
        try:
            item_list = None
            for dt in mod_view_table.selection():
                item_list = mod_view_table.item(dt, 'values')
            select_name = item_list[1]
            select_calories = item_list[2]
            select_price = item_list[3]
            select_id = item_list[0]

            mod_name_entry.config(state=NORMAL)
            mod_price_entry.config(state=NORMAL)
            mod_calories_entry.config(state=NORMAL)
            mod_frame_button.config(state=NORMAL)

            mod_name_entry.insert(0, select_name)
            mod_price_entry.insert(0, select_price)
            mod_calories_entry.insert(0, select_calories)
        except BaseException:
            messagebox.showinfo("", "Oops! Something went wrong.")

    @staticmethod
    def confirm_mod(event=None):
        try:
            food_id = select_id
            new_name_entry = mod_name_entry.get()
            new_calories_entry = mod_calories_entry.get()
            new_price_entry = mod_price_entry.get()
            mod_update_query = "UPDATE food SET foodName = %s, calories = %s, price = %s WHERE food.foodId = %s"
            sql_cursor.execute(mod_update_query, [new_name_entry, new_calories_entry, new_price_entry, food_id])
            sql_db.commit()
            messagebox.showinfo("", "Success!")
        except BaseException:
            messagebox.showinfo("", "Failed to update!")

    @staticmethod
    def edit_button(event=None):
        apply_profile_button.config(state=NORMAL)
        res_name_box.config(bg='white')
        res_owner_box.config(bg='white')
        res_city_box.config(bg='white')
        res_state_box.config(bg='white')
        res_phone_box.config(bg='white')
        res_open_box.config(bg='white')
        res_close_box.config(bg='white')

    def apply_button(self, event=None):
        get_owner_id = self.id
        new_res_name_box = res_name_box.get()
        new_res_city_box = res_city_box.get()
        new_res_state_box = res_state_box.get()
        new_res_phone_box = res_phone_box.get()
        new_res_open_box = res_open_box.get()
        new_res_close_box = res_close_box.get()

        profile_update_query = "UPDATE restaurant SET resName = %s, city = %s, state = %s, " \
                               "phoneNumber = %s, timeOpen = %s, timeClose = %s WHERE ownerId = %s"
        sql_cursor.execute(profile_update_query, [new_res_name_box, new_res_city_box, new_res_state_box,
                                                  new_res_phone_box, new_res_open_box, new_res_close_box, get_owner_id])
        sql_db.commit()
        apply_profile_button.config(state=DISABLED)
        res_name_box.config(bg='#F0F0F0')
        res_owner_box.config(bg='#F0F0F0')
        res_city_box.config(bg='#F0F0F0')
        res_state_box.config(bg='#F0F0F0')
        res_phone_box.config(bg='#F0F0F0')
        res_open_box.config(bg='#F0F0F0')
        res_close_box.config(bg='#F0F0F0')
        messagebox.showinfo("", "Update Success!")


    @staticmethod
    def menu_entry_onclick(event):
        if menu_entry.get() == 'Enter new menu name':
            menu_entry.delete(0, "end")
            menu_entry.insert(0, '')
            menu_entry.config(fg='black', justify=LEFT)

    @staticmethod
    def menu_entry_focusout(event):
        if menu_entry.get() == '':
            menu_entry.insert(0, 'Enter new menu name')
            menu_entry.config(fg='grey', justify=CENTER)

    def show_frame(self, frame):
        if frame == profile_frame:
            get_owner_id = self.id
            get_profile_query = "SELECT * FROM restaurant WHERE ownerId = %s"
            sql_cursor.execute(get_profile_query, [get_owner_id])
            result = sql_cursor.fetchall()

            res_name_box.delete(0, END)
            res_owner_box.delete(0, END)
            res_city_box.delete(0, END)
            res_state_box.delete(0, END)
            res_phone_box.delete(0, END)
            res_open_box.delete(0, END)
            res_close_box.delete(0, END)

            res_name_box.insert(0, result[0][1])
            res_owner_box.insert(0, result[0][2])
            res_city_box.insert(0, result[0][3])
            res_state_box.insert(0, result[0][4])
            res_phone_box.insert(0, result[0][5])
            res_open_box.insert(0, result[0][6])
            res_close_box.insert(0, result[0][7])
            frame.tkraise()
        else:
            frame.tkraise()

    @staticmethod
    def button_on_hover(button, event=None):
        button['background'] = '#FF9D00'

    @staticmethod
    def button_off_hover(button, event=None):
        if button['text'] in ('Add Food', 'Modify Food', 'View Orders'):
            button['background'] = '#ff5900'
        else:
            button['background'] = '#FF8000'
