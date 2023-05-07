from src.kasir.apps.gudang import Gudang
from src.kasir.apps.kasir import Kasir
from src.kasir.tools.db import DbHelper
from src.kasir.tools.tools import *


class Core:

    def __init__(self, user):
        self.user = user
        self.__db = DbHelper()

    def run(self):
        print(f"Selamat datang {self.user.username} di Toko Buku CLI")
        if self.user.role == "admin":
            self.__admin_menu()
        elif self.user.role == "kasir":
            self.__kasir_menu()
        elif self.user.role == "gudang":
            self.__gudang_menu()
        else:
            print("Role tidak ditemukan")

    def __kasir_menu(self):
        kasir = Kasir()
        kasir.run()

    def __gudang_menu(self):
        gudang = Gudang()
        gudang.run()

    def __admin_menu(self):
        while True:
            print("\nMenu:")
            print("1. Tambah User")
            print("2. Hapus User")
            print("3. Tampilkan User")
            print("4. Menu Kasir")
            print("5. Menu Gudang")
            print("6. Tampilkan Transaksi")
            print("7. Keluar")
            menu = int(input("\nPilih menu: "))
            print("")
            if menu == 1:
                self.__add_user()
            elif menu == 2:
                self.__remove_user()
            elif menu == 3:
                self.__show_user()
            elif menu == 4:
                self.__kasir_menu()
            elif menu == 5:
                self.__gudang_menu()
            elif menu == 6:
                self.__show_transaksi()
            elif menu == 7:
                self.__db.exit()
                break

    def __show_user(self):
        print("Daftar User")
        print("===========")
        cursor = self.__db.select("user", "*", "1")
        if cursor:
            for row in cursor:
                print(f"Username: {row[1]}")
                print(f"Role: {row[3]}")
                print("")
        else:
            print("User masih kosong")

    def __add_user(self):
        print("Tambah User")
        print("===========")
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        role = input("Masukkan role: ")
        if confirm("Tambah user?"):
            self.__db.insert("user", "username, password, role",
                             f"'{username}', '{encrypt_password(password)}', '{role}'")
            print("User berhasil ditambahkan")

    def __remove_user(self):
        print("Hapus User")
        print("==========")
        self.__show_user()
        username = input("Masukkan username: ")
        if confirm("Hapus user?"):
            self.__db.delete("user", f"username = '{username}'")
            print("User berhasil dihapus")

    def __show_transaksi(self):
        print("Daftar Transaksi")
        print("================")
        cursor = self.__db.select("transaksi", "*", "1")
        if cursor:
            for row in cursor:
                detail = self.__db.select("detail_transaksi", "*", f"id_transaksi = '{row[0]}'")
                print(f"ID Transaksi: {row[0]}")
                print(f"Tanggal: {row[1]}")
                print(f"Total: {currencyFormat(row[2])}")
                print("=====")
                i = 1
                for d in detail:
                    barang = self.__db.select("barang", "*", f"id_barang = '{d[2]}'")[0]
                    print(f"{i}. {barang[1]} x {d[3]} = {currencyFormat(d[4])}")
                    i += 1
                    print("")
        else:
            print("Transaksi masih kosong")
