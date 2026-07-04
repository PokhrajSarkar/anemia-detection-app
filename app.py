import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from database import (
    initialize_database, verify_login, register_doctor,
    get_all_doctors, delete_doctor, save_patient_record,
    get_all_records, get_doctor_records, delete_record, delete_all_records
)

# Page configuration
st.set_page_config(
    page_title='Anaemia Detection System',
    page_icon='🩸',
    layout='wide'
)

# Initialize database on startup
initialize_database()

# Load both models
model_no_hb = joblib.load('anemia_model_no_hb.pkl')
model_with_hb = joblib.load('anemia_model_with_hb.pkl')

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# ── LOGIN PAGE ──
def show_login():
    st.markdown("""
        <style>
        .stButton > button {
            background: linear-gradient(90deg, #1E88E5, #1565C0) !important;
            color: white !important;
            border-radius: 8px !important;
            height: 50px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0px 4px 12px rgba(30, 136, 229, 0.4) !important;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #1565C0, #0D47A1) !important;
            box-shadow: 0px 6px 16px rgba(30, 136, 229, 0.6) !important;
            transform: translateY(-2px) !important;
        }
        .stTextInput > div > div > input {
            border-radius: 8px !important;
            height: 45px !important;
            font-size: 16px !important;
            border: 1.5px solid #1E88E5 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 40px 0px 20px 0px;'>
                <h1 style='color: #1E88E5; font-size: 36px; font-weight: 800;'>🩸 Anaemia Detection System</h1>
                <p style='color: #666; font-size: 16px;'>Hospital Clinical Decision Support System</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('---')
        username = st.text_input('👤 Username', placeholder='Enter your username')
        password = st.text_input('🔒 Password', type='password', placeholder='Enter your password')
        st.markdown('<br>', unsafe_allow_html=True)

        if st.button('Login', use_container_width=True):
            if not username or not password:
                st.error('⚠️ Please enter both username and password.')
            else:
                user = verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error('❌ Invalid username or password.')

        st.markdown('---')
        st.markdown("""
            <div style='text-align: center; color: #999; font-size: 13px;'>
                For access, contact your system administrator.
            </div>
        """, unsafe_allow_html=True)

# ── MAIN APP ──
def show_app():
    st.markdown("""
        <style>
        .main {
            background-color: #f0f4f8;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E88E5 0%, #1565C0 100%);
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: white !important;
            font-size: 16px !important;
        }
        .stButton > button {
            background: linear-gradient(90deg, #1E88E5, #1565C0) !important;
            color: white !important;
            border-radius: 10px !important;
            height: 48px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0px 4px 12px rgba(30, 136, 229, 0.4) !important;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #1565C0, #0D47A1) !important;
            box-shadow: 0px 6px 16px rgba(30, 136, 229, 0.6) !important;
            transform: translateY(-2px) !important;
        }
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            border-radius: 8px !important;
            border: 1.5px solid #1E88E5 !important;
            font-size: 15px !important;
        }
        [data-testid="stMetric"] {
            background: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
            border-left: 4px solid #1E88E5;
        }
        h1 {
            color: #1565C0 !important;
            font-weight: 800 !important;
        }
        h2, h3 {
            color: #1E88E5 !important;
        }
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.image('logo.png', width=80)
    st.sidebar.title('Anaemia Detection')
    st.sidebar.markdown(f"👤 **{st.session_state.user['full_name']}**")
    st.sidebar.markdown(f"🏥 Role: **{st.session_state.user['role'].capitalize()}**")
    st.sidebar.markdown('---')

    # Navigation based on role
    if st.session_state.user['role'] == 'admin':
        page = st.sidebar.radio('Navigation', [
            '🔬 Prediction',
            '📋 Patient Records',
            '📊 Analytics',
            '👨‍⚕️ Manage Doctors'
        ])
    else:
        page = st.sidebar.radio('Navigation', [
            '🔬 Prediction',
            '📋 Patient Records',
            '📊 Analytics'
        ])

    st.sidebar.markdown('---')
    if st.sidebar.button('🚪 Logout'):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.sidebar.info('Always consult a doctor for final diagnosis.')

    # ── PREDICTION PAGE ──
    if page == '🔬 Prediction':
        st.title('🔬 Anaemia Prediction')
        st.markdown('Fill in the patient details below and click **Predict** to get the result.')
        st.markdown('---')

        mode = st.radio('Select Mode', ['Screening Mode (Without HB)', 'Clinical Mode (With HB)'], horizontal=True)
        st.markdown('---')

        st.subheader('Patient Information')
        col1, col2, col3 = st.columns(3)
        with col1:
            patient_name = st.text_input('Patient Name')
        with col2:
            patient_id = st.text_input('Patient ID')
        with col3:
            age = st.number_input('Age (in months)', min_value=1, max_value=120, value=12)

        gender = st.radio('Gender', ['Male', 'Female'], horizontal=True)

        st.markdown('---')
        st.subheader('Clinical Observations')

        col4, col5 = st.columns(2)
        with col4:
            conjunctival = st.selectbox('Conjunctival Pallor', ['ABSENT', 'BORDERLINE', 'PRESENT'])
            tongue = st.selectbox('Tongue Pallor', ['ABSENT', 'BORDERLINE', 'PRESENT'])
            nailbed = st.selectbox('Nailbed Pallor', ['ABSENT', 'BORDERLINE', 'PRESENT'])
            palmar = st.selectbox('Palmar Pallor', ['ABSENT', 'BORDERLINE', 'PRESENT'])

        with col5:
            mcv = st.selectbox('MCV', ['1A (Normal)', '1B (Low)', '1C (High)'])
            mch = st.selectbox('MCH', ['2A (Normal)', '2B (Low)', '2C (High)'])
            mchc = st.selectbox('MCHC', ['3A (Normal)', '3B (Low)', '3C (High)'])
            rdw = st.selectbox('RDW', ['4A (Normal)', '4C (High)'])
            ps = st.selectbox('Peripheral Smear', ['1 (Normal)', '2 (Microcytic)', '3 (Dimorphic)', '2,3 (Mixed)'])
            if mode == 'Clinical Mode (With HB)':
                hb = st.number_input('Haemoglobin HB (g/dl)', min_value=1.0, max_value=20.0, value=10.0, step=0.1)

        st.markdown('---')

        if st.button('🔍 Predict Anaemia', use_container_width=True):
            if not patient_name:
                st.error('Please enter patient name.')
            elif not patient_id:
                st.error('Please enter patient ID.')
            else:
                pallor_map = {'ABSENT': 0, 'BORDERLINE': 1, 'PRESENT': 2}
                mcv_map = {'1A (Normal)': 1, '1B (Low)': 2, '1C (High)': 3}
                mch_map = {'2A (Normal)': 1, '2B (Low)': 2, '2C (High)': 3}
                mchc_map = {'3A (Normal)': 1, '3B (Low)': 2, '3C (High)': 3}
                rdw_map = {'4A (Normal)': 1, '4C (High)': 2}
                ps_map = {'1 (Normal)': 1, '2 (Microcytic)': 2, '3 (Dimorphic)': 3, '2,3 (Mixed)': 4}
                gender_map = {'Male': 1, 'Female': 0}

                if mode == 'Screening Mode (Without HB)':
                    input_data = pd.DataFrame({
                        'AGE': [age],
                        'CONJUNCTIVAL_ENCODED': [pallor_map[conjunctival]],
                        'TONGUE_ENCODED': [pallor_map[tongue]],
                        'NAILBED_ENCODED': [pallor_map[nailbed]],
                        'PALMAR_ENCODED': [pallor_map[palmar]],
                        'GENDER_ENCODED': [gender_map[gender]],
                        'PS_ENCODED': [ps_map[ps]],
                        'MCV_ENCODED': [mcv_map[mcv]],
                        'MCH_ENCODED': [mch_map[mch]],
                        'MCHC_ENCODED': [mchc_map[mchc]],
                        'RDW_ENCODED': [rdw_map[rdw]]
                    })
                    prediction = model_no_hb.predict(input_data)[0]
                    proba = model_no_hb.predict_proba(input_data)[0]
                else:
                    input_data = pd.DataFrame({
                        'AGE': [age],
                        'HB (g/dl)': [hb],
                        'CONJUNCTIVAL_ENCODED': [pallor_map[conjunctival]],
                        'TONGUE_ENCODED': [pallor_map[tongue]],
                        'NAILBED_ENCODED': [pallor_map[nailbed]],
                        'PALMAR_ENCODED': [pallor_map[palmar]],
                        'GENDER_ENCODED': [gender_map[gender]],
                        'PS_ENCODED': [ps_map[ps]],
                        'MCV_ENCODED': [mcv_map[mcv]],
                        'MCH_ENCODED': [mch_map[mch]],
                        'MCHC_ENCODED': [mchc_map[mchc]],
                        'RDW_ENCODED': [rdw_map[rdw]]
                    })
                    prediction = model_with_hb.predict(input_data)[0]
                    proba = model_with_hb.predict_proba(input_data)[0]

                confidence = round(max(proba) * 100, 1)

                st.markdown('---')
                st.subheader('Prediction Result')

                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    if prediction == 'No Anemia':
                        st.success(f'### ✅ {prediction}')
                    elif prediction == 'Mild':
                        st.warning(f'### ⚠️ {prediction} Anaemia')
                    elif prediction == 'Moderate':
                        st.warning(f'### ⚠️ {prediction} Anaemia')
                    elif prediction == 'Severe':
                        st.error(f'### 🚨 {prediction} Anaemia')

                with col_r2:
                    st.metric('Confidence Score', f'{confidence}%')
                    st.metric('Mode Used', mode.split('(')[0].strip())
                    st.metric('Doctor', st.session_state.user['full_name'])

                record = {
                    'Patient Name': patient_name,
                    'Patient ID': patient_id,
                    'Age (months)': age,
                    'Gender': gender,
                    'Mode': 'Screening' if mode == 'Screening Mode (Without HB)' else 'Clinical',
                    'Prediction': prediction,
                    'Confidence': f'{confidence}%',
                    'Doctor': st.session_state.user['username'],
                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                save_patient_record(record)
                st.success('✅ Record saved to database successfully!')

    # ── PATIENT RECORDS PAGE ──
    elif page == '📋 Patient Records':
        st.title('📋 Patient Records')
        st.markdown('---')

        if st.session_state.user['role'] == 'admin':
            records_df = get_all_records()
        else:
            records_df = get_doctor_records(st.session_state.user['username'])

        if len(records_df) == 0:
            st.info('No records found.')
        else:
            search = st.text_input('🔍 Search by Patient Name or ID')
            if search:
                records_df = records_df[
                    records_df['patient_name'].str.contains(search, case=False, na=False) |
                    records_df['patient_id'].str.contains(search, case=False, na=False)
                ]

            st.dataframe(records_df, use_container_width=True)

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.metric('Total Records', len(records_df))
            with col_d2:
                st.metric('Anaemia Cases', len(records_df[records_df['prediction'] != 'No Anemia']))

            csv = records_df.to_csv(index=False)
            st.download_button('📥 Download as CSV', data=csv, file_name='patient_records.csv', mime='text/csv')

            st.markdown('---')
            st.subheader('Manage Records')

            col_m1, col_m2 = st.columns(2)

            with col_m1:
                if st.session_state.user['role'] == 'admin':
                    if st.button('🗑️ Clear All Records', type='secondary', use_container_width=True):
                        delete_all_records()
                        st.success('All records cleared!')
                        st.rerun()

            with col_m2:
                record_options = [
                    f"ID:{row['id']} - {row['patient_name']} ({row['prediction']})"
                    for _, row in records_df.iterrows()
                ]
                selected = st.selectbox('Select record to delete', record_options)
                if st.button('🗑️ Delete Selected Record', type='secondary', use_container_width=True):
                    record_id = int(selected.split(':')[1].split(' ')[0])
                    delete_record(record_id)
                    st.success('Record deleted!')
                    st.rerun()

    # ── ANALYTICS PAGE ──
    elif page == '📊 Analytics':
        st.title('📊 Analytics Dashboard')
        st.markdown('---')

        if st.session_state.user['role'] == 'admin':
            records_df = get_all_records()
        else:
            records_df = get_doctor_records(st.session_state.user['username'])

        if len(records_df) == 0:
            st.info('No records yet. Make some predictions first.')
        else:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric('Total Patients', len(records_df))
            with col2:
                st.metric('Anaemia Cases', len(records_df[records_df['prediction'] != 'No Anemia']))
            with col3:
                st.metric('Severe Cases', len(records_df[records_df['prediction'] == 'Severe']))
            with col4:
                st.metric('No Anemia', len(records_df[records_df['prediction'] == 'No Anemia']))

            st.markdown('---')

            col_c1, col_c2 = st.columns(2)

            with col_c1:
                st.subheader('Prediction Distribution')
                fig1, ax1 = plt.subplots()
                records_df['prediction'].value_counts().plot(kind='bar', ax=ax1, color='steelblue')
                ax1.set_xlabel('Anaemia Category')
                ax1.set_ylabel('Count')
                plt.tight_layout()
                st.pyplot(fig1)

            with col_c2:
                st.subheader('Gender Distribution')
                fig2, ax2 = plt.subplots()
                records_df['gender'].value_counts().plot(kind='pie', ax=ax2, autopct='%1.1f%%')
                ax2.set_ylabel('')
                plt.tight_layout()
                st.pyplot(fig2)

    # ── MANAGE DOCTORS PAGE (ADMIN ONLY) ──
    elif page == '👨‍⚕️ Manage Doctors':
        st.title('👨‍⚕️ Manage Doctors')
        st.markdown('---')

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader('Register New Doctor')
            full_name = st.text_input('Full Name')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            confirm_password = st.text_input('Confirm Password', type='password')

            if st.button('Register Doctor', use_container_width=True):
                if not full_name or not username or not password:
                    st.error('Please fill in all fields.')
                elif password != confirm_password:
                    st.error('Passwords do not match.')
                elif len(password) < 6:
                    st.error('Password must be at least 6 characters.')
                else:
                    success = register_doctor(full_name, username, password)
                    if success:
                        st.success(f'Doctor {full_name} registered successfully!')
                    else:
                        st.error('Username already exists. Choose a different one.')

        with col_b:
            st.subheader('Registered Doctors')
            doctors = get_all_doctors()
            if doctors:
                doctors_df = pd.DataFrame(doctors)
                st.dataframe(doctors_df[['full_name', 'username', 'created_at']], use_container_width=True)

                st.markdown('---')
                doctor_options = [f"{d['full_name']} ({d['username']})" for d in doctors]
                selected_doctor = st.selectbox('Select doctor to remove', doctor_options)
                if st.button('🗑️ Remove Doctor', type='secondary', use_container_width=True):
                    username_to_delete = selected_doctor.split('(')[1].replace(')', '')
                    delete_doctor(username_to_delete)
                    st.success('Doctor removed successfully!')
                    st.rerun()
            else:
                st.info('No doctors registered yet.')

# ── MAIN FLOW ──
if st.session_state.logged_in:
    show_app()
else:
    show_login()