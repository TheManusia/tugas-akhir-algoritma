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
        sql = f"CREATE TABLE IF NOT EXISTS {name} ({fields})"
        print(sql)
        cursor.execute(sql)

    def insert(self, table, fields, values):
        cursor = self.__db.cursor()
        sql = f"INSERT INTO {table} ({fields}) VALUES ({values})"
        cursor.execute(sql)
        self.__db.commit()
        return cursor.lastrowid

    def login(self, username, password):
        cursor = self.__db.cursor()
        sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(sql)
        return cursor.fetchone()

    def select(self, table, fields, where):
        cursor = self.__db.cursor()
        sql = f"SELECT {fields} FROM {table} WHERE {where}"
        cursor.execute(sql)
        return cursor.fetchall()

    def delete(self, table, where):
        cursor = self.__db.cursor()
        sql = f"DELETE FROM {table} WHERE {where}"
        cursor.execute(sql)
        self.__db.commit()

    def update(self, table, set, where):
        cursor = self.__db.cursor()
        sql = f"UPDATE {table} SET {set} WHERE {where}"
        print(sql)
        cursor.execute(sql)
        self.__db.commit()

    def exit(self):
        self.__db.close()
