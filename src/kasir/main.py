from src.kasir.apps.core import Core
from src.kasir.model.user import User
from src.kasir.tools.tools import encrypt_password
from tools.db import DbHelper
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':

    db = DbHelper()

    if db.check_connection():
        print("Berhasil terkoneksi ke database")
        print("Membuat tabel barang")
        db.create_table("barang", "id_barang INT AUTO_INCREMENT PRIMARY KEY,"
                                  " nama VARCHAR(255),"
                                  " harga INT,"
                                  " stok INT")
        print("Membuat tabel transaksi")
        db.create_table("transaksi", "id_transaksi INT AUTO_INCREMENT PRIMARY KEY,"
                                     " tanggal DATE,"
                                     " total INT")
        print("Membuat tabel detail_transaksi")
        db.create_table("detail_transaksi", "id_detail INT AUTO_INCREMENT PRIMARY KEY,"
                                            " id_transaksi INT,"
                                            " id_barang INT,"
                                            " qty INT,"
                                            " total INT,"
                                            " FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi),"
                                            " FOREIGN KEY (id_barang) REFERENCES barang(id_barang)")
        print("Membuat tabel user")
        db.create_table("user", "id_user INT AUTO_INCREMENT PRIMARY KEY,"
                                " username VARCHAR(255),"
                                " password TEXT,"
                                " role VARCHAR(255)")

        print("Cek isi tabel user")
        cursor = db.select("user", "*", "1")

        if cursor:
            print("Tabel user sudah terisi")
        else:
            print("Tabel user belum terisi")

            print("Membuat user admin")
            pw = encrypt_password("admin")
            db.insert("user", "username, password, role", "'admin', '" + pw + "', 'admin'")
            print("Membuat user kasir")
            pw = encrypt_password("kasir")
            db.insert("user", "username, password, role", "'kasir', '" + pw + "', 'kasir'")
            print("Membuat user gudang")
            pw = encrypt_password("gudang")
            db.insert("user", "username, password, role", "'gudang', '" + pw + "', 'gudang'")

    else:
        print("Gagal terkoneksi ke database")
        exit(1)

    print("\n\nLogin")
    while True:
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        password = encrypt_password(password)
        user = db.login(username, password)
        if user:
            print("Login berhasil")
            break
        else:
            print("Username atau password salah")

    db.exit()

    core = Core(User(user[1], user[2], user[3]))
    core.run()
