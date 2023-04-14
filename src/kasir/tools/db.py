import os

import mysql.connector


class DbHelper:

    def __init__(self):
        try:
            self.__db = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME")
            )
        except mysql.connector.Error as err:
            print("Gagal terkoneksi ke database")
            print(err)
            exit(1)

    def check_connection(self):
        return self.__db.is_connected()

    def create_table(self, name, fields):
        cursor = self.__db.cursor()
        sql = f"CREATE TABLE IF NOT EXIST {name} ({fields})"
        cursor.execute(sql)