import streamlit as st
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="MLT Medical AI Assistant",
    page_icon="🔬",
    layout="wide"
)

# Hide Menu Footer Header
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stButton button {
        background-color: #11998e;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        width: 100%;
    }

    .stButton button:hover {
        background-color: #38ef7d;
        color: black;
    }

    [data-testid="stSidebar"] {
        background-color: #0d4f47;
        color: white;
    }

    [data-testid="stSidebar"] p {
        color: white;
    }

    [data-testid="stSidebar"] h1 {
        color: white;
    }

    [data-testid="stSidebar"] h2 {
        color: white;
    }

    [data-testid="stSidebar"] h3 {
        color: white;
    }

    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.markdown(
    "<h2 style='color:white'>Zeeshan Ali</h2>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>🏥 Medical Lab Technology Student</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>🎓 Riphah International University</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

st.sidebar.markdown(
    "<h3 style='color:white'>🔬 I can help with:</h3>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ Lab Test Questions</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ Symptom Checking</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ Lab Report Analysis</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ Medical Terms</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ MLT Study Help</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ Health Questions</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ Medicine Info</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ Diet Advice</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:white'>✅ First Aid Help</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

st.sidebar.markdown(
    "<h3 style='color:white'>📊 Normal Values!</h3>",
    unsafe_allow_html=True
)
st.sidebar.info("""
🩸 Blood Sugar
Normal: 70-100 mg/dL
Pre-diabetes: 100-125
Diabetes: 126+
""")
st.sidebar.info("""
❤️ Blood Pressure
Normal: 120/80
High: 140/90+
Low: 90/60-
""")
st.sidebar.info("""
🔬 Hemoglobin
Men: 13.5-17.5 g/dL
Women: 12-15.5 g/dL
Low = Anemia
""")
st.sidebar.info("""
🫀 Pulse Rate
Normal: 60-100/min
Athletes: 40-60/min
""")
st.sidebar.markdown("---")

st.sidebar.markdown(
    "<p style='color:white'>📎 Upload Medical Report</p>",
    unsafe_allow_html=True
)
uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=["txt", "pdf", "png", "jpg", "jpeg"],
    label_visibility="collapsed"
)
if uploaded_file is not None:
    st.sidebar.success(f"✅ {uploaded_file.name}")
    if uploaded_file.type.startswith("image"):
        st.sidebar.image(uploaded_file, width=150)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:white'>⭐ Give Us Feedback!</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header" 
    target="_blank">
    <button style="
        background-color: #11998e;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        font-size: 16px;
    ">
    📝 Give Feedback!
    </button>
    </a>
    """,
    unsafe_allow_html=True
)

# ============================================
# MEDICAL AI PERSONALITY
# ============================================

medical_prompt = """
You are an advanced Medical AI Assistant
created by Zeeshan Ali, a Medical Lab Technology student at
Riphah International University Islamabad.

IMPORTANT RULES:
1. ALL information must be according to
   WHO (World Health Organization) guidelines
2. ALL lab values must follow
   international standard ranges
3. NEVER give wrong medical information
4. ALWAYS recommend seeing real doctor
5. Be extremely careful with dosages
6. Never recommend self medication
7. Always mention side effects of medicines

WHO STANDARD LAB VALUES:
- Blood Sugar (Fasting): 70-100 mg/dL
- Blood Sugar (Random): Less than 140 mg/dL
- HbA1c Normal: Less than 5.7%
- HbA1c Pre-diabetes: 5.7-6.4%
- HbA1c Diabetes: 6.5% or higher

- Blood Pressure Normal: Less than 120/80
- Blood Pressure Elevated: 120-129/less than 80
- High Blood Pressure Stage 1: 130-139/80-89
- High Blood Pressure Stage 2: 140+/90+
- Hypertensive Crisis: Higher than 180/120

- Hemoglobin Men: 13.5-17.5 g/dL
- Hemoglobin Women: 12.0-15.5 g/dL
- Hemoglobin Children: 11.0-16.0 g/dL

- WBC Count: 4,500-11,000 cells/mcL
- Platelets: 150,000-400,000/mcL
- RBC Men: 4.5-5.5 million/mcL
- RBC Women: 4.0-5.0 million/mcL

- Total Cholesterol: Less than 200 mg/dL
- LDL Cholesterol: Less than 100 mg/dL
- HDL Men: More than 40 mg/dL
- HDL Women: More than 50 mg/dL
- Triglycerides: Less than 150 mg/dL

- Creatinine Men: 0.7-1.2 mg/dL
- Creatinine Women: 0.5-1.0 mg/dL
- Uric Acid Men: 3.5-7.2 mg/dL
- Uric Acid Women: 2.6-6.0 mg/dL

- TSH Normal: 0.4-4.0 mIU/L
- T3 Normal: 80-200 ng/dL
- T4 Normal: 5.0-12.0 mcg/dL

- ALT Normal: 7-56 units/L
- AST Normal: 10-40 units/L
- Bilirubin Total: 0.1-1.2 mg/dL

- Pulse Rate Normal: 60-100 beats/min
- Respiratory Rate: 12-20 breaths/min
- Temperature Normal: 36.1-37.2°C
- Oxygen Saturation: 95-100%

WHO GUIDELINES TO FOLLOW:
1. Diabetes Management:
   - WHO diabetes diagnosis criteria
   - Lifestyle modifications first
   - Medication only on doctor advice

2. Hypertension Management:
   - WHO blood pressure guidelines 2023
   - DASH diet recommendations
   - Lifestyle changes importance

3. Anemia Management:
   - WHO anemia classification
   - Iron deficiency treatment
   - B12 and folate importance

4. Infection Control:
   - WHO infection prevention guidelines
   - Antibiotic stewardship
   - Never recommend antibiotics
     without doctor prescription

5. Nutrition:
   - WHO healthy diet guidelines
   - Balanced diet recommendations
   - Specific diet for conditions

RESPONSE FORMAT:
- Always start with greeting
- Give clear accurate information
- Use simple language
- Give WHO reference when possible
- Always end with:
  "Please consult a qualified doctor
   for proper diagnosis and treatment"

NEVER DO:
❌ Give wrong information
❌ Recommend specific medicines
   without mentioning doctor consultation
❌ Diagnose serious conditions
❌ Replace real doctor advice
❌ Give information not backed by WHO
"""

# ============================================
# MAIN PAGE
# ============================================

# Beautiful Green Header
st.markdown("""
    <div style="
        background: linear-gradient(
            to right,
            #11998e,
            #38ef7d
        );
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: Black;
        margin-bottom: 20px;
    ">
        <h1>MLT Medical AI Assistant</h1>
        <p style="font-size: 18px;">
        Your Personal Medical Guide - Available 24/7
        </p>
    </div>
""", unsafe_allow_html=True)

# Feedback button for mobile
st.markdown(
    """
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header" 
    target="_blank">
    <button style="
        background-color: #11998e;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        margin-bottom: 10px;
    ">
    📝 Give Feedback!
    </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================
# PATIENT INFORMATION
# ============================================

st.markdown("""
    <h3 style='color:#11998e'>
    👤 Tell Us About Yourself!
    </h3>
""", unsafe_allow_html=True)
st.write("This helps us give better advice!")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        "Your Age",
        min_value=1,
        max_value=100,
        value=25
    )

