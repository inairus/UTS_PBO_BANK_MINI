from rekening_tabungan import RekeningTabungan
from rekening_giro import RekeningGiro
from transaksi import Transaksi


def input_angka(pesan, boleh_kosong=False):
    # Validasi input angka
    while True:
        nilai = input(pesan).strip()
        if boleh_kosong and nilai == "":
            return None
        try:
            return float(nilai.replace(",", "."))
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")


def tambah_rekening(daftar_rekening):
    # Tambah rekening baru
    print("\n--- TAMBAH REKENING BARU ---")
    print("1. Rekening Tabungan")
    print("2. Rekening Giro")
    jenis = input("Pilih jenis (1/2): ").strip()

    no_rek = input("Nomor Rekening : ").strip()
    pemilik = input("Nama Pemilik   : ").strip()
    saldo_awal = input_angka("Saldo Awal     : ")

    if not no_rek or not pemilik:
        print("Nomor rekening dan nama pemilik tidak boleh kosong.")
        return

    if any(r.get_no_rekening() == no_rek for r in daftar_rekening):
        print("Nomor rekening sudah terdaftar.")
        return

    if jenis == "1":
        bunga = input_angka("Bunga (%) [default 2.0]: ", boleh_kosong=True)
        admin = input_angka("Biaya Admin [default 50000]: ", boleh_kosong=True)
        setor_min = input_angka("Setoran Minimal [default 100000]: ", boleh_kosong=True)

        rek = RekeningTabungan(
            no_rek,
            pemilik,
            saldo_awal,
            "Aktif",
            2.0 if bunga is None else bunga,
            50000 if admin is None else admin,
            100000 if setor_min is None else setor_min,
        )
    elif jenis == "2":
        batas_lebih = input_angka("Batas Tarik Lebih [default 500000000]: ", boleh_kosong=True)
        biaya_layanan = input_angka("Biaya Layanan Giro [default 100000]: ", boleh_kosong=True)
        kode_layanan = input("Kode Layanan [default GR-01]: ").strip() or "GR-01"

        rek = RekeningGiro(
            no_rek,
            pemilik,
            saldo_awal,
            "Aktif",
            500000000 if batas_lebih is None else batas_lebih,
            100000 if biaya_layanan is None else biaya_layanan,
            kode_layanan,
        )
    else:
        print("Pilihan jenis rekening tidak valid.")
        return

    daftar_rekening.append(rek)
    print("Rekening berhasil ditambahkan!")


def tambah_transaksi(daftar_rekening, daftar_transaksi):
    # Proses transaksi rekening
    print("\n--- TAMBAH TRANSAKSI ---")
    if not daftar_rekening:
        print("Rekening belum terdaftar.")
        return

    no_rek = input("Masukkan Nomor Rekening: ").strip()
    rek = next((r for r in daftar_rekening if r.get_no_rekening() == no_rek), None)
    if rek is None:
        print("Rekening tidak ditemukan.")
        return

    id_trx = input("ID Transaksi (misal TRX01): ").strip()
    jenis = input("Jenis Transaksi (Setor/Tarik): ").strip()
    nominal = input_angka("Nominal Transaksi: ")

    if not id_trx:
        print("ID transaksi tidak boleh kosong.")
        return

    trx = Transaksi(id_trx, rek, jenis, nominal)  # Relasi transaksi-rekening
    berhasil, pesan = trx.proses_transaksi()
    daftar_transaksi.append(trx)

    print("Hasil:", pesan)
    print("Status Transaksi:", trx.get_status_trx())


def tampilkan_data(daftar_rekening, daftar_transaksi):
    # Tampil rekening dan transaksi
    print("\n--- DAFTAR REKENING ---")
    if not daftar_rekening:
        print("Belum ada data rekening.")
    else:
        for idx, rek in enumerate(daftar_rekening, start=1):
            print(f"\n[{idx}]")
            if isinstance(rek, RekeningTabungan):
                print(rek.info_tabungan())
            elif isinstance(rek, RekeningGiro):
                print(rek.info_giro())
            else:
                print(rek.info_rekening())

    print("\n--- RIWAYAT TRANSAKSI ---")
    if not daftar_transaksi:
        print("Belum ada transaksi.")
    else:
        for idx, trx in enumerate(daftar_transaksi, start=1):
            print(f"\n[{idx}]")
            print(trx.info_transaksi())


