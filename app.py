import streamlit as st
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="MLT Medical AI Assistant",
    page_icon="🔬",
    layout="wide"
)

# ============================================
# PROFESSIONAL DARK THEME CSS
# ============================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* ── Global background & font ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #0a0f1e !important;
    font-family: 'Sora', sans-serif !important;
    color: #cbd5e0 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton, .stAppDeployButton,
.viewerBadge_container__1QSob,
._profilePreview_gzau3_63 { display: none !important; }

/* ── Shimmer top bar ── */
[data-testid="stApp"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #11998e, #63b3ed, #9f7aea, #11998e);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
    z-index: 9999;
}
@keyframes shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* ── Main content area ── */
[data-testid="stAppViewContainer"] > .main .block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1100px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0d1526 !important;
    border-right: 1px solid rgba(17,153,142,0.2) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label { color: #cbd5e0 !important; }

/* Sidebar info boxes */
[data-testid="stSidebar"] .stAlert {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.25) !important;
    border-radius: 10px !important;
    color: #a0aec0 !important;
}

/* Sidebar file uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #141c2e !important;
    border: 1px dashed rgba(17,153,142,0.4) !important;
    border-radius: 10px !important;
}

/* ── Headings ── */
h1, h2, h3 { font-family: 'Sora', sans-serif !important; }

