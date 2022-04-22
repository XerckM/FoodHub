from tkinter import *
import mysql.connector


class Admin(object):
    def __init__(self, root, user, pwd):
        self.user = user
        self.pwd = pwd
        self.admin_frame(root)

    def admin_frame(self, root):
        sql_db = mysql.connector.connect(host='localhost',
                                         user=self.user,
                                         passwd=self.pwd,
                                         database='food_delivery')
        frame = Toplevel(root)
