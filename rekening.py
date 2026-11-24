class Rekening:
    def __init__(self, no_rekening, pemilik, saldo_awal=0, status="Aktif"):
        self.__no_rekening = str(no_rekening).strip() if no_rekening is not None else ""  # Nomor rekening unik
        self.__pemilik = str(pemilik).strip() if pemilik is not None else ""  # Nama pemilik rekening
        self.__saldo = self._parse_saldo_awal(saldo_awal)  # Saldo rekening (float >= 0)
        self.__status = self._normalisasi_status(status) or "Aktif"  # Status: Aktif/Diblokir/Tutup

    def _parse_saldo_awal(self, saldo_awal):
        if saldo_awal is None:
            return 0.0
        try:
            nilai = float(str(saldo_awal).strip().replace(",", "."))
            return nilai if nilai >= 0 else 0.0
        except (TypeError, ValueError):
            return 0.0

    def _normalisasi_status(self, status):
        if status is None:
            return ""
        teks = str(status).strip().capitalize()
        return teks if teks in ["Aktif", "Diblokir", "Tutup"] else ""

    def get_no_rekening(self):
        return self.__no_rekening

    def get_pemilik(self):
        return self.__pemilik

    def get_saldo(self):
        return self.__saldo

    def get_status(self):
        return self.__status

    def ubah_status(self, status_baru):
        status_bersih = self._normalisasi_status(status_baru)
        if status_bersih:
            self.__status = status_bersih
            return True
        return False

    def setor(self, nominal):
        if self.__status != "Aktif":
            return False, f"Rekening tidak aktif (status: {self.__status})."
        if nominal <= 0:
            return False, "Nominal setor harus lebih dari 0."
        self.__saldo += float(nominal)
        return True, f"Setor Rp{nominal:,.0f} berhasil."

    def tarik(self, nominal):
        if self.__status != "Aktif":
            return False, f"Rekening tidak aktif (status: {self.__status})."
        if nominal <= 0:
            return False, "Nominal tarik harus lebih dari 0."
        if nominal > self.__saldo:
            return False, "Saldo tidak mencukupi."
        self.__saldo -= float(nominal)
        return True, f"Tarik Rp{nominal:,.0f} berhasil."

    def cek_status_rekening(self):
        return f"No. Rek {self.__no_rekening} ({self.__pemilik}) -> Status: {self.__status} | Saldo: Rp{self.__saldo:,.0f}"

    def info_rekening(self):
        return (
            f"No. Rekening : {self.__no_rekening}\n"
            f"Pemilik      : {self.__pemilik}\n"
            f"Jenis        : {self.__class__.__name__}\n"
            f"Saldo        : Rp{self.__saldo:,.0f}\n"
            f"Status       : {self.__status}"
        )