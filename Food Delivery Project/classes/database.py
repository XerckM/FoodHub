class Database:

    @staticmethod
    def create_db(self):
        name = input('Enter database name: ')
        return f'CREATE DATABASE {name}'

    @staticmethod
    def remove_db(self):
        name = input('Enter database name: ')
        return f'DROP DATABASE {name}'

    @staticmethod
    def create_tb(self):
        table = input('Create table: ')
        return table

    @staticmethod
    def add_driver(fname, lname, driver_id, salary):
        pass



