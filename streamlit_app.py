import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("Model_Random_Forest_Classifier.joblib")

# Helper functions
def convert_yes_no(value):
    return 1 if value == 'Yes' else 0

def convert_gender(value):
    return 1 if value == 'Man' else 0

def convert_marital_status(value):
    mapping = {
        'Single': 1,
        'Married': 2,
        'Widower': 3,
        'Divorced': 4,
        'Facto Union': 5,
        'Legally Separated': 6
    }
    return mapping.get(value, 0)

# Sidebar Input
st.sidebar.title("🔍 Prediksi Dropout Siswa")

gender = convert_gender(st.sidebar.radio("Jenis Kelamin", ['Man', 'Woman']))
marital_status = convert_marital_status(st.sidebar.selectbox("Status Pernikahan",
                ['Single', 'Married', 'Widower', 'Divorced', 'Facto Union', 'Legally Separated']))
age = st.sidebar.slider("Usia saat enrollment", 10, 100, 18)

debtor = convert_yes_no(st.sidebar.radio("Memiliki hutang?", ['Yes', 'No']))
fees_up_to_date = convert_yes_no(st.sidebar.radio("Pembayaran Terkini Lunas?", ['Yes', 'No']))
scholarship = convert_yes_no(st.sidebar.radio("Penerima Beasiswa?", ['Yes', 'No']))
displaced = convert_yes_no(st.sidebar.radio("Dari keluarga kurang mampu?", ['Yes', 'No']))

st.sidebar.markdown("### Data Akademik")
sem1_credited = st.sidebar.number_input("SKS Semester 1 (Kredit)", 0)
sem2_credited = st.sidebar.number_input("SKS Semester 2 (Kredit)", 0)
sem1_enrolled = st.sidebar.number_input("SKS Semester 1 (Enrolled)", 0)
sem2_enrolled = st.sidebar.number_input("SKS Semester 2 (Enrolled)", 0)
sem1_approved = st.sidebar.number_input("SKS Semester 1 (Approved)", 0)
sem2_approved = st.sidebar.number_input("SKS Semester 2 (Approved)", 0)
sem1_grade = st.sidebar.number_input("Nilai Semester 1", 0.0)
sem2_grade = st.sidebar.number_input("Nilai Semester 2", 0.0)

# Prediksi
if st.sidebar.button("🔍 Prediksi"):
    data_pred = pd.DataFrame([[
        marital_status, displaced, debtor, fees_up_to_date, gender,
        scholarship, age, sem1_credited, sem2_credited, sem1_enrolled,
        sem2_enrolled, sem1_approved, sem2_approved, sem1_grade, sem2_grade
    ]], columns=[
        'Marital_status', 'Displaced', 'Debtor', 'Tuition_fees_up_to_date',
        'Gender', 'Scholarship_holder', 'Age_at_enrollment',
        'Curricular_units_1st_sem_credited', 'Curricular_units_2nd_sem_credited',
        'Curricular_units_1st_sem_enrolled', 'Curricular_units_2nd_sem_enrolled',
        'Curricular_units_1st_sem_approved', 'Curricular_units_2nd_sem_approved',
        'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade'
    ])

    result = model.predict(data_pred)

    if result[0] == 0:
        st.success("✅ Siswa tidak dropout.")
        st.balloons()
    else:
        st.error("⚠️ Siswa berpotensi dropout.")

# Halaman Utama
st.title("🎓 Jaya Jaya Institut - Prediksi Dropout")
st.markdown("""
Selamat datang di sistem prediksi dropout **Jaya Jaya Institut**.  
Gunakan panel di sebelah kiri untuk memasukkan data siswa dan lakukan prediksi.
""")

st.subheader("📌 Cara Kerja Sistem:")
st.write("""
- Isi data siswa pada sidebar  
- Klik tombol **Prediksi**  
- Hasil prediksi akan tampil di halaman ini
""")
