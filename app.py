import streamlit as st

st.set_page_config(
    page_title="Chatbot Informasi Akademik SMK",
    page_icon="🎓"
)

st.title("🎓 Chatbot Informasi Akademik SMK")
st.write("Selamat datang! Silakan masukkan nama kamu.")

nama = st.text_input("Nama siswa")

if st.button("Mulai"):
    if nama.strip():
        st.success(f"Halo, {nama}! Selamat datang di Chatbot Akademik SMK.")

        pertanyaan = st.selectbox(
            "Informasi apa yang ingin kamu lihat?",
            [
                "Pilih informasi",
                "Jadwal pelajaran",
                "Nilai siswa",
                "Absensi siswa",
                "Kegiatan sekolah"
            ]
        )

        if pertanyaan != "Pilih informasi":
            st.info(
                f"Kamu memilih informasi: {pertanyaan}. "
                "Data akademik perlu dihubungkan ke database agar dapat ditampilkan."
            )
    else:
        st.warning("Silakan masukkan nama terlebih dahulu.")
