import streamlit as st
import pandas as pd
import os
from PIL import Image
from decimal import Decimal, ROUND_HALF_UP
import base64

# === Background Video Function ===
def get_video_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode()

video_base64 = get_video_base64("media/background.mp4")

# === Background Styling with Video and Overlay ===
st.markdown(
    f"""
    <style>
    .stApp {{
        background: transparent;
    }}

    .block-container {{
        position: relative;
        z-index: 0;
        color: #ffffff;
    }}

    #video-background {{
        position: fixed;
        top: 0;
        left: 0;
        min-width: 100%;
        min-height: 100%;
        object-fit: cover;
        z-index: -3;
    }}

    .video-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.65); /* Darker overlay */
        z-index: -2;
    }}

    /* Headings */
    .block-container h1,
    .block-container h2,
    .block-container h3 {{
        color: #2dd4bf !important;
    }}

    /* General input labels */
    label,
    .stSelectbox > div,
    .stNumberInput > div {{
        color: #ffffff !important;
    }}

    /* Corrected radio group labels like 'Marks' and 'Grades' */
    div.row-widget.stRadio > div:first-child {{
        color: #ffffff !important;  /* Change to #2dd4bf if you want teal */
        font-weight: bold !important;
        font-size: 16px;
    }}

    /* Individual radio options */
    .stRadio > div > label,
    .stRadio > div > div > label,
    .stRadio label span {{
        color: #ffffff !important;
        font-weight: 600;
    }}

    /* Calculate SGPA Button */
    div.stButton > button {{
        background-color: #2dd4bf;
        font-weight: 700;
        font-size: 16px;
        padding: 0.6em 1.2em;
        border: none;
        border-radius: 8px;
        transition: background-color 0.3s ease;
        color: #000000;  /* Black text */
    }}

    div.stButton > button:hover {{
        background-color: #20c997;
        transform: scale(1.03);
    }}

    /* SGPA Result box */
    .custom-sgpa-result {{
        background-color: #2dd4bf;
        color: white;
        border-left: 5px solid #ffffff;
        padding: 1em;
        border-radius: 8px;
        font-weight: 800;
        font-size: 20px;
        margin-top: 1em;
    }}
    
    .stRadio .st-emotion-cache-bvleps p{{
        color: #808080 
    }}
    
    </style>

    <video autoplay muted loop id="video-background">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    <div class="video-overlay"></div>
    """,
    unsafe_allow_html=True
)


# === Load Logo ===
logo_path = "FAST_logo.png"
logo = Image.open(logo_path)

# === Load Available Grading Sheets ===
grading_dir = "grading_sheets"
universities = [f.replace(".xlsx", "") for f in os.listdir(grading_dir) if f.endswith(".xlsx")]

# === Title & Author ===
st.title("\U0001F393 SGPA Calculator")
st.markdown(
    """
    <div style='font-size:20px; margin-top:-10px; margin-bottom:5px; color:white;'>
        Made by <strong style="color:#2dd4bf;">Insiya Fakhruddin Mandsaur</strong>
    </div>
    """,
    unsafe_allow_html=True
)

# === Header Layout ===
col1, col2 = st.columns([0.35, 8])
with col1:
    st.image("FAST_logo.png", width=32)

with col2:
    st.markdown(
        """
        <div style='display: flex; align-items: center; height: 100%;'>
            <span style='font-size: 15px;'>
                Bachelor's in Artificial Intelligence – <strong>Batch of 2026</strong>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# === Step 1: Select University ===
universities = [
    "NED University", "FAST-NUCES", "COMSATS", "IBA",
    "GIKI", "LUMS", "NUST", "Habib University", "Ziauddin University"
]
universities = sorted(universities)
selected_uni = st.selectbox("Select your university", universities)

if selected_uni:
    grading_path = os.path.join(grading_dir, f"{selected_uni}.xlsx")
    grade_df = pd.read_excel(grading_path)
    st.success(f"Grading policy loaded for {selected_uni}")

    num_subjects = st.number_input("How many subjects do you have?", min_value=1, max_value=20, step=1)
    marks_list = []
    credit_list = []
    grade_input_list = []
    available_grades = grade_df['Grade'].unique().tolist()

    st.subheader("Enter Subject Details")

    for i in range(num_subjects):
        st.markdown(f"### Subject {i+1}")
        col1, col2, col3 = st.columns([1, 1, 2])
        input_type = col1.radio("Input Type", ["Marks", "Grade"], key=f"type_{i}")

        if input_type == "Marks":
            marks = col2.number_input("Marks Obtained", min_value=0.0, max_value=100.0, step=0.5, key=f"marks_{i}")
            grade_input = None
        else:
            grade_input = col2.selectbox("Select Grade", available_grades, key=f"grade_{i}")
            marks = None

        credits = col3.number_input("Credit Hours", min_value=0.5, max_value=6.0, step=0.5, key=f"credits_{i}")

        marks_list.append(marks)
        grade_input_list.append(grade_input)
        credit_list.append(credits)

    def marks_to_gpa(marks, df):
        for _, row in df.iterrows():
            if row['Min Marks'] <= marks <= row['Max Marks']:
                return row['GPA']
        return 0.0

    def grade_to_gpa(grade, df):
        row = df[df['Grade'] == grade]
        if not row.empty:
            return float(row['GPA'].values[0])
        return 0.0

    def calculate_sgpa(marks_list, grade_list, credit_list, df):
        total_points = Decimal('0')
        total_credits = Decimal('0')

        for m, g, c in zip(marks_list, grade_list, credit_list):
            credit = Decimal(str(c))
            if g:
                gpa = Decimal(str(grade_to_gpa(g, df)))
            else:
                gpa = Decimal(str(marks_to_gpa(m, df)))

            total_points += gpa * credit
            total_credits += credit

        if total_credits == 0:
            return 0.0

        sgpa = total_points / total_credits
        return float(sgpa.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    if st.button("Calculate SGPA"):
        sgpa = calculate_sgpa(marks_list, grade_input_list, credit_list, grade_df)
        st.markdown(
            f"""
            <div class="custom-sgpa-result">
                ✅ Your SGPA is: {sgpa}
            </div>
            """,
            unsafe_allow_html=True
        )