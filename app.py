import streamlit as st
import pandas as pd
import requests

# --- CONFIG ---
DATABASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTMvqtDGEsFiviYP0gOt-4oX0lgNj0y-kXtGxWrSqh0L1hBQ8XwZlUS6wtbUegI6RPmihvYkiVTeDtE/pub?gid=0&single=true&output=csv"  # your database CSV link
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwVUFmjJP-N-w8XOyQI6Kc_nKzbjWwNXZddgZChPiyRzIDliL0-hvP9zAoy4SrIXf8/exec"  # your Apps Script URL

# --- APP START ---
st.title("Survey Kepuasan Mahasiswa")

@st.cache_data
def load_database():
    df = pd.read_csv(DATABASE_SHEET_URL)
    df['NIM'] = df['NIM'].astype(str).str.strip()
    df['Matakuliah'] = df['Matakuliah'].astype(str).str.strip()
    return df

nim = st.text_input("Masukkan NIM Anda:")

if nim:
    df = load_database()
    student_courses = df[df["NIM"] == nim]

    if not student_courses.empty:
        st.success(f"Ditemukan {len(student_courses)} mata kuliah untuk NIM {nim}")
        st.write("Silakan isi survei:")

        all_filled = True  # track if everything is filled
        survey_data = []

        for _, row in student_courses.iterrows():
            course = row["Matakuliah"]
            st.markdown(f"<h3 style='color:#2E86C1'>{course}</h3>", unsafe_allow_html=True)
            
            q1 = st.selectbox("1. Dosen menguasai materi pembelajaran dengan baik dan mudah dipahami, menggunakan sumber-sumber referensi terbaru serta mengembangkan gagasan baru/inovatif",
                              options=["-", 1, 2, 3, 4, 5],
                              index=0,
                              key=f"{course}_q1"
                             )
            q2 = st.selectbox("2. Dosen menyampaikan materi kuliah secara sistematis dan mudah diikuti",
                              options=[1, 2, 3, 4, 5],
                              index=0,
                              key=f"{course}_q2"
                             )
            q3 = st.selectbox("3. Dosen menggunakan media pembelajaran dengan tepat dan menarik",
                              options=[1, 2, 3, 4, 5],
                              index=0,
                              key=f"{course}_q3"
                             )
            q4 = st.selectbox("4. Dosen membuka ruang diskusi dan interaksi dengan mahasiswa selama perkuliahan",
                              options=[1, 2, 3, 4, 5],
                              index=0,
                              key=f"{course}_q4"
                             )
            q5 = st.selectbox("5. Dosen memberikan umpan balik yang membangun terhadap hasil kerja mahasiswa",
                              options=[1, 2, 3, 4, 5],
                              index=0,
                              key=f"{course}_q5"
                             )
            q6 = st.selectbox("6. Secara umum, proses pembelajaran pada mata kuliah ini berjalan dengan baik",
                              options=[1, 2, 3, 4, 5],
                              index=0,
                              key=f"{course}_q6"
                             )

            # Check if any question is left blank
        if None in (q1, q2, q3, q4, q5, q6):
            all_filled = False
        
            survey_data.append({
                "nim": nim,
                "mataKuliah": course,
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "q4": q4,
                "q5": q5,
                "q6": q6
            })
        
    if not all_filled:
        st.warning("Harap isi semua pertanyaan sebelum mengirim.")
        st.button("Kirim Semua",disabled=True)
    else:
        if st.button("Kirim Semua"):
            res = requests.post(SCRIPT_URL, json=survey_data)
            if res.status_code == 200 and "OK" in res.text:
                st.success("Data berhasil dikirim!")
            else:
                st.error("Gagal mengirim data.")
else:
    st.warning("NIM tidak ditemukan dalam database.")
