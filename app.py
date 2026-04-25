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

# Round Picture Style
st.sidebar.markdown("""
    <style>
    [data-testid="stSidebar"] img {
        border-radius: 50%;
        border: 3px solid #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Profile
st.sidebar.image("https://avatars.githubusercontent.com/zee5969", width=100)
st.sidebar.title("Zeeshan Ali")
st.sidebar.write("🏥 Medical Lab Technology Student")
st.sidebar.write("🎓 Riphah International University")
st.sidebar.write("📍 Islamabad, Pakistan")
st.sidebar.markdown("---")

# What Bot Can Help With
st.sidebar.write("### 🔬 I can help with:")
st.sidebar.write("✅ Lab Test Questions")
st.sidebar.write("✅ Medical Terms")
st.sidebar.write("✅ MLT Study Help")
st.sidebar.write("✅ Health Questions")
st.sidebar.write("✅ Medicine Info")
st.sidebar.markdown("---")

# Upload File
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
- If asked non medical questions
  answer them too but focus on medical topics
"""

# Main Chatbot
st.title("🔬 MLT Medical AI Assistant")
st.write("Ask me anything about medicine and health!")

# Quick Question Buttons
st.write("### Quick Questions:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔬 What is CBC?"):
        st.session_state.quick = "What is CBC blood test?"

with col2:
    if st.button("💊 Common medicines"):
        st.session_state.quick = "Tell me about common medicines"

with col3:
    if st.button("🧪 Lab tests"):
        st.session_state.quick = "What are common lab tests?"

st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick" not in st.session_state:
    st.session_state.quick = None

# Handle quick questions
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
        messages=st.session_state.messages,
        system=medical_prompt
    )

    ai_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat Input
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
        messages=st.session_state.messages,
        system=medical_prompt
    )

    ai_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