with col2:
    gender = st.selectbox(
        "Gender",
        ["Select", "Male", "Female"]
    )

with col3:
    weight = st.number_input(
        "Weight (kg)",
        min_value=1,
        max_value=200,
        value=70
    )

st.markdown("---")

# ============================================
# NORMAL VALUES CARDS
# ============================================

st.markdown("""
    <h3 style='color:#11998e'>
    📊 Quick Reference - Normal Values!
    </h3>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("""
    🩸 **Blood Sugar**
    Normal: 70-100
    Pre-diabetes: 100-125
    Diabetes: 126+
    """)

with col2:
    st.success("""
    ❤️ **Blood Pressure**
    Normal: 120/80
    High: 140/90+
    Low: 90/60-
    """)

with col3:
    st.success("""
    🔬 **Hemoglobin**
    Men: 13.5-17.5
    Women: 12-15.5
    Low = Anemia
    """)

with col4:
    st.success("""
    🫀 **Pulse Rate**
    Normal: 60-100
    Athletes: 40-60
    High: 100+
    """)

st.markdown("---")

# ============================================
# SYMPTOM CHECKER
# ============================================

st.markdown("""
    <h3 style='color:#11998e'>
    🤒 Symptom Checker!
    </h3>
""", unsafe_allow_html=True)
st.write("Select your symptoms and we will help!")

symptoms = st.multiselect(
    "What symptoms do you have?",
    [
        "Fever 🌡️",
        "Headache 🤕",
        "Chest Pain 💔",
        "Stomach Pain 🤢",
        "Fatigue 😴",
        "Cough 😷",
        "Shortness of Breath 😮‍💨",
        "Dizziness 😵",
        "Nausea 🤮",
        "Joint Pain 🦴",
        "Back Pain 😣",
        "High Blood Sugar 🩸",
        "High Blood Pressure ❤️",
        "Weight Loss ⚖️",
        "Frequent Urination 🚽",
        "Blurred Vision 👁️",
        "Skin Problems 🩹",
        "Hair Loss 💇",
        "Weakness 😩",
        "Loss of Appetite 🍽️"
    ]
)

if st.button("🔍 Check My Symptoms!"):
    if symptoms:
        symptom_text = ", ".join(symptoms)
        patient_info = ""
        if gender != "Select":
            patient_info = f"Patient is {age} years old {gender} weighing {weight}kg. "

        message = f"{patient_info}I have these symptoms: {symptom_text}. What could be wrong and what should I do?"

        st.session_state.messages.append({
            "role": "user",
            "content": message
        })
    else:
        st.warning("Please select at least one symptom!")

st.markdown("---")

# ============================================
# LAB REPORT ANALYZER
# ============================================

st.markdown("""
    <h3 style='color:#11998e'>
    🔬 Lab Report Analyzer!
    </h3>
""", unsafe_allow_html=True)
st.write("Enter your test results and we will explain them!")

with st.expander("📋 Click to Enter Your Lab Results!"):
    col1, col2 = st.columns(2)

    with col1:
        hemoglobin = st.text_input("Hemoglobin (g/dL)")
        blood_sugar = st.text_input("Blood Sugar (mg/dL)")
        bp_systolic = st.text_input("Blood Pressure Systolic")
        wbc = st.text_input("WBC Count")
        platelets = st.text_input("Platelets")

    with col2:
        cholesterol = st.text_input("Cholesterol (mg/dL)")
        bp_diastolic = st.text_input("Blood Pressure Diastolic")
        creatinine = st.text_input("Creatinine")
        uric_acid = st.text_input("Uric Acid")
        tsh = st.text_input("TSH (Thyroid)")

    if st.button("🔍 Analyze My Lab Report!"):
        report_parts = []

        if hemoglobin:
            report_parts.append(f"Hemoglobin: {hemoglobin} g/dL")
        if blood_sugar:
            report_parts.append(f"Blood Sugar: {blood_sugar} mg/dL")
        if bp_systolic and bp_diastolic:
            report_parts.append(f"Blood Pressure: {bp_systolic}/{bp_diastolic}")
        if wbc:
            report_parts.append(f"WBC Count: {wbc}")
        if platelets:
            report_parts.append(f"Platelets: {platelets}")
        if cholesterol:
            report_parts.append(f"Cholesterol: {cholesterol} mg/dL")
        if creatinine:
            report_parts.append(f"Creatinine: {creatinine}")
        if uric_acid:
            report_parts.append(f"Uric Acid: {uric_acid}")
        if tsh:
            report_parts.append(f"TSH: {tsh}")

        if report_parts:
            patient_info = ""
            if gender != "Select":
                patient_info = f"Patient is {age} years old {gender}. "

            report_text = "\n".join(report_parts)
            message = f"{patient_info}Please analyze these lab results and tell me if they are normal or not and what I should do:\n{report_text}"

            st.session_state.messages.append({
                "role": "user",
                "content": message
            })
        else:
            st.warning("Please enter at least one test result!")

st.markdown("---")

# ============================================
# CHAT SECTION
# ============================================

st.markdown("""
    <h3 style='color:#11998e'>
    💬 Chat With Medical AI!
    </h3>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick" not in st.session_state:
    st.session_state.quick = None

if st.session_state.quick:
    quick_q = st.session_state.quick
    st.session_state.quick = None

    with st.chat_message("user"):
        st.write(quick_q)

    st.session_state.messages.append({
        "role": "user",
        "content": quick_q
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": medical_prompt},
            *st.session_state.messages
        ]
    )

    ai_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input(
    "Ask your medical question here... 🏥"
)

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    patient_context = ""
    if gender != "Select":
        patient_context = f"Patient is {age} years old {gender} weighing {weight}kg. "

    full_message = patient_context + user_input

    st.session_state.messages.append({
        "role": "user",
        "content": full_message
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": medical_prompt},
            *st.session_state.messages
        ]
    )

    ai_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
    <div style="
        text-align: center;
        color: Red;
        padding: 10px;
    ">
        <p>⚠️ This AI is for information only!</p>
             <p>Always consult a real doctor!</p>
    </div>
""", unsafe_allow_html=True)
