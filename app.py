import streamlit as st
import pandas as pd
import requests

# --- CONFIG ---
DATABASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-XXX/pub?gid=0&single=true&output=csv"  # your database CSV link
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwVUFmjJP-N-w8XOyQI6Kc_nKzbjWwNXZddgZChPiyRzIDliL0-hvP9zAoy4SrIXf8/exec"  # your Apps Script URL

# --- APP START ---
st.title("Survey Kepuasan Mahasiswa")

@st.cache_data
def load_database():
    df = pd.read_csv(DATABASE_SHEET_URL)
    df['NIM'] = df['NIM'].astype(str).str.strip()
    df['Mata Kuliah'] = df['Mata Kuliah'].astype(str).str.strip()
    return df

nim = st.text_input("Masukkan NIM Anda:")

if nim:
    df = load_database()
    student_courses = df[df["NIM"] == nim]

    if not student_courses.empty:
        st.success(f"Ditemukan {len(student_courses)} mata kuliah untuk NIM {nim}")
        st.write("Silakan isi survei:")

        survey_data = []

        for _, row in student_courses.iterrows():
            course = row["Mata Kuliah"]
            st.markdown(f"### {course}")
            cols = st.columns(6)
            q1 = cols[0].number_input(f"Q1 ({course})", 1, 5, 3, key=f"{course}_q1")
            q2 = cols[1].number_input(f"Q2 ({course})", 1, 5, 3, key=f"{course}_q2")
            q3 = cols[2].number_input(f"Q3 ({course})", 1, 5, 3, key=f"{course}_q3")
            q4 = cols[3].number_input(f"Q4 ({course})", 1, 5, 3, key=f"{course}_q4")
            q5 = cols[4].number_input(f"Q5 ({course})", 1, 5, 3, key=f"{course}_q5")
            q6 = cols[5].number_input(f"Q6 ({course})", 1, 5, 3, key=f"{course}_q6")

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

        if st.button("Kirim Semua"):
            res = requests.post(SCRIPT_URL, json=survey_data)
            if res.status_code == 200 and "OK" in res.text:
                st.success("Data berhasil dikirim!")
            else:
                st.error("Gagal mengirim data.")
    else:
        st.warning("NIM tidak ditemukan dalam database.")
