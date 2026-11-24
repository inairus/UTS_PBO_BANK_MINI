from rekening import Rekening


class RekeningTabungan(Rekening):
    def __init__(self, no_rekening, pemilik, saldo_awal=0, status="Aktif",
                 bunga_persen=2.0, biaya_admin=5000, setoran_minimal=10000):
        super().__init__(no_rekening, pemilik, saldo_awal, status)
        self.__bunga_persen = float(bunga_persen) if float(bunga_persen) >= 0 else 0.0
        self.__biaya_admin = float(biaya_admin) if float(biaya_admin) >= 0 else 0.0
        self.__setoran_minimal = float(setoran_minimal) if float(setoran_minimal) >= 0 else 0.0

    def get_bunga_persen(self):
        return self.__bunga_persen

    def get_biaya_admin(self):
        return self.__biaya_admin

    def get_setoran_minimal(self):
        return self.__setoran_minimal

    def ubah_bunga_persen(self, bunga_baru):
        if bunga_baru >= 0:
            self.__bunga_persen = float(bunga_baru)
            return True
        return False

    def hitung_bunga(self):
        return self.get_saldo() * (self.__bunga_persen / 100.0)

    def info_tabungan(self):
        return (
            f"{self.info_rekening()}\n"
            f"Bunga        : {self.__bunga_persen:.2f}% (Estimasi: Rp{self.hitung_bunga():,.0f})\n"
            f"Biaya Admin  : Rp{self.__biaya_admin:,.0f}\n"
            f"Setoran Min  : Rp{self.__setoran_minimal:,.0f}"
        )