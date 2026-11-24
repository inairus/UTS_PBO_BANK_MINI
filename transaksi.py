from datetime import datetime


class Transaksi:
    def __init__(self, id_transaksi, rekening, jenis, nominal):
        self.__id_transaksi = str(id_transaksi).strip() if id_transaksi is not None else ""  # ID unik transaksi
        self.__rekening = rekening  # Objek rekening terkait
        self.__jenis = str(jenis).strip().capitalize() if jenis is not None else ""  # Jenis: Setor/Tarik
        self.__nominal = self._parse_nominal(nominal)  # Nominal angka (float)
        self.__waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Waktu transaksi dibuat
        self.__status_trx = "Pending"  # Status: Pending/Berhasil/Gagal
        self.__keterangan = ""  # Pesan hasil atau alasan gagal

    def _parse_nominal(self, nominal):
        if nominal is None:
            return 0.0
        if isinstance(nominal, str):
            teks = nominal.strip().replace(",", ".")
            if not teks:
                return 0.0
            try:
                return float(teks)
            except ValueError:
                return 0.0
        try:
            return float(nominal)
        except (TypeError, ValueError):
            return 0.0

    def get_id_transaksi(self):
        return self.__id_transaksi

    def get_rekening(self):
        return self.__rekening

    def get_jenis(self):
        return self.__jenis

    def get_nominal(self):
        return self.__nominal

    def get_status_trx(self):
        return self.__status_trx

    def proses_transaksi(self):
        if not self.__id_transaksi:
            self.__status_trx = "Gagal"
            self.__keterangan = "ID transaksi tidak boleh kosong."
            return False, self.__keterangan

        if self.__nominal <= 0:
            self.__status_trx = "Gagal"
            self.__keterangan = "Nominal transaksi harus lebih dari 0."
            return False, self.__keterangan

        if self.__rekening is None:
            self.__status_trx = "Gagal"
            self.__keterangan = "Data rekening tidak ditemukan."
            return False, self.__keterangan

        if self.__jenis == "Setor":
            berhasil, pesan = self.__rekening.setor(self.__nominal)
        elif self.__jenis == "Tarik":
            berhasil, pesan = self.__rekening.tarik(self.__nominal)
        else:
            berhasil = False
            pesan = "Jenis transaksi harus Setor atau Tarik."

        self.__status_trx = "Berhasil" if berhasil else "Gagal"
        self.__keterangan = pesan
        return berhasil, pesan

    def info_transaksi(self):
        no_rek = self.__rekening.get_no_rekening() if self.__rekening else "-"
        pemilik = self.__rekening.get_pemilik() if self.__rekening else "-"
        return (
            f"ID Transaksi : {self.__id_transaksi}\n"
            f"Waktu        : {self.__waktu}\n"
            f"No. Rekening : {no_rek} ({pemilik})\n"
            f"Jenis        : {self.__jenis}\n"
            f"Nominal      : Rp{self.__nominal:,.0f}\n"
            f"Status Trx   : {self.__status_trx}\n"
            f"Keterangan   : {self.__keterangan}"
        )