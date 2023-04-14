from src.kasir.kasir import Kasir
from tools.db import DbHelper
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':

    db = DbHelper()

    if db.check_connection():
        kasir = Kasir()
        kasir.run()
