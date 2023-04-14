class Barang:
    def __init__(self, id_barang, nama, harga, stok):
        self.id_barang = id_barang
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def __str__(self):
        return f"{self.id_barang} - {self.nama}: Rp{'{:,.2f}'.format(self.harga)} ({self.stok})"
