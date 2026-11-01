import streamlit as st

st.set_page_config(
    page_title="Chatbot Akademik SMK",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 CHATBOT INFORMASI AKADEMIK SMK")
st.subheader("Selamat Datang di Layanan Informasi Akademik")

nama = st.text_input("Masukkan nama siswa")

if st.button("Mulai"):
    if nama.strip():
        st.success(f"Selamat datang, {nama}!")

        menu = st.selectbox(
            "Pilih informasi akademik",
            ["Jadwal Pelajaran", "Nilai Siswa", "Absensi", "Kegiatan Sekolah"]
        )

        st.info(f"Kamu memilih menu: {menu}")
    else:
        st.warning("Masukkan nama terlebih dahulu.")