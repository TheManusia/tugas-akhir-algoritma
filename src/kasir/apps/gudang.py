from src.kasir.model.barang import Barang
from src.kasir.tools.db import DbHelper
from src.kasir.tools.tools import *


class Gudang:
    def __init__(self):
        self.db = DbHelper()
        self.barang = []
        self.__fetch_barang()

    def run(self):
        print("Selamat datang di Gudang CLI")
        while True:
            print("\nMenu:")
            print("1. Tampilkan Barang")
            print("2. Tambah Barang")
            print("3. Hapus Barang")
            print("4. Update Barang")
            print("5. Keluar")
            menu = int(input("\nPilih menu: "))
            print("")
            if menu == 1:
                self.__show_barang()
            elif menu == 2:
                self.__add_barang()
            elif menu == 3:
                self.__remove_barang()
            elif menu == 4:
                self.__update_barang()
            elif menu == 5:
                self.db.exit()
                break

    def __fetch_barang(self):
        self.barang.clear()
        cursor = self.db.select("barang", "*", "1")
        if cursor:
            for row in cursor:
                self.barang.append(Barang(row[0], row[1], row[2], row[3]))

    def __show_barang(self):
        self.__fetch_barang()
        print("Daftar Barang:\n")
        for b in self.barang:
            print(b)

        if len(self.barang) == 0:
            print("Barang masih kosong")

    def __get_barang_by_id(self, id_barang):
        barang = None
        result = self.db.select("barang", "*", f"id_barang='{id_barang}'")
        if result:
            row = result[0]
            barang = Barang(row[0], row[1], row[2], row[3])
        return barang

    def __remove_barang(self):
        print("Hapus Barang")
        print("============")
        self.__show_barang()
        id_barang = input("Masukkan ID Barang: ")
        barang = self.__get_barang_by_id(id_barang)
        if barang and confirm("Apakah anda yakin ingin menghapus barang ini?"):
            self.db.delete("barang", f"id_barang='{id_barang}'")
            print("Berhasil menghapus barang")
        else:
            print("Barang tidak ditemukan")

    def __update_barang(self):
        print("Update Barang")
        print("=============")
        self.__show_barang()
        id_barang = input("Masukkan ID Barang: ")
        barang = self.__get_barang_by_id(id_barang)
        if barang:
            print(barang)
            print("Masukkan data baru")
            nama = input("Masukkan Nama Barang: ")
            harga = int(input("Masukkan Harga Barang: "))
            stok = int(input("Masukkan Stok Barang: "))
            if harga > 0 and stok > 0 and confirm("Apakah anda yakin ingin mengupdate barang ini?"):
                self.db.update("barang", f"nama='{nama}'", f"id_barang='{id_barang}'")
                self.db.update("barang", f"harga='{harga}'", f"id_barang='{id_barang}'")
                self.db.update("barang", f"stok='{stok}'", f"id_barang='{id_barang}'")
                print("Berhasil mengupdate barang")
            else:
                print("Harga atau stok barang tidak valid")
        else:
            print("Barang tidak ditemukan")

    def __add_barang(self):
        print("Tambah Barang")
        print("=============")
        print("1. Tambah barang yang sudah ada")
        print("2. Tambah barang baru")
        menu = int(input("Pilih menu: "))
        if menu == 1:
            self.__add_existing_barang()
        elif menu == 2:
            self.__add_new_barang()

    def __add_new_barang(self):
        print("Tambah Barang Baru")
        print("==================")
        nama = input("Masukkan Nama Barang: ")
        harga = int(input("Masukkan Harga Barang: "))
        stok = int(input("Masukkan Stok Barang: "))
        if harga > 0 and stok > 0 and confirm("Apakah anda yakin ingin menambahkan barang ini?"):
            self.db.insert("barang", "nama, harga, stok", f"'{nama}', {harga}, {stok}")
            print("Berhasil menambahkan barang")
        else:
            print("Harga atau stok barang tidak valid")

    def __add_existing_barang(self):
        print("Tambah Barang yang sudah ada")
        print("=============================")
        self.__show_barang()
        id_barang = int(input("Masukkan ID Barang: "))
        qty = int(input("Masukkan Jumlah Barang: "))
        if qty > 0:
            barang = self.__get_barang_by_id(id_barang)
            if barang and confirm("Apakah anda yakin ingin menambahkan barang ini?"):
                self.db.update("barang", "stok = stok + " + str(qty), "id_barang = " + str(id_barang))
                print("Berhasil menambahkan barang")
            else:
                print("Barang tidak ditemukan")
        else:
            print("Jumlah barang tidak valid")
