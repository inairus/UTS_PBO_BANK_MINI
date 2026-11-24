from rekening import Rekening


class RekeningGiro(Rekening):
    def __init__(self, no_rekening, pemilik, saldo_awal=0, status="Aktif",
                 batas_tarik_lebih=500000, biaya_layanan=10000, kode_layanan="GR-01"):
        super().__init__(no_rekening, pemilik, saldo_awal, status)
        self.__batas_tarik_lebih = self._parse_non_negatif(batas_tarik_lebih)  # Plafon tarik lebih (Rp)
        self.__biaya_layanan = self._parse_non_negatif(biaya_layanan)  # Biaya layanan giro (Rp)
        self.__kode_layanan = str(kode_layanan).strip() or "GR-01"  # Kode  giro

    def _parse_non_negatif(self, nilai):
        try:
            angka = float(str(nilai).strip().replace(",", "."))
            return angka if angka >= 0 else 0.0
        except (TypeError, ValueError):
            return 0.0

    def get_batas_tarik_lebih(self):
        return self.__batas_tarik_lebih

    def get_biaya_layanan(self):
        return self.__biaya_layanan

    def get_kode_layanan(self):
        return self.__kode_layanan

    def ubah_batas_tarik_lebih(self, batas_baru):
        try:
            angka = float(str(batas_baru).strip().replace(",", "."))
        except (TypeError, ValueError):
            return False
        if angka >= 0:
            self.__batas_tarik_lebih = angka
            return True
        return False

    def tarik(self, nominal):
        if self.get_status() != "Aktif":
            return False, f"Rekening tidak aktif (status: {self.get_status()})."
        if nominal <= 0:
            return False, "Nominal tarik harus lebih dari 0."
        batas_maksimal = self.get_saldo() + self.__batas_tarik_lebih
        if nominal > batas_maksimal:
            return False, "Melebihi saldo dan batas tarik lebih."
        # Pakai penarikan biasa jika cukup di saldo, atau overdraft jika melebihi saldo
        return super().tarik(nominal) if nominal <= self.get_saldo() else self.__tarik_overdraft(nominal)

    def __tarik_overdraft(self, nominal):
        # Mengurangi saldo hingga 0 dan mengurangi sisa batas tarik lebih
        selisih_saldo = self.get_saldo()
        sisa_kurang = nominal - selisih_saldo
        if sisa_kurang > self.__batas_tarik_lebih:
            return False, "Melebihi batas tarik lebih."
        if selisih_saldo > 0:
            super().tarik(selisih_saldo)
        self.__batas_tarik_lebih -= sisa_kurang
        return True, f"Tarik Rp{nominal:,.0f} berhasil (menggunakan batas tarik lebih Rp{sisa_kurang:,.0f})."

    def info_giro(self):
        return (
            f"{self.info_rekening()}\n"
            f"Kode Layanan     : {self.__kode_layanan}\n"
            f"Batas Tarik Lebih: Rp{self.__batas_tarik_lebih:,.0f}\n"
            f"Biaya Layanan    : Rp{self.__biaya_layanan:,.0f}"
        )