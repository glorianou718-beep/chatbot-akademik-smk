
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).parent / "akademik.db"


def koneksi_database():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def buat_database():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            id_siswa INTEGER PRIMARY KEY AUTOINCREMENT,
            nis TEXT UNIQUE,
            nama TEXT,
            kelas TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jadwal (
            id_jadwal INTEGER PRIMARY KEY AUTOINCREMENT,
            hari TEXT,
            jam TEXT,
            mata_pelajaran TEXT,
            guru TEXT,
            kelas TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai (
            id_nilai INTEGER PRIMARY KEY AUTOINCREMENT,
            id_siswa INTEGER,
            mata_pelajaran TEXT,
            nilai REAL,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS absensi (
            id_absensi INTEGER PRIMARY KEY AUTOINCREMENT,
            id_siswa INTEGER,
            tanggal TEXT,
            status TEXT,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kegiatan (
            id_kegiatan INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_kegiatan TEXT,
            tanggal TEXT,
            tempat TEXT,
            keterangan TEXT
        )
    """)

    conn.commit()
    conn.close()


def isi_data():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO siswa (nis, nama, kelas)
        VALUES (?, ?, ?)
    """, ("12345", "Gloria", "XI RPL"))

    siswa = cursor.execute("""
        SELECT id_siswa FROM siswa WHERE nis = ?
    """, ("12345",)).fetchone()

    id_siswa = siswa["id_siswa"]

    if cursor.execute("SELECT COUNT(*) FROM jadwal").fetchone()[0] == 0:
        jadwal = [
            ("Senin", "07.00 - 08.30", "Pemrograman Python", "Bapak Andi", "XI RPL"),
            ("Senin", "08.30 - 10.00", "Basis Data", "Ibu Sinta", "XI RPL"),
            ("Senin", "10.30 - 12.00", "Sistem Informasi", "Bapak Rudi", "XI RPL"),
            ("Selasa", "07.00 - 08.30", "Bahasa Indonesia", "Ibu Maria", "XI RPL"),
            ("Selasa", "08.30 - 10.00", "Matematika", "Bapak Yanto", "XI RPL"),
            ("Selasa", "10.30 - 12.00", "Jaringan Komputer", "Bapak Anton", "XI RPL")
        ]

        cursor.executemany("""
            INSERT INTO jadwal
            (hari, jam, mata_pelajaran, guru, kelas)
            VALUES (?, ?, ?, ?, ?)
        """, jadwal)

    if cursor.execute("SELECT COUNT(*) FROM nilai").fetchone()[0] == 0:
        nilai = [
            (id_siswa, "Pemrograman Python", 85),
            (id_siswa, "Basis Data", 88),
            (id_siswa, "Sistem Informasi", 90),
            (id_siswa, "Jaringan Komputer", 87)
        ]

        cursor.executemany("""
            INSERT INTO nilai (id_siswa, mata_pelajaran, nilai)
            VALUES (?, ?, ?)
        """, nilai)

    if cursor.execute("SELECT COUNT(*) FROM absensi").fetchone()[0] == 0:
        absensi = [
            (id_siswa, "2026-10-01", "Hadir"),
            (id_siswa, "2026-10-02", "Hadir"),
            (id_siswa, "2026-10-03", "Hadir"),
            (id_siswa, "2026-10-04", "Izin"),
            (id_siswa, "2026-10-05", "Sakit")
        ]

        cursor.executemany("""
            INSERT INTO absensi (id_siswa, tanggal, status)
            VALUES (?, ?, ?)
        """, absensi)

    if cursor.execute("SELECT COUNT(*) FROM kegiatan").fetchone()[0] == 0:
        kegiatan = [
            ("Upacara Bendera", "2026-10-05", "Lapangan Sekolah",
             "Upacara rutin hari Senin"),
            ("Ujian Tengah Semester", "2026-10-10", "Ruang Kelas",
             "Ujian Tengah Semester"),
            ("Kegiatan Olahraga", "2026-10-15", "Lapangan Sekolah",
             "Kegiatan olahraga siswa")
        ]

        cursor.executemany("""
            INSERT INTO kegiatan
            (nama_kegiatan, tanggal, tempat, keterangan)
            VALUES (?, ?, ?, ?)
        """, kegiatan)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    buat_database()
    isi_data()
    print("Database berhasil dibuat!")
    print("Data contoh berhasil dimasukkan!")
