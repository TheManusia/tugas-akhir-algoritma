from src.kasir.apps.gudang import Gudang
from src.kasir.apps.kasir import Kasir
from src.kasir.tools.db import DbHelper
from src.kasir.tools.tools import Tools


class Core:

    def __init__(self, user):
        self.user = user
        self.__db = DbHelper()
        self.__tools = Tools()

    def run(self):
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
            print("6. Keluar")
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
                break

    def __show_user(self):
        print("Daftar User")
        print("===========")
        cursor = self.__db.select("user", "*", "1")
        if cursor:
            for row in cursor:
                print(f"Username: {row[0]}")
                print(f"Password: {row[1]}")
                print(f"Role: {row[2]}")
                print("")
        else:
            print("User masih kosong")

    def __add_user(self):
        print("Tambah User")
        print("===========")
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        role = input("Masukkan role: ")
        if self.__tools.confirm("Tambah user?"):
            self.__db.insert("user", "username, password, role",
                             f"'{username}', '{self.__tools.encrypt_password(password)}', '{role}'")
            print("User berhasil ditambahkan")

    def __remove_user(self):
        print("Hapus User")
        print("==========")
        self.__show_user()
        username = input("Masukkan username: ")
        if self.__tools.confirm("Hapus user?"):
            self.__db.delete("user", f"username = '{username}'")
            print("User berhasil dihapus")
