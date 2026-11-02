
import streamlit as st
import Database

# Konfigurasi halaman
st.set_page_config(
    page_title="Chatbot Informasi Akademik SMK",
    page_icon="🎓",
    layout="wide"
)

# Membuat database dan mengisi data contoh
Database.buat_database()
Database.isi_data()


# Mengambil data siswa
def cari_siswa(nis):
    conn = Database.koneksi_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM siswa WHERE nis = ?",
        (nis,)
    )

    siswa = cursor.fetchone()
    conn.close()
    return siswa


# Tampilan utama
st.title("🎓 Chatbot Informasi Akademik SMK")
st.write("Selamat datang di layanan informasi akademik sekolah.")
st.divider()

# Sidebar
st.sidebar.title("📚 Menu Akademik")
menu = st.sidebar.radio(
    "Pilih informasi:",
    [
        "Beranda",
        "Jadwal Pelajaran",
        "Nilai Akademik",
        "Absensi",
        "Kegiatan Sekolah"
    ]
)

# Login siswa
st.subheader("👩‍🎓 Identitas Siswa")
nis = st.text_input("Masukkan NIS siswa", placeholder="Contoh: 12345")

if nis:
    siswa = cari_siswa(nis)

    if siswa is None:
        st.error("Data siswa tidak ditemukan. Periksa kembali NIS.")
    else:
        st.success(f"Selamat datang, {siswa['nama']}!")
        st.info(f"Kelas: {siswa['kelas']}")

        id_siswa = siswa["id_siswa"]

        if menu == "Beranda":
            st.subheader("🏫 Beranda Akademik")
            st.write(
                "Silakan pilih menu di sebelah kiri "
                "untuk melihat informasi akademik."
            )

            col1, col2, col3 = st.columns(3)
            col1.metric("Nama Siswa", siswa["nama"])
            col2.metric("NIS", siswa["nis"])
            col3.metric("Kelas", siswa["kelas"])

        elif menu == "Jadwal Pelajaran":
            st.subheader("📅 Jadwal Pelajaran")

            conn = Database.koneksi_database()
            data = conn.execute("""
                SELECT hari, jam, mata_pelajaran, guru, kelas
                FROM jadwal
                ORDER BY
                CASE hari
                    WHEN 'Senin' THEN 1
                    WHEN 'Selasa' THEN 2
                    WHEN 'Rabu' THEN 3
                    WHEN 'Kamis' THEN 4
                    WHEN 'Jumat' THEN 5
                    WHEN 'Sabtu' THEN 6
                    ELSE 7
                END, jam
            """).fetchall()
            conn.close()

            if data:
                st.table([dict(row) for row in data])
            else:
                st.warning("Jadwal belum tersedia.")

        elif menu == "Nilai Akademik":
            st.subheader("📝 Nilai Akademik")

            conn = Database.koneksi_database()
            data = conn.execute("""
                SELECT mata_pelajaran, nilai
                FROM nilai
                WHERE id_siswa = ?
            """, (id_siswa,)).fetchall()
            conn.close()

            if data:
                st.table([dict(row) for row in data])

                rata_rata = sum(row["nilai"] for row in data) / len(data)
                st.metric("Rata-rata Nilai", f"{rata_rata:.2f}")
            else:
                st.warning("Nilai belum tersedia.")

        elif menu == "Absensi":
            st.subheader("📋 Informasi Absensi")

            conn = Database.koneksi_database()
            data = conn.execute("""
                SELECT status, COUNT(*) AS jumlah
                FROM absensi
                WHERE id_siswa = ?
                GROUP BY status
            """, (id_siswa,)).fetchall()
            conn.close()

            jumlah_absensi = {
                "Hadir": 0,
                "Izin": 0,
                "Sakit": 0,
                "Alpa": 0
            }

            for row in data:
                jumlah_absensi[row["status"]] = row["jumlah"]

            total = sum(jumlah_absensi.values())
            persentase = (
                jumlah_absensi["Hadir"] / total * 100
                if total > 0 else 0
            )

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Hadir", jumlah_absensi["Hadir"])
            col2.metric("Izin", jumlah_absensi["Izin"])
            col3.metric("Sakit", jumlah_absensi["Sakit"])
            col4.metric("Alpa", jumlah_absensi["Alpa"])

            st.metric("Persentase Kehadiran", f"{persentase:.1f}%")

        elif menu == "Kegiatan Sekolah":
            st.subheader("🎉 Kegiatan Sekolah")

            conn = Database.koneksi_database()
            data = conn.execute("""
                SELECT nama_kegiatan, tanggal, tempat, keterangan
                FROM kegiatan
                ORDER BY tanggal
            """).fetchall()
            conn.close()

            if data:
                for kegiatan in data:
                    with st.container(border=True):
                        st.markdown(f"### {kegiatan['nama_kegiatan']}")
                        st.write("📅 Tanggal:", kegiatan["tanggal"])
                        st.write("📍 Tempat:", kegiatan["tempat"])
                        st.write("ℹ️ Keterangan:", kegiatan["keterangan"])
            else:
                st.warning("Belum ada kegiatan sekolah.")

else:
    st.info("Masukkan NIS terlebih dahulu untuk melihat informasi akademik.")

st.divider()
st.caption("Chatbot Informasi Akademik SMK | Berbasis Python dan SQLite")
