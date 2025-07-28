import streamlit as st
import pandas as pd
import os
from PIL import Image
from decimal import Decimal, ROUND_HALF_UP

logo_path = "FAST_logo.png"  # or .jpg/.jpeg depending on your file
logo = Image.open(logo_path)
# === Set grading sheets directory ===
grading_dir = "grading_sheets"
universities = [f.replace(".xlsx", "") for f in os.listdir(grading_dir) if f.endswith(".xlsx")]

st.title("🎓 SGPA Calculator")
st.markdown(
    """
    <div style='font-size:20px; margin-top:-10px; margin-bottom:5px;'>
        Made by <strong>Insiya Fakhruddin Mandsaur</strong>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([0.35, 8])  # Narrow logo column

with col1:
    st.image("FAST_logo.png", width=32)  # Small but readable logo

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

st.write("")  # Adds a small vertical space


# === Step 1: Select University ===
universities = [
    "NED University", "FAST-NUCES", "COMSATS", "IBA",
    "GIKI", "LUMS", "NUST", "Habib University","Ziauddin University"
]

# Sort alphabetically
universities = sorted(universities)

# Dropdown
selected_uni = st.selectbox("Select your university", universities)


if selected_uni:
    # Load grading policy
    grading_path = os.path.join(grading_dir, f"{selected_uni}.xlsx")
    grade_df = pd.read_excel(grading_path)
    st.success(f"Grading policy loaded for {selected_uni}")

    # === Step 2: Number of Subjects ===
    num_subjects = st.number_input("How many subjects do you have?", min_value=1, max_value=20, step=1)

    # Lists to store inputs
    marks_list = []
    credit_list = []
    grade_input_list = []

    # Extract available grades from sheet
    available_grades = grade_df['Grade'].unique().tolist()

    st.subheader("Enter Subject Details")

    for i in range(num_subjects):
        st.markdown(f"### Subject {i+1}")
        col1, col2, col3 = st.columns([1, 1, 2])

        # Choose input type
        input_type = col1.radio("Input Type", ["Marks", "Grade"], key=f"type_{i}")

        # Based on input type, show appropriate field
        if input_type == "Marks":
            marks = col2.number_input("Marks Obtained", min_value=0.0, max_value=100.0, step=0.5, key=f"marks_{i}")
            grade_input = None
        else:
            grade_input = col2.selectbox("Select Grade", available_grades, key=f"grade_{i}")
            marks = None

        # Credit hours input
        credits = col3.number_input("Credit Hours", min_value=0.5, max_value=6.0, step=0.5, key=f"credits_{i}")

        # Append to lists
        marks_list.append(marks)
        grade_input_list.append(grade_input)
        credit_list.append(credits)

    # === GPA Conversion Functions ===
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

    # === SGPA Calculation ===

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

    # === Calculate Button ===
    if st.button("Calculate SGPA"):
        sgpa = calculate_sgpa(marks_list, grade_input_list, credit_list, grade_df)
        st.success(f"✅ Your SGPA is: {sgpa}")