def cari_data(daftar_rekening):
    # Cari data rekening
    print("\n--- CARI REKENING ---")
    kata_kunci = input("Masukkan No. Rekening atau Nama Pemilik: ").strip().lower()
    hasil = [
        r for r in daftar_rekening
        if kata_kunci in r.get_no_rekening().lower() or kata_kunci in r.get_pemilik().lower()
    ]

    if not hasil:
        print("Data rekening tidak ditemukan.")
        return

    for rek in hasil:
        print("-" * 35)
        if isinstance(rek, RekeningTabungan):
            print(rek.info_tabungan())
        elif isinstance(rek, RekeningGiro):
            print(rek.info_giro())
        else:
            print(rek.info_rekening())


def ubah_data(daftar_rekening):
    # Ubah status atau atribut
    print("\n--- UBAH DATA REKENING ---")
    no_rek = input("Masukkan Nomor Rekening yang ingin diubah: ").strip()
    rek = next((r for r in daftar_rekening if r.get_no_rekening() == no_rek), None)
    if rek is None:
        print("Rekening tidak ditemukan.")
        return

    print("1. Ubah Status Rekening (Aktif / Diblokir / Tutup)")
    if isinstance(rek, RekeningTabungan):
        print("2. Ubah Bunga Tabungan (%)")
    elif isinstance(rek, RekeningGiro):
        print("2. Ubah Batas Tarik Lebih")

    pilihan = input("Pilih opsi: ").strip()
    if pilihan == "1":
        status_baru = input("Status baru (Aktif/Diblokir/Tutup): ").strip().capitalize()
        if rek.ubah_status(status_baru):
            print("Status rekening berhasil diubah.")
        else:
            print("Status tidak valid.")
    elif pilihan == "2" and isinstance(rek, RekeningTabungan):
        bunga_baru = input_angka("Persentase bunga baru: ")
        if rek.ubah_bunga_persen(bunga_baru):
            print("Bunga tabungan berhasil diubah.")
        else:
            print("Nilai bunga tidak valid.")
    elif pilihan == "2" and isinstance(rek, RekeningGiro):
        batas_baru = input_angka("Batas tarik lebih baru: ")
        if rek.ubah_batas_tarik_lebih(batas_baru):
            print("Batas tarik lebih berhasil diubah.")
        else:
            print("Nilai batas tidak valid.")
    else:
        print("Pilihan tidak valid.")


def cek_status_data(daftar_rekening):
    # Cek status rekening
    print("\n--- CEK STATUS DATA REKENING ANDA ---")
    if not daftar_rekening:
        print("Belum ada data rekening.")
        return

    for rek in daftar_rekening:
        print(rek.cek_status_rekening())


def main():
    # Loop menu utama
    daftar_rekening = []
    daftar_transaksi = []

    while True:
        print("\n=== APLIKASI REKENING BANK MINI ===")
        print("1. Tambah Data (Rekening / Transaksi)")
        print("2. Tampilkan Data")
        print("3. Cari Data")
        print("4. Ubah Data")
        print("5. Cek Status Data")
        print("0. Keluar")

        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            print("1a. Tambah Rekening Baru")
            print("1b. Tambah Transaksi")
            sub = input("Pilih (a/b): ").strip().lower()
            if sub == "a":
                tambah_rekening(daftar_rekening)
            elif sub == "b":
                tambah_transaksi(daftar_rekening, daftar_transaksi)
            else:
                print("Pilihan tidak valid.")
        elif pilih == "2":
            tampilkan_data(daftar_rekening, daftar_transaksi)
        elif pilih == "3":
            cari_data(daftar_rekening)
        elif pilih == "4":
            ubah_data(daftar_rekening)
        elif pilih == "5":
            cek_status_data(daftar_rekening)
        elif pilih == "0":
            print("Terima kasih telah menggunakan Aplikasi Rekening Bank Mini Kami.")
            break
        else:
            print("Menu tidak tersedia. Silakan pilih 0-5.")


if __name__ == "__main__":
    main()