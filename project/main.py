import os

import mysql.connector

from project.kasir import Kasir
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':

    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )

        if db.is_connected():
            print("Terkoneksi ke database")
    except mysql.connector.Error as err:
        print("Gagal terkoneksi ke database")
        exit(1)

    kasir = Kasir()
    kasir.run()
