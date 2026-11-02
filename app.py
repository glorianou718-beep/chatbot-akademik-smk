import streamlit as st
import Database

st.set_page_config(
    page_title="Chatbot Informasi Akademik SMK",
    page_icon="🎓",
    layout="centered"
)

# Menyiapkan database
Database.buat_database()
Database.isi_data()

st.title("🎓 CHATBOT INFORMASI AKADEMIK SMK")
st.subheader("Selamat Datang di Layanan Informasi Akademik")
st.write("Silakan masukkan nama untuk melihat informasi akademik.")

# Memasukkan nama siswa
nama = st.text_input("Masukkan nama siswa")

if st.button("Mulai"):
    conn = Database.koneksi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_siswa, nama, nis, kelas
        FROM siswa
        WHERE LOWER(nama) = LOWER(?)
        """,
        (nama.strip(),)
    )

    siswa = cursor.fetchone()
    conn.close()

    if siswa:
        st.session_state["siswa_id"] = siswa["id_siswa"]
        st.session_state["nama"] = siswa["nama"]
        st.session_state["kelas"] = siswa["kelas"]
    else:
        st.error("Data siswa tidak ditemukan.")

# Menampilkan informasi siswa
if "siswa_id" in st.session_state:
    st.success(f"Selamat datang, {st.session_state['nama']}!")
    st.write(f"**Nama:** {st.session_state['nama']}")
    st.write(f"**Kelas:** {st.session_state['kelas']}")

    menu = st.selectbox(
        "Pilih informasi akademik",
        [
            "Pilih Menu",
            "Jadwal Pelajaran",
            "Nilai Akademik",
            "Absensi",
            "Kegiatan Sekolah"
        ]
    )

    conn = Database.koneksi_database()
    cursor = conn.cursor()

    if menu == "Jadwal Pelajaran":
        st.subheader("📚 Jadwal Pelajaran")

        cursor.execute("""
            SELECT hari, jam, mata_pelajaran, guru
            FROM jadwal
            WHERE kelas = ?
            ORDER BY
                CASE hari
                    WHEN 'Senin' THEN 1
                    WHEN 'Selasa' THEN 2
                    WHEN 'Rabu' THEN 3
                    WHEN 'Kamis' THEN 4
                    WHEN 'Jumat' THEN 5
                    WHEN 'Sabtu' THEN 6
                    ELSE 7
                END
        """, (st.session_state["kelas"],))

        data = cursor.fetchall()

        if data:
            st.table([dict(row) for row in data])
        else:
            st.info("Jadwal belum tersedia.")

    elif menu == "Nilai Akademik":
        st.subheader("📝 Nilai Akademik")

        cursor.execute("""
            SELECT mata_pelajaran, nilai
            FROM nilai
            WHERE id_siswa = ?
        """, (st.session_state["siswa_id"],))

        data = cursor.fetchall()

        if data:
            st.table([dict(row) for row in data])
            rata_rata = sum(row["nilai"] for row in data) / len(data)
            st.metric("Rata-rata Nilai", f"{rata_rata:.2f}")
        else:
            st.info("Nilai belum tersedia.")

    elif menu == "Absensi":
        st.subheader("📋 Rekap Absensi")

        cursor.execute("""
            SELECT status, COUNT(*) AS jumlah
            FROM absensi
            WHERE id_siswa = ?
            GROUP BY status
        """, (st.session_state["siswa_id"],))

        data = cursor.fetchall()
        rekap = {row["status"]: row["jumlah"] for row in data}

        hadir = rekap.get("Hadir", 0)
        izin = rekap.get("Izin", 0)
        sakit = rekap.get("Sakit", 0)
        alpa = rekap.get("Alpa", 0)

        total = hadir + izin + sakit + alpa
        persentase = (hadir / total * 100) if total > 0 else 0

        st.write(f"**Hadir:** {hadir}")
        st.write(f"**Izin:** {izin}")
        st.write(f"**Sakit:** {sakit}")
        st.write(f"**Alpa:** {alpa}")
        st.metric("Persentase Kehadiran", f"{persentase:.1f}%")

    elif menu == "Kegiatan Sekolah":
        st.subheader("🏫 Kegiatan Sekolah")

        cursor.execute("""
            SELECT nama_kegiatan, tanggal, tempat, keterangan
            FROM kegiatan
            ORDER BY tanggal
        """)

        data = cursor.fetchall()

        if data:
            for kegiatan in data:
                st.markdown(f"### {kegiatan['nama_kegiatan']}")
                st.write(f"📅 Tanggal: {kegiatan['tanggal']}")
                st.write(f"📍 Tempat: {kegiatan['tempat']}")
                st.write(f"Keterangan: {kegiatan['keterangan']}")
                st.divider()
        else:
            st.info("Belum ada kegiatan sekolah.")

    conn.close()
