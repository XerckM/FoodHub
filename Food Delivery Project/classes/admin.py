from tkinter import *
import mysql.connector


class Admin(object):
    def __init__(self, root):
        self.root = root
        self.admin_frame(self.root)

    def admin_frame(self, root):
        sql_db = mysql.connector.connect(host='localhost',
                                         port='3307',
                                         user='root',
                                         passwd='',
                                         database='food_delivery')
        frame = Toplevel(root)
