import csv
from datetime import datetime

# === Fungsi untuk membaca produk dari file CSV ===
def load_produk(nama_file):
    produk_list = []
    try:
        with open(nama_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                produk = {
                    "id": int(row["id"]),
                    "nama": row["nama"],
                    "harga": int(row["harga"]),
                    "stok": int(row["stok"])
                }
                produk_list.append(produk)
    except FileNotFoundError:
        print(f"File '{nama_file}' tidak ditemukan. Memulai dengan daftar kosong.")
    return produk_list

# === Fungsi untuk menyimpan produk ke file CSV ===
def simpan_produk(nama_file, produk_list):
    with open(nama_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["id", "nama", "harga", "stok"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produk in produk_list:
            writer.writerow(produk)

# === Fungsi untuk mencatat transaksi ke file CSV ===
def catat_transaksi(nama_file, id_produk, nama_produk, jumlah, total_harga):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(nama_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ["waktu", "id_produk", "nama_produk", "jumlah", "total_harga"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        file.seek(0, 2)  # Pindah ke akhir file
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "waktu": waktu,
            "id_produk": id_produk,
            "nama_produk": nama_produk,
            "jumlah": jumlah,
            "total_harga": total_harga
        })

# === Fitur 1: Menampilkan daftar produk ===
def tampilkan_produk(produk_list):
    print("\n=== Daftar Produk ===")
    if not produk_list:
        print("Belum ada produk.")
    for p in produk_list:
        print(f"{p['id']}. {p['nama']} - Rp{p['harga']} (Stok: {p['stok']})")

# === Fitur 2: Menambahkan produk baru (manual ID + validasi) ===
def tambah_produk(produk_list):
    while True:
        try:
            id_baru = int(input("Masukkan ID produk: "))
            if any(p["id"] == id_baru for p in produk_list):
                print("❌ ID sudah digunakan. Silakan masukkan ID lain.")
                continue
            break
        except ValueError:
            print("❌ Masukkan ID berupa angka.")

    nama = input("Nama produk: ")
    try:
        harga = int(input("Harga produk: "))
        stok = int(input("Jumlah stok: "))
    except ValueError:
        print("❌ Input harga/stok harus berupa angka.")
        return

    produk_baru = {
        "id": id_baru,
        "nama": nama,
        "harga": harga,
        "stok": stok
    }
    produk_list.append(produk_baru)
    print("✅ Produk berhasil ditambahkan.")

# === Fitur 3: Transaksi penjualan + catat transaksi ===
def transaksi_penjualan(produk_list):
    if not produk_list:
        print("Belum ada produk.")
        return

    tampilkan_produk(produk_list)
    try:
        id_pilih = int(input("Masukkan ID produk yang ingin dibeli: "))
        jumlah = int(input("Jumlah yang dibeli: "))
    except ValueError:
        print("❌ Input harus berupa angka.")
        return

    for p in produk_list:
        if p["id"] == id_pilih:
            if p["stok"] >= jumlah:
                total = p["harga"] * jumlah
                p["stok"] -= jumlah
                print(f"🛒 Total harga: Rp{total}")
                print("✅ Transaksi berhasil.")

                # Catat transaksi ke file transaksi.csv
                catat_transaksi("transaksi.csv", p["id"], p["nama"], jumlah, total)
            else:
                print("❌ Stok tidak cukup.")
            return
    print("❌ Produk tidak ditemukan.")

# === Fungsi utama ===
def jalankan_kasir():
    nama_file_produk = "produk.csv"
    produk = load_produk(nama_file_produk)

    while True:
        print("\n==== MENU KASIR ====")
        print("1. Tampilkan Produk")
        print("2. Tambah Produk")
        print("3. Transaksi Penjualan")
        print("4. Simpan dan Keluar")

        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            tampilkan_produk(produk)
        elif pilihan == "2":
            tambah_produk(produk)
        elif pilihan == "3":
            transaksi_penjualan(produk)
        elif pilihan == "4":
            simpan_produk(nama_file_produk, produk)
            print("✅ Data disimpan. Keluar dari program.")
            break
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")

# === Jalankan Program ===
if __name__ == "__main__":
    jalankan_kasir()