/* ── HEADER BANNER ── */
.mlt-banner {
    background: linear-gradient(135deg, #0d2e2b, #0d1a2e);
    border: 1px solid rgba(17,153,142,0.3);
    border-radius: 16px;
    padding: 24px 32px;
    text-align: center;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.mlt-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #11998e, #63b3ed, #9f7aea);
}
.mlt-banner h1 {
    color: #e2e8f0 !important;
    font-size: 28px !important;
    font-weight: 600 !important;
    margin: 0 0 6px !important;
}
.mlt-banner p {
    color: #11998e !important;
    font-size: 16px !important;
    margin: 0 !important;
}

/* ── Section headings ── */
.section-title {
    color: #11998e !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    margin: 8px 0 4px !important;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Divider ── */
hr { border-color: rgba(17,153,142,0.15) !important; margin: 20px 0 !important; }

/* ── Number input & Select box ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Sora', sans-serif !important;
}
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label { color: #a0aec0 !important; font-size: 13px !important; }

/* ── Multiselect ── */
[data-testid="stMultiSelect"] > div > div {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
[data-testid="stMultiSelect"] label { color: #a0aec0 !important; }
span[data-baseweb="tag"] {
    background: rgba(17,153,142,0.2) !important;
    border: 1px solid rgba(17,153,142,0.4) !important;
    border-radius: 6px !important;
    color: #11998e !important;
}

/* ── Text inputs ── */
[data-testid="stTextInput"] input {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Sora', sans-serif !important;
}
[data-testid="stTextInput"] input::placeholder { color: #4a5568 !important; }
[data-testid="stTextInput"] label { color: #a0aec0 !important; font-size: 13px !important; }
[data-testid="stTextInput"] input:focus {
    border-color: rgba(17,153,142,0.6) !important;
    box-shadow: none !important;
}

/* ── Buttons ── */
.stButton button {
    background: linear-gradient(135deg, #11998e, #0d7a71) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-size: 15px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #38ef7d, #11998e) !important;
    color: #0a0f1e !important;
    transform: translateY(-1px) !important;
}

/* ── Success cards (normal values) ── */
.stAlert[data-baseweb="notification"] {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.25) !important;
    border-left: 3px solid #11998e !important;
    border-radius: 12px !important;
    color: #a0aec0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.2) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #11998e !important;
    font-family: 'Sora', sans-serif !important;
}

/* ── Warning / info ── */
.stWarning {
    background: rgba(239,187,44,0.08) !important;
    border: 1px solid rgba(239,187,44,0.25) !important;
    border-radius: 10px !important;
    color: #f6c342 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.15) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 10px !important;
    color: #cbd5e0 !important;
    animation: fadeUp 0.25s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* User message slightly different */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #0d2035, #1a0d2e) !important;
    border-color: rgba(159,122,234,0.2) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #141c2e !important;
    border: 1px solid rgba(17,153,142,0.3) !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #e2e8f0 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #4a5568 !important; }
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(17,153,142,0.6) !important;
}

/* ── Footer ── */
.mlt-footer {
    text-align: center;
    padding: 14px;
    color: #e53e3e;
    font-size: 13px;
    background: rgba(229,62,62,0.06);
    border: 1px solid rgba(229,62,62,0.2);
    border-radius: 10px;
    margin-top: 10px;
}
.powered {
    text-align: center;
    font-size: 11px;
    color: #2d3748;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
    margin-top: 8px;
}

/* ── Feedback button inline ── */
.feedback-btn a button {
    background: #11998e !important;
    color: white !important;
    padding: 8px 16px !important;
    border: none !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    font-size: 13px !important;
    margin-bottom: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# MEDICAL AI PERSONALITY (unchanged)
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

RESPONSE FORMAT:
- Always start with greeting
- Give clear accurate information
- Use simple language
- Give WHO reference when possible
- Always end with: "Please consult a qualified doctor for proper diagnosis and treatment"

NEVER DO:
❌ Give wrong information
❌ Recommend specific medicines without mentioning doctor consultation
❌ Diagnose serious conditions
❌ Replace real doctor advice
❌ Give information not backed by WHO
"""

# ============================================
# SIDEBAR (unchanged logic, new style)
# ============================================

st.sidebar.markdown("<h2 style='color:#e2e8f0;font-family:Sora,sans-serif'>Zeeshan Ali</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#11998e'>🏥 Medical Lab Technology Student</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#a0aec0'>🎓 Riphah International University</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("<h3 style='color:#e2e8f0;font-family:Sora,sans-serif'>🔬 I can help with:</h3>", unsafe_allow_html=True)
helps = ["Lab Test Questions","Symptom Checking","Lab Report Analysis","Medical Terms","MLT Study Help","Health Questions","Medicine Info","Diet Advice","First Aid Help"]
for h in helps:
    st.sidebar.markdown(f"<p style='color:#a0aec0;margin:2px 0'>✅ {h}</p>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:#e2e8f0;font-family:Sora,sans-serif'>📊 Normal Values</h3>", unsafe_allow_html=True)
st.sidebar.info("🩸 Blood Sugar\nNormal: 70-100 mg/dL\nPre-diabetes: 100-125\nDiabetes: 126+")
st.sidebar.info("❤️ Blood Pressure\nNormal: 120/80\nHigh: 140/90+\nLow: 90/60-")
st.sidebar.info("🔬 Hemoglobin\nMen: 13.5-17.5 g/dL\nWomen: 12-15.5 g/dL\nLow = Anemia")
st.sidebar.info("🫀 Pulse Rate\nNormal: 60-100/min\nAthletes: 40-60/min")

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='color:#a0aec0'>📎 Upload Medical Report</p>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt","pdf","png","jpg","jpeg"], label_visibility="collapsed")
if uploaded_file is not None:
    st.sidebar.success(f"✅ {uploaded_file.name}")
    if uploaded_file.type.startswith("image"):
        st.sidebar.image(uploaded_file, width=150)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='color:#a0aec0'>⭐ Give Us Feedback!</p>", unsafe_allow_html=True)
st.sidebar.markdown("""
<a href="https://docs.google.com/forms/d/e/1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header" target="_blank">
<button style="background:linear-gradient(135deg,#11998e,#0d7a71);color:white;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;width:100%;font-size:15px;font-family:Sora,sans-serif;font-weight:500;">
📝 Give Feedback!
</button></a>""", unsafe_allow_html=True)

# ============================================
# MAIN PAGE HEADER
# ============================================

st.markdown("""
<div class="mlt-banner">
    <h1>🔬 MLT Medical AI Assistant</h1>
    <p>Your Personal Medical Guide — Available 24/7</p>
</div>""", unsafe_allow_html=True)

st.markdown("""
<a href="https://docs.google.com/forms/d/e/1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header" target="_blank">
<button style="background:linear-gradient(135deg,#11998e,#0d7a71);color:white;padding:8px 18px;border:none;border-radius:8px;cursor:pointer;font-size:13px;margin-bottom:14px;font-family:Sora,sans-serif;">
📝 Give Feedback!
</button></a>""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# PATIENT INFORMATION (unchanged logic)
# ============================================

st.markdown("<div class='section-title'>👤 Tell Us About Yourself!</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#718096;font-size:13px;margin-bottom:12px'>This helps us give better advice!</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Your Age", min_value=1, max_value=100, value=25)
with col2:
    gender = st.selectbox("Gender", ["Select", "Male", "Female"])
with col3:
    weight = st.number_input("Weight (kg)", min_value=1, max_value=200, value=70)

st.markdown("---")

# ============================================
# NORMAL VALUES CARDS (unchanged logic)
# ============================================

st.markdown("<div class='section-title'>📊 Quick Reference — Normal Values</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("🩸 **Blood Sugar**\nNormal: 70-100\nPre-diabetes: 100-125\nDiabetes: 126+")
with col2:
    st.success("❤️ **Blood Pressure**\nNormal: 120/80\nHigh: 140/90+\nLow: 90/60-")
with col3:
    st.success("🔬 **Hemoglobin**\nMen: 13.5-17.5\nWomen: 12-15.5\nLow = Anemia")
with col4:
    st.success("🫀 **Pulse Rate**\nNormal: 60-100\nAthletes: 40-60\nHigh: 100+")

st.markdown("---")

# ============================================
# SYMPTOM CHECKER (unchanged logic)
# ============================================

st.markdown("<div class='section-title'>🤒 Symptom Checker</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#718096;font-size:13px;margin-bottom:12px'>Select your symptoms and we will help!</p>", unsafe_allow_html=True)

symptoms = st.multiselect("What symptoms do you have?", [
    "Fever 🌡️","Headache 🤕","Chest Pain 💔","Stomach Pain 🤢","Fatigue 😴",
    "Cough 😷","Shortness of Breath 😮‍💨","Dizziness 😵","Nausea 🤮",
    "Joint Pain 🦴","Back Pain 😣","High Blood Sugar 🩸","High Blood Pressure ❤️",
    "Weight Loss ⚖️","Frequent Urination 🚽","Blurred Vision 👁️","Skin Problems 🩹",
    "Hair Loss 💇","Weakness 😩","Loss of Appetite 🍽️"
])

if st.button("🔍 Check My Symptoms!"):
    if symptoms:
        symptom_text = ", ".join(symptoms)
        patient_info = f"Patient is {age} years old {gender} weighing {weight}kg. " if gender != "Select" else ""
        message = f"{patient_info}I have these symptoms: {symptom_text}. What could be wrong and what should I do?"
        st.session_state.messages.append({"role": "user", "content": message})
    else:
        st.warning("Please select at least one symptom!")

st.markdown("---")

# ============================================
# LAB REPORT ANALYZER (unchanged logic)
# ============================================

st.markdown("<div class='section-title'>🔬 Lab Report Analyzer</div>", unsafe_allow_html=True)

with st.expander("📋 Click to Enter Your Lab Results!"):
    col1, col2 = st.columns(2)
    with col1:
        hemoglobin  = st.text_input("Hemoglobin (g/dL)")
        blood_sugar = st.text_input("Blood Sugar (mg/dL)")
        bp_systolic = st.text_input("Blood Pressure Systolic")
        wbc         = st.text_input("WBC Count")
        platelets   = st.text_input("Platelets")
    with col2:
        cholesterol  = st.text_input("Cholesterol (mg/dL)")
        bp_diastolic = st.text_input("Blood Pressure Diastolic")
        creatinine   = st.text_input("Creatinine")
        uric_acid    = st.text_input("Uric Acid")
        tsh          = st.text_input("TSH (Thyroid)")

    if st.button("🔍 Analyze My Lab Report!"):
        report_parts = []
        if hemoglobin:  report_parts.append(f"Hemoglobin: {hemoglobin} g/dL")
        if blood_sugar: report_parts.append(f"Blood Sugar: {blood_sugar} mg/dL")
        if bp_systolic and bp_diastolic: report_parts.append(f"Blood Pressure: {bp_systolic}/{bp_diastolic}")
        if wbc:         report_parts.append(f"WBC Count: {wbc}")
        if platelets:   report_parts.append(f"Platelets: {platelets}")
        if cholesterol: report_parts.append(f"Cholesterol: {cholesterol} mg/dL")
        if creatinine:  report_parts.append(f"Creatinine: {creatinine}")
        if uric_acid:   report_parts.append(f"Uric Acid: {uric_acid}")
        if tsh:         report_parts.append(f"TSH: {tsh}")

        if report_parts:
            patient_info = f"Patient is {age} years old {gender}. " if gender != "Select" else ""
            report_text  = "\n".join(report_parts)
            message = f"{patient_info}Please analyze these lab results and tell me if they are normal or not and what I should do:\n{report_text}"
            st.session_state.messages.append({"role": "user", "content": message})
        else:
            st.warning("Please enter at least one test result!")

st.markdown("---")

# ============================================
# CHAT SECTION (unchanged logic)
# ============================================

st.markdown("<div class='section-title'>💬 Chat With Medical AI</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick" not in st.session_state:
    st.session_state.quick = None

if st.session_state.quick:
    quick_q = st.session_state.quick
    st.session_state.quick = None
    with st.chat_message("user"):
        st.write(quick_q)
    st.session_state.messages.append({"role": "user", "content": quick_q})
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": medical_prompt}, *st.session_state.messages]
    )
    ai_reply = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.write(ai_reply)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask your medical question here... 🏥")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    patient_context = f"Patient is {age} years old {gender} weighing {weight}kg. " if gender != "Select" else ""
    full_message = patient_context + user_input
    st.session_state.messages.append({"role": "user", "content": full_message})
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": medical_prompt}, *st.session_state.messages]
    )
    ai_reply = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.write(ai_reply)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div class="mlt-footer">
    ⚠️ This AI is for information only! Always consult a real doctor!
</div>
<div class="powered">⚡ Powered by Voxora Technologies · MLT AI v2.0</div>
""", unsafe_allow_html=True)
