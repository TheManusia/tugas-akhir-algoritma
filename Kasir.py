from Model.Barang import Barang


def currencyFormat(number):
    return f"Rp{'{:,.2f}'.format(number)}"


class Kasir:

    def __init__(self):
        self.barang = [
            Barang(1, "Buku", 10000, 10),
            Barang(2, "Pensil", 5000, 20),
            Barang(3, "Penghapus", 3000, 30),
            Barang(4, "Penggaris", 2000, 40),
            Barang(5, "Penghapus Kertas", 1000, 50),
            Barang(6, "Penghapus Karet", 500, 60),
            Barang(7, "Penghapus Pensil", 100, 70),
        ]
        self.cart = []

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
                self.__showBarang()
            elif menu == 2:
                self.__showCart()
            elif menu == 3:
                self.__addToCart()
            elif menu == 4:
                self.__removeFromCart()
            elif menu == 5:
                self.__checkout()
            elif menu == 6:
                break
            else:
                print("Menu tidak tersedia")

    def __showBarang(self):
        print("Daftar Barang:\n")
        for b in self.barang:
            print(b)

        if len(self.barang) == 0:
            print("Barang masih kosong")

    def __showCart(self):
        print("Keranjang:")
        for c in self.cart:
            print(c)

        if len(self.cart) == 0:
            print("Keranjang masih kosong")

    def __addToCart(self):
        self.__showBarang()
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

                    # Kurangi stok barang di daftar barang
                    b.stok -= qty
                else:
                    print("Stok tidak cukup")
            else:
                print("Barang tidak ditemukan")

    def __removeFromCart(self):
        self.__showCart()
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

        # Mengosongkan keranjang
        self.cart.clear()

        # Menghapus barang yang stoknya habis
        for b in self.barang:
            if b.stok == 0:
                self.barang.remove(b)
