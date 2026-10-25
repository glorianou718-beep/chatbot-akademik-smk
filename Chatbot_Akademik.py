import sqlite3

# ==============================
# KONEKSI DATABASE
# ==============================
DATABASE = "akademik.db"


def koneksi_database():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==============================
# MENCARI DATA SISWA
# ==============================
def cari_siswa(nama):
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM siswa
        WHERE LOWER(nama) = LOWER(?)
    """, (nama,))

    siswa = cursor.fetchone()

    conn.close()

    return siswa


# ==============================
# TAMPILKAN JADWAL
# ==============================
def tampilkan_jadwal():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hari, jam, mata_pelajaran, guru
        FROM jadwal
        ORDER BY
            CASE hari
                WHEN 'Senin' THEN 1
                WHEN 'Selasa' THEN 2
                WHEN 'Rabu' THEN 3
                WHEN 'Kamis' THEN 4
                WHEN 'Jumat' THEN 5
                ELSE 6
            END,
            jam
    """)

    data = cursor.fetchall()
    conn.close()

    print("Bot: Berikut informasi jadwal pelajaran:")
    print()

    hari_sebelumnya = ""

    for row in data:

        if row["hari"] != hari_sebelumnya:
            print(row["hari"] + ":")
            hari_sebelumnya = row["hari"]

        print(
            "-",
            row["jam"],
            ":",
            row["mata_pelajaran"],
            "(" + row["guru"] + ")"
        )

    print()


# ==============================
# TAMPILKAN NILAI
# ==============================
def tampilkan_nilai(id_siswa):
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mata_pelajaran, nilai
        FROM nilai
        WHERE id_siswa = ?
    """, (id_siswa,))

    data = cursor.fetchall()
    conn.close()

    print("Bot: Berikut informasi nilai kamu:")
    print()

    for row in data:
        print(
            row["mata_pelajaran"],
            ":",
            row["nilai"]
        )

    print()


# ==============================
# TAMPILKAN ABSENSI
# ==============================
def tampilkan_absensi(id_siswa):
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*) AS jumlah
        FROM absensi
        WHERE id_siswa = ?
        GROUP BY status
    """, (id_siswa,))

    data = cursor.fetchall()
    conn.close()

    print("Bot: Berikut informasi absensi kamu:")
    print()

    hasil = {
        "Hadir": 0,
        "Izin": 0,
        "Sakit": 0,
        "Alpa": 0
    }

    for row in data:
        if row["status"] in hasil:
            hasil[row["status"]] = row["jumlah"]

    print("Hadir :", hasil["Hadir"], "kali")
    print("Izin  :", hasil["Izin"], "kali")
    print("Sakit :", hasil["Sakit"], "kali")
    print("Alpa  :", hasil["Alpa"], "kali")

    print()


# ==============================
# TAMPILKAN KEGIATAN
# ==============================
def tampilkan_kegiatan():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nama_kegiatan, tanggal, tempat, keterangan
        FROM kegiatan
        ORDER BY tanggal
    """)

    data = cursor.fetchall()
    conn.close()

    print("Bot: Berikut kegiatan sekolah:")
    print()

    nomor = 1

    for row in data:

        print(str(nomor) + ".", row["nama_kegiatan"])
        print("   Tanggal :", row["tanggal"])
        print("   Tempat  :", row["tempat"])

        if row["keterangan"]:
            print("   Keterangan :", row["keterangan"])

        print()

        nomor += 1


# ==============================
# TAMPILKAN INFORMASI UJIAN
# ==============================
def tampilkan_ujian():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nama_kegiatan, tanggal, tempat, keterangan
        FROM kegiatan
        WHERE LOWER(nama_kegiatan) LIKE '%ujian%'
    """)

    data = cursor.fetchall()
    conn.close()

    print("Bot: Informasi ujian:")
    print()

    if len(data) == 0:
        print("Belum ada informasi ujian.")
    else:

        for row in data:
            print(row["nama_kegiatan"])
            print("Tanggal :", row["tanggal"])
            print("Tempat  :", row["tempat"])

            if row["keterangan"]:
                print("Keterangan :", row["keterangan"])

            print()


# ==============================
# PROGRAM CHATBOT
# ==============================

print("======================================")
print("     CHATBOT INFORMASI AKADEMIK SMK")
print("======================================")

nama = input("Masukkan nama kamu: ")

# Mencari siswa di database
siswa = cari_siswa(nama)

print()

if siswa:
    print("Halo,", siswa["nama"])
    print("Kelas :", siswa["kelas"])
    print("Selamat datang di Chatbot Akademik!")
    print("Saya siap membantu memberikan informasi.")
else:
    print("Halo,", nama)
    print("Data siswa belum ditemukan di database.")
    print("Tetapi kamu tetap dapat menggunakan chatbot.")

while True:

    print()

    pertanyaan = input("Apa yang ingin kamu tanyakan? ")

    pertanyaan = pertanyaan.lower()

    print()

    # =========================
    # INFORMASI JADWAL
    # =========================
    if "jadwal" in pertanyaan:

        tampilkan_jadwal()

    # =========================
    # INFORMASI NILAI
    # =========================
    elif "nilai" in pertanyaan:

        if siswa:
            tampilkan_nilai(siswa["id_siswa"])
        else:
            print("Bot: Data nilai siswa tidak ditemukan.")

    # =========================
    # INFORMASI ABSENSI
    # =========================
    elif "absensi" in pertanyaan or "kehadiran" in pertanyaan:

        if siswa:
            tampilkan_absensi(siswa["id_siswa"])
        else:
            print("Bot: Data absensi siswa tidak ditemukan.")

    # =========================
    # INFORMASI KEGIATAN
    # =========================
    elif "kegiatan" in pertanyaan or "agenda" in pertanyaan:

        tampilkan_kegiatan()

    # =========================
    # INFORMASI AKADEMIK
    # =========================
    elif "akademik" in pertanyaan:

        print("Bot: Informasi akademik yang tersedia:")
        print()
        print("- Jadwal pelajaran")
        print("- Nilai siswa")
        print("- Absensi siswa")
        print("- Kegiatan sekolah")
        print("- Jadwal ujian")
        print("- Informasi pembelajaran")

    # =========================
    # INFORMASI UJIAN
    # =========================
    elif "ujian" in pertanyaan:

        tampilkan_ujian()

    # =========================
    # SALAM
    # =========================
    elif "halo" in pertanyaan or "hai" in pertanyaan:

        print("Bot: Halo", nama + "!")
        print("Bot: Ada yang bisa saya bantu?")

    # =========================
    # BANTUAN
    # =========================
    elif "bantuan" in pertanyaan or "menu" in pertanyaan:

        print("Bot: Saya dapat membantu kamu dengan:")
        print()
        print("1. Jadwal")
        print("2. Nilai")
        print("3. Absensi")
        print("4. Kegiatan sekolah")
        print("5. Informasi akademik")
        print("6. Informasi ujian")

    # =========================
    # KELUAR
    # =========================
    elif "keluar" in pertanyaan or "exit" in pertanyaan:

        print("Bot: Terima kasih sudah menggunakan")
        print("     Chatbot Informasi Akademik SMK.")
        print("Sampai jumpa,", nama + "!")
        break

    # =========================
    # PERTANYAAN TIDAK DIKENALI
    # =========================
    else:

        print("Bot: Maaf,", nama)
        print("Bot: Saya belum memahami pertanyaan tersebut.")
        print("Bot: Silakan tanyakan tentang:")
        print("- Jadwal")
        print("- Nilai")
        print("- Absensi")
        print("- Kegiatan")
        print("- Akademik")
        print("- Ujian")