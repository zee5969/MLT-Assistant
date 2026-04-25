import streamlit as st
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="MLT Assistant AI",
    page_icon="🔬"
)

# Hide Menu Footer Header
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# Sidebar Profile
st.sidebar.title("Zeeshan Ali")
st.sidebar.write("🏥 Medical Lab Technology Student")
st.sidebar.markdown("---")
st.sidebar.write("### 🔬 I can help with:")
st.sidebar.write("✅ Lab Test Questions")
st.sidebar.write("✅ Medical Terms")
st.sidebar.write("✅ MLT Study Help")
st.sidebar.write("✅ Health Questions")
st.sidebar.write("✅ Medicine Information")
st.sidebar.markdown("---")
st.sidebar.write("📎 Upload File")
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
st.sidebar.write("⭐ Give Us Feedback!")
st.sidebar.markdown(
    """
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header" 
    target="_blank">
    <button style="
        background-color: #0083B8;
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

# Medical AI Personality
medical_prompt = """
You are a Medical AI Assistant specialized in:
- Medical Laboratory Technology (MLT)
- Lab tests and their interpretations
- Medical terminology
- Human anatomy and physiology
- Common diseases and conditions
- Medicine information
- Health advice

You were created by Zeeshan Ali, an MLT student
at Riphah International University Islamabad.

Important rules:
- Always give accurate medical information
- Use simple and easy language
- Always recommend consulting a real doctor
  for serious medical issues
- Be friendly and helpful
"""

# Main Page
st.title("🔬 MLT Medical AI Assistant")

# Info visible on mobile
st.write("👨‍⚕️ **Created by Zeeshan Ali**")
st.write("🏥 MLT Student - Riphah International University Islamabad")

st.markdown("---")

# Feedback button visible on mobile
st.markdown(
    """
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header" 
    target="_blank">
    <button style="
        background-color: #0083B8;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
    ">
    📝 Give Feedback!
    </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.write("Ask me anything about medicine and health!")

# Quick Question Buttons
st.write("### Quick Questions:")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔬 CBC?"):
        st.session_state.quick = "What is CBC blood test?"
with col2:
    if st.button("💊 Medicines"):
        st.session_state.quick = "Tell me about common medicines"
with col3:
    if st.button("🧪 Lab tests"):
        st.session_state.quick = "What are common lab tests?"

st.markdown("---")

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

user_input = st.chat_input("Ask your medical question here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
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
