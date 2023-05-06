from src.kasir.model.barang import Barang
from src.kasir.tools.db import DbHelper


def currencyFormat(number):
    return f"Rp{'{:,.2f}'.format(number)}"


class Kasir:

    def __init__(self):
        self.db = DbHelper()
        self.barang = []
        self.cart = []
        self.__fetch_barang()

    def __fetch_barang(self):
        self.barang.clear()
        cursor = self.db.select("barang", "*", "stok > 0")
        if cursor:
            for row in cursor:
                self.barang.append(Barang(row[0], row[1], row[2], row[3]))

    def run(self):
        print("Selamat datang di Toko Buku CLI")
        while True:
            print("\nMenu:")
            print("1. Tampilkan Barang")
            print("2. Tampilkan Keranjang")
            print("3. Tambahkan ke Keranjang")
            print("4. Hapus dari Keranjang")
            print("5. Checkout")
            print("6. Keluar")
            menu = int(input("\nPilih menu: "))
            print("")
            if menu == 1:
                self.__show_barang()
            elif menu == 2:
                self.__show_cart()
            elif menu == 3:
                self.__add_to_cart()
            elif menu == 4:
                self.__remove_from_cart()
            elif menu == 5:
                self.__checkout()
            elif menu == 6:
                break
            else:
                print("Menu tidak tersedia")

    def __show_barang(self):
        # Update data barang
        self.__fetch_barang()

        print("Daftar Barang:\n")
        for b in self.barang:
            print(b)

        if len(self.barang) == 0:
            print("Barang masih kosong")

    def __show_cart(self):
        print("Keranjang:")
        for c in self.cart:
            print(c)

        if len(self.cart) == 0:
            print("Keranjang masih kosong")

    def __add_to_cart(self):
        self.__show_barang()
        print("")
        id_barang = int(input("Masukkan ID Barang: "))
        qty = int(input("Masukkan Jumlah Barang: "))
        for b in self.barang:
            if b.id_barang == id_barang:
                # Jika stok barang cukup maka tambahkan ke keranjang
                if qty <= b.stok:

                    # Cari barang yang sama di keranjang dan tambahkan stok
                    for c in self.cart:
                        if c.id_barang == id_barang:
                            c.stok += qty
                            b.stok -= qty
                            return

                    self.cart.append(Barang(b.id_barang, b.nama, b.harga, qty))

                    # Kurangi stok barang di database
                    b.stok -= qty
                    self.db.update("barang", f"stok = {b.stok}", f"id_barang = {b.id_barang}")
                else:
                    print("Stok tidak cukup")
            else:
                print("Barang tidak ditemukan")

    def __remove_from_cart(self):
        self.__show_cart()
        id_barang = int(input("Masukkan ID Barang: "))
        qty = int(input("Masukkan Jumlah Barang: "))
        for c in self.cart:
            if c.id_barang == id_barang:
                c.stok -= qty

                # Jika stok barang di keranjang habis maka hapus dari keranjang
                if c.stok <= 0:
                    self.cart.remove(c)

                # Cari barang yang sama di daftar barang dan tambahkan stok
                for b in self.barang:
                    if b.id_barang == id_barang:
                        b.stok += qty
                        self.db.update("barang", f"stok = {b.stok}", f"id_barang = {b.id_barang}")
                        break
            else:
                print("Barang tidak ditemukan")

    def __checkout(self):
        # Menghitung total harga barang di keranjang
        total = 0
        for c in self.cart:
            total += c.harga * c.stok

        print(f"\nTotal harus Dibayar: {currencyFormat(total)}")
        uang = int(input("Uang Tunai Pembeli: Rp "))

        if uang < total:
            print("Uang tidak cukup")
            return

        # Menghitung kembalian
        kembalian = int(uang - total)
        print(f"Kembalian : {currencyFormat(kembalian)}")

        # Menampilkan struk
        print("\n===================================")
        print("======= S T R U K   B E L I =======")
        print("===================================")
        for c in self.cart:
            print(
                f"{c.nama}\t\t: {c.stok} x {currencyFormat(c.harga)} = {currencyFormat(c.stok * c.harga)}")
        print("")
        print(f"Tagihan\t\t\t: {currencyFormat(total)}")
        print(f"Dibayar\t\t\t: {currencyFormat(uang)}")
        print(f"Kembalian\t\t: {currencyFormat(kembalian)}")
        print("===================================")
        print("===================================")

        # Menambahkan detail transaksi ke database
        id=self.db.insert("transaksi", "tanggal, total", f"NOW(), {total}")
        for c in self.cart:
            self.db.insert("detail_transaksi", "id_transaksi, id_barang, qty", f"{id}, {c.id_barang}, {c.stok}")

        # Mengosongkan keranjang
        self.cart.clear()
