import sqlite3
import os.path
import datetime

class Database:
    def __init__(self):
        have_database = self.is_have_database()
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        if (have_database == False):
            self.cursor.execute("CREATE TABLE prices (id INTEGER PRIMARY KEY AUTOINCREMENT, isbn INTEGER, date INTEGER, price INTEGER, salesman TEXT, city TEXT, marketplace TEXT)")
            self.con.commit()

    def get_date(self):
        now = datetime.datetime.now()
        today_midnight = datetime.datetime(now.year, now.month, now.day)
        seconds_since_epoch = (today_midnight - datetime.datetime(1970, 1, 1)).total_seconds()
        return seconds_since_epoch

    def is_have_database(self):
        return os.path.exists('database.db')

    def add_product(self, isbn, price:int, salesman:str, city:str, marketplace:str):
        self.cursor.execute(f"insert into prices (date, isbn, price, salesman, city, marketplace) VALUES ({self.get_date()}, {isbn}, {price},  '{salesman}', '{city}', '{marketplace}')")
        self.con.commit()

    def get_all_product(self):
        self.cursor.execute(f"SELECT DISTINCT date, isbn, price, salesman, city, marketplace FROM prices ORDER BY isbn, date, price")
        return self.cursor.fetchall()
    
    def get_data(self, city, marketplace, isbn):
        self.cursor.execute(f"SELECT DISTINCT date, isbn, price, salesman, city, marketplace FROM prices WHERE city = '{city}'  and marketplace = '{marketplace}' and isbn = {isbn} ORDER BY isbn, date, price")
        return self.cursor.fetchall()
    
    def get_isbn(self):
        self.cursor.execute(f"SELECT DISTINCT isbn FROM prices LIMIT 2")
        return self.cursor.fetchall()

    def __del__(self):
        self.con.close()