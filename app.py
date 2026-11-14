import csv
import datetime
import hashlib
import hmac
import os
import re
import secrets as pysecrets
import time

import requests
import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MLT Medical AI Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# VISUAL THEME — HIGH-CONTRAST CLINICAL DESIGN
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --navy: #10243A;
        --navy-2: #183B56;
        --teal: #0D9488;
        --ink: #17212B;
        --body: #263442;
        --muted: #526273;
        --line: #D8E1E8;
        --page: #F4F7FA;
        --white: #FFFFFF;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background: var(--page) !important;
        color: var(--ink) !important;
    }

    /* Make default Streamlit text readable on the light canvas. */
    .stApp p, .stApp li, .stApp label, .stApp span,
    .stApp [data-testid="stMarkdownContainer"] {
        color: var(--body);
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp h5, .stApp h6 {
        color: var(--navy) !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
    }

    [data-testid="stHeader"] {
        background: rgba(244, 247, 250, 0.98) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--navy) !important;
        border-right: 1px solid rgba(255,255,255,.12);
    }
    [data-testid="stSidebar"] * {
        color: #F3F7FB !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #C6D4E0 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.20) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
        color: #E8F0F6 !important;
    }

    .brand-mark {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 18px 0;
    }
    .brand-icon {
        width: 54px;
        height: 54px;
        flex: 0 0 54px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #18A999, #176B87);
        color: #FFFFFF !important;
        font-size: 26px;
        box-shadow: 0 8px 22px rgba(13,148,136,.25);
    }
    .brand-name {
        font-family: 'Manrope', sans-serif;
        color: #FFFFFF !important;
        font-size: 18px;
        line-height: 1.2;
        font-weight: 800;
    }
    .brand-sub {
        color: #C6D4E0 !important;
        font-size: 10px;
        margin-top: 5px;
        letter-spacing: .09em;
        text-transform: uppercase;
    }

    /* Hero */
    .hero {
        background: linear-gradient(120deg, #10243A 0%, #174D68 58%, #0D817D 100%);
        border-radius: 22px;
        padding: 30px 34px;
        color: #FFFFFF !important;
        margin: 4px 0 24px 0;
        box-shadow: 0 14px 34px rgba(16,36,58,.13);
    }
    .hero-eyebrow {
        color: #C8F1EB !important;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: 9px;
    }
    .hero h1 {
        color: #FFFFFF !important;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(26px, 3vw, 38px);
        font-weight: 800;
        line-height: 1.15;
        margin: 0 0 10px 0;
    }
    .hero .hero-title, .stApp .hero .hero-title {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(26px, 3vw, 38px);
        font-weight: 800;
        line-height: 1.15;
        margin: 0 0 10px 0;
    }
    .hero p {
        color: #F0F7FA !important;
        font-size: 15px;
        margin: 0;
        max-width: 760px;
        line-height: 1.65;
    }

    .section-heading {
        color: #10243A !important;
        font-family: 'Manrope', sans-serif;
        font-size: 21px;
        font-weight: 800;
        margin: 8px 0 4px 0;
    }
    .section-subtitle {
        color: #526273 !important;
        font-size: 13px;
        margin-bottom: 16px;
    }

    /* Cards */
    .info-card {
        background: #FFFFFF !important;
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        padding: 17px 18px;
        min-height: 108px;
        box-shadow: 0 4px 14px rgba(16,36,58,.045);
    }
    .info-card .card-label {
        color: #526273 !important;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .info-card .card-value {
        color: #10243A !important;
        font-family: 'Manrope', sans-serif;
        font-size: 17px;
        font-weight: 800;
        overflow-wrap: anywhere;
    }
    .info-card .card-note {
        color: #526273 !important;
        font-size: 11px;
        margin-top: 5px;
    }

    /* Buttons */
    .stButton > button, .stLinkButton > a, [data-testid="stFormSubmitButton"] button {
        border-radius: 11px !important;
        border: 1px solid #C9D6DF !important;
        font-weight: 700 !important;
        min-height: 42px;
        color: #183246 !important;
        background: #FFFFFF !important;
        transition: all .15s ease;
    }
    .stButton > button:hover, .stLinkButton > a:hover {
        border-color: #0D9488 !important;
        color: #08766F !important;
        background: #F0FBF9 !important;
    }
    .stButton > button[kind="primary"],
    [data-testid="stFormSubmitButton"] button[kind="primary"] {
        background: linear-gradient(100deg, #176B87, #0D9488) !important;
        border: 0 !important;
        color: #FFFFFF !important;
    }
    .stButton > button[kind="primary"] *,
    [data-testid="stFormSubmitButton"] button[kind="primary"] * {
        color: #FFFFFF !important;
    }

    /* Chat: explicitly set text colour to prevent pale/near-white messages. */
    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1px solid #DCE5EB !important;
        border-radius: 16px !important;
        padding: 15px 17px !important;
        margin-bottom: 11px !important;
        box-shadow: 0 3px 12px rgba(16,36,58,.035);
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em {
        color: #202B36 !important;
        opacity: 1 !important;
        line-height: 1.7 !important;
    }
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] h4 {
        color: #10243A !important;
    }

    /* Chat input — light, readable input rather than a dark/low-contrast field. */
    [data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border: 1px solid #C9D6DF !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 16px rgba(16,36,58,.06) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #17212B !important;
        -webkit-text-fill-color: #17212B !important;
        background: #FFFFFF !important;
        caret-color: #0D9488 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #526273 !important;
        -webkit-text-fill-color: #526273 !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInput"] button {
        color: #FFFFFF !important;
        background: #176B87 !important;
        border-radius: 10px !important;
    }

    /* Forms and standard inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input,
    .stSelectbox [data-baseweb="select"] > div {
        color: #17212B !important;
        background: #FFFFFF !important;
        border-color: #C9D6DF !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #657586 !important;
        opacity: 1 !important;
    }
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stRadio label, .stForm label {
        color: #263442 !important;
        font-weight: 600 !important;
    }

    [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #D8E1E8 !important;
        border-radius: 14px !important;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: #172B3A !important;
    }
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #D8E1E8 !important;
        padding: 14px;
        border-radius: 14px;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #172B3A !important;
    }

    .disclaimer {
        background: #FFF8E9;
        border: 1px solid #EAD39D;
        color: #634713 !important;
        border-radius: 12px;
        padding: 13px 16px;
        font-size: 12px;
        line-height: 1.6;
        margin-top: 18px;
    }
    .disclaimer strong, .disclaimer p {
        color: #634713 !important;
    }
    .footer {
        color: #526273 !important;
        text-align: center;
        font-size: 11px;
        padding: 22px 0 8px 0;
    }

    /* =====================================================
       FONT-COLOUR CONTRAST FIXES
       ===================================================== */

    /* Sidebar headings (Navigation, Developer, Learning areas) were navy on a
       navy sidebar — make them white. */
    .stApp [data-testid="stSidebar"] h1,
    .stApp [data-testid="stSidebar"] h2,
    .stApp [data-testid="stSidebar"] h3,
    .stApp [data-testid="stSidebar"] h4,
    .stApp [data-testid="stSidebar"] h5,
    .stApp [data-testid="stSidebar"] h6 {
        color: #FFFFFF !important;
    }

    /* Sidebar buttons have a white background, so their label must be dark
       (it was inheriting the light sidebar text colour = white on white). */
    .stApp [data-testid="stSidebar"] .stButton > button,
    .stApp [data-testid="stSidebar"] .stButton > button *,
    .stApp [data-testid="stSidebar"] .stLinkButton > a,
    .stApp [data-testid="stSidebar"] .stLinkButton > a * {
        color: #183246 !important;
    }
    .stApp [data-testid="stSidebar"] .stButton > button:hover,
    .stApp [data-testid="stSidebar"] .stButton > button:hover *,
    .stApp [data-testid="stSidebar"] .stLinkButton > a:hover,
    .stApp [data-testid="stSidebar"] .stLinkButton > a:hover * {
        color: #08766F !important;
    }

    /* Hero title stays white on the dark gradient. */
    .stApp .hero h1 {
        color: #FFFFFF !important;
    }

    /* Main-page buttons: dark label on white, white label on primary. */
    .stApp [data-testid="stMain"] .stButton > button p,
    .stApp [data-testid="stMain"] .stLinkButton > a p {
        color: #183246 !important;
    }
    .stApp [data-testid="stMain"] .stButton > button:hover p {
        color: #08766F !important;
    }
    .stApp [data-testid="stMain"] .stButton > button[kind="primary"] p,
    .stApp [data-testid="stFormSubmitButton"] button[kind="primary"] p {
        color: #FFFFFF !important;
    }

    /* Header / toolbar icons on the light header bar. */
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] a,
    [data-testid="stHeader"] svg {
        color: #17212B !important;
        fill: #17212B;
    }

    /* Links in body text and chat answers. */
    .stApp [data-testid="stMain"] [data-testid="stMarkdownContainer"] a {
        color: #0B6B8A !important;
    }

    /* Inline code, tables and quotes inside chat answers. */
    [data-testid="stChatMessage"] :not(pre) > code {
        color: #0B5C57 !important;
    }
    [data-testid="stChatMessage"] table th,
    [data-testid="stChatMessage"] table td,
    [data-testid="stChatMessage"] blockquote,
    [data-testid="stChatMessage"] blockquote p {
        color: #202B36 !important;
    }
    [data-testid="stChatMessage"] table th {
        color: #10243A !important;
        font-weight: 700 !important;
    }

    /* Alerts (st.info / st.warning / st.error). */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] li,
    [data-testid="stAlert"] span {
        color: #1F2A37 !important;
    }

    /* Widget labels and input text (form page). */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: #263442 !important;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        -webkit-text-fill-color: #17212B !important;
    }
    .stSelectbox [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] input {
        color: #17212B !important;
        -webkit-text-fill-color: #17212B !important;
    }

    /* Selectbox dropdown list: dark text needs a light list background
       (the only non-font-colour line, required for readable options). */
    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] [role="listbox"] {
        background: #FFFFFF !important;
    }
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] li *,
    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] [role="option"] * {
        color: #17212B !important;
    }

    /* Spinner / progress text on the light page. */
    [data-testid="stSpinner"] p,
    [data-testid="stSpinner"] span {
        color: #263442 !important;
    }

    /* Alerts: always a light box with dark text, in light or dark mode. */
    [data-testid="stAlert"],
    [data-testid="stAlert"] > div,
    [data-testid="stAlertContainer"],
    [data-testid="stAlert"] [data-baseweb="notification"] {
        background: #EAF2F8 !important;
        border-color: #C5D8E6 !important;
    }
    [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]),
    [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) > div,
    [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) [data-testid="stAlertContainer"],
    [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) [data-baseweb="notification"] {
        background: #FFF8E9 !important;
        border-color: #EAD39D !important;
    }
    [data-testid="stAlert"]:has([data-testid="stAlertContentError"]),
    [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) > div,
    [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) [data-testid="stAlertContainer"],
    [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) [data-baseweb="notification"] {
        background: #FDECEC !important;
        border-color: #F2B8B5 !important;
    }
    [data-testid="stAlert"] *:not(svg):not(path) {
        color: #1F2A37 !important;
    }

    /* Select boxes (any Streamlit version): white box, dark text. */
    [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border-color: #C9D6DF !important;
    }
    [data-baseweb="select"] *,
    [data-testid="stSelectbox"] * {
        color: #17212B !important;
        -webkit-text-fill-color: #17212B !important;
    }
    [data-baseweb="select"] svg {
        fill: #526273 !important;
    }

    /* Bottom bar behind the chat input: match the light page. */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: #F4F7FA !important;
    }

    /* AI provider selector (replaces the old AI Engine card). */
    .provider-label {
        color: #526273 !important;
        font-size: 12px;
        font-weight: 700;
        margin: 4px 0 6px 2px;
    }
    .provider-note {
        color: #526273 !important;
        font-size: 11px;
        margin: 6px 0 0 2px;
        overflow-wrap: anywhere;
    }

    /* Thumbs up / down feedback under answers. */
    [data-testid="stFeedback"] button,
    [data-testid="stFeedback"] button * {
        color: #526273 !important;
    }
    [data-testid="stFeedback"] button:hover,
    [data-testid="stFeedback"] button:hover * {
        color: #0D9488 !important;
    }

    /* Download button (admin area). */
    .stDownloadButton > button {
        border-radius: 11px !important;
        border: 1px solid #C9D6DF !important;
        background: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .stApp .stDownloadButton > button,
    .stApp .stDownloadButton > button * {
        color: #183246 !important;
    }

    /* Sign-in / Create account tabs. */
    button[data-baseweb="tab"] p,
    button[role="tab"] p {
        color: #263442 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p,
    button[role="tab"][aria-selected="true"] p {
        color: #0B6B8A !important;
    }
    [data-baseweb="tab-highlight"] {
        background-color: #0D9488 !important;
    }

    /* Remove the Fork / GitHub / Deploy toolbar and the menu. */
    [data-testid="stToolbar"],
    [data-testid="stToolbarActions"],
    [data-testid="stAppDeployButton"],
    [data-testid="stMainMenu"],
    [data-testid="stDecoration"],
    .stDeployButton,
    .stAppDeployButton,
    .viewerBadge_container__r5tak,
    [class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
    }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# APPLICATION CONFIGURATION
# =========================================================
CREATOR_NAME = "Zeeshan Ali"
FEEDBACK_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header"
)

# AI providers the visitor can choose from. Models can be changed with the
# GROQ_MODEL / OPENAI_MODEL environment variables or Streamlit secrets.
def get_secret(name):
    """Read a value from Streamlit Secrets, then from environment variables."""
    value = None
    try:
        value = st.secrets.get(name)
    except Exception:
        pass
    return value or os.getenv(name)


PROVIDERS = {
    "Groq": {"model": get_secret("GROQ_MODEL") or "openai/gpt-oss-20b"},
    "OpenAI": {"model": get_secret("OPENAI_MODEL") or "gpt-5-mini"},
}

SYSTEM_PROMPT = """
You are the MLT Medical AI Assistant, an educational assistant focused primarily
on Medical Laboratory Technology (MLT), laboratory medicine, and biomedical science.

CREATOR
If asked who created, developed, built, or made you, answer:
"I was developed by Zeeshan Ali, a Medical Laboratory Technology student and
AI enthusiast. This project combines MLT education with artificial intelligence
to support students and learners in understanding laboratory science."
Do not claim the creator is a doctor, physician, hospital, or medical institution.

CORE SUBJECT AREAS
- Hematology and blood banking / transfusion science
- Clinical chemistry / clinical biochemistry
- Medical microbiology and parasitology
- Histopathology and cytopathology
- Immunology and serology
- Molecular diagnostics, PCR, genetics, and laboratory techniques
- Quality control, quality assurance, biosafety, and laboratory management
- Specimen collection, handling, processing, and rejection criteria
- MLT examinations, revision notes, viva questions, and MCQs

RESPONSE STYLE — ANSWER ONLY WHAT IS ASKED
- Answer exactly what the user asked, directly, in the first sentence.
- Do not add background, extra sections, related topics, examples, or
  explanations the user did not ask for. Do not explain on your own.
- Keep answers short by default. A direct question gets a direct answer
  (1 to 4 sentences, or one short list or table only if the question needs it).
- Give a detailed explanation (principle, procedure, clinical significance,
  limitations, etc.) only when the user clearly asks to explain, describe in
  detail, or prepare notes or steps. Even then, cover only what was asked.
- Do not add introductions, summaries, repeated questions, or closing offers
  such as "would you like to know more". Ask a question back only if the
  request is truly unclear.
- Use simple, student-friendly language.
- For MCQs: if asked to create them, give four options, mark the correct
  answer, and add a one-line reason. If asked to answer one, give the correct
  option and a one-line reason.
- Do not invent references, guideline quotations, citations, or laboratory ranges.
- If something is uncertain or context-dependent, say so in one short sentence.

LABORATORY RESULTS AND REFERENCE INTERVALS
- Reference intervals vary by laboratory, method, instrument, age, sex, pregnancy
  status, population, and clinical context.
- Prefer the interval printed on the user's own laboratory report.
- Never diagnose based on one value alone.
- Explain possible interpretations cautiously and identify when clinician review
  is important.
- Do not describe every reference value as a universal WHO standard.

MEDICAL SAFETY
- You are an educational AI tool, not a doctor or diagnostic service.
- Do not diagnose or claim certainty about a disease.
- Do not prescribe medicines, recommend changing doses, or advise stopping
  prescribed treatment.
- Do not interpret symptoms as a confirmed diagnosis.
- For emergency warning signs (such as severe chest pain, severe breathing
  difficulty, stroke signs, unconsciousness, or severe bleeding), advise seeking
  emergency medical care immediately.
- Only if a user shares names, phone numbers, addresses, identity numbers, or
  other identifying information from a medical report, remind them not to.
  Do not add this reminder otherwise.
- Do not claim to have inspected an uploaded file unless its contents are actually
  provided to you in the conversation.

Keep the assistant's identity focused on MLT education and laboratory science.
"""

# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "provider" not in st.session_state:
    st.session_state.provider = "Groq"
if "feedback_sent" not in st.session_state:
    st.session_state.feedback_sent = set()

# =========================================================
# AI CLIENTS & RESPONSE
# =========================================================
def get_ai_response(conversation):
    """Send the conversation to the selected provider and return the reply."""
    provider = st.session_state.get("provider", "Groq")
    model = PROVIDERS[provider]["model"]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *conversation]

    if provider == "OpenAI" and not IS_PAID:
        raise RuntimeError("OpenAI is available to paid members only. Please choose Groq.")

    if provider == "OpenAI":
        api_key = get_secret("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured. Add it to Streamlit Secrets "
                "or your environment variables."
            )
        from openai import OpenAI  # imported here so Groq still works without it

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_completion_tokens=4000,
        )
    else:
        api_key = get_secret("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. Add it to Streamlit Secrets "
                "or your environment variables."
            )
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.4,
            max_tokens=1800,
        )
    return response.choices[0].message.content or "I couldn't generate a response. Please try again."


def submit_user_message(message):
    """Add a user message, request a reply, and preserve chat history."""
    clean_message = message.strip()
    if not clean_message:
        return
    if BLOCKED:
        return
    st.session_state.messages.append({"role": "user", "content": clean_message})
    try:
        with st.spinner("Preparing an MLT-focused response..."):
            answer = get_ai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        if LIMITS_ACTIVE and not IS_PAID and USER:
            add_usage(USER)
    except Exception as error:
        # Avoid showing tracebacks or API credentials in the public interface.
        st.error(f"Unable to generate a response. Please check your {st.session_state.get('provider', 'AI')} API configuration and try again. Details: {error}")


# =========================================================
# ANSWER FEEDBACK (thumbs up / thumbs down)
# =========================================================
FEEDBACK_FILE = "feedback_log.csv"
FEEDBACK_HEADER = ["time_utc", "rating", "comment", "provider", "question", "answer"]


def save_feedback(index, rating, comment=""):
    """Append one feedback row (rating: 'up' or 'down') to a CSV file."""
    messages = st.session_state.messages
    if index >= len(messages):
        return
    question = ""
    for j in range(index - 1, -1, -1):
        if messages[j]["role"] == "user":
            question = messages[j]["content"]
            break
    row = [
        datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        rating,
        comment.strip(),
        st.session_state.get("provider", ""),
        question[:1000],
        messages[index]["content"][:2000],
    ]
    new_file = not os.path.exists(FEEDBACK_FILE)
    try:
        with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if new_file:
                writer.writerow(FEEDBACK_HEADER)
            writer.writerow(row)
    except OSError:
        pass


def on_thumb(index):
    """Runs when a thumb is clicked under an answer."""
    value = st.session_state.get(f"fb_{index}")
    if value is None:
        return
    save_feedback(index, "up" if value == 1 else "down")


def render_feedback(index):
    """Show thumbs under an answer, plus an optional reason after thumbs down."""
    selection = st.feedback(
        "thumbs",
        key=f"fb_{index}",
        on_change=on_thumb,
        args=(index,),
    )
    if selection == 1:
        st.markdown('<div class="provider-note">Thanks for your feedback.</div>', unsafe_allow_html=True)
    elif selection == 0:
        if index in st.session_state.feedback_sent:
            st.markdown('<div class="provider-note">Thanks, your feedback was sent.</div>', unsafe_allow_html=True)
        else:
            comment = st.text_area(
                "What went wrong? (optional)",
                key=f"fbc_{index}",
                height=80,
                placeholder="e.g. incorrect, too long, not what I asked",
            )
            if st.button("Send feedback", key=f"fbs_{index}"):
                save_feedback(index, "down", comment)
                st.session_state.feedback_sent.add(index)
                st.rerun()


# =========================================================
# ACCOUNTS, MEMBERSHIP AND DAILY LIMIT
# =========================================================
# Accounts are stored in a free Supabase table. Sign-up/sign-in is switched on
# only when SUPABASE_URL and SUPABASE_SERVICE_KEY exist in Streamlit Secrets.
# Without them the app stays open for everyone, exactly as before.
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_SERVICE_KEY")
AUTH_ENABLED = bool(SUPABASE_URL and SUPABASE_KEY)
LIMITS_ACTIVE = AUTH_ENABLED

try:
    FREE_LIMIT = int(get_secret("FREE_DAILY_LIMIT") or 5)
except (TypeError, ValueError):
    FREE_LIMIT = 5
PAYMENT_DETAILS = get_secret("PAYMENT_DETAILS") or "Please contact the developer to get unlimited access."

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_FAILED_LOGINS = 5
LOCK_MINUTES = 15


def email_list(name):
    """Read a comma-separated (or TOML list) secret as a set of lowercase emails."""
    raw = get_secret(name) or ""
    if isinstance(raw, (list, tuple)):
        raw = ",".join(str(item) for item in raw)
    return {item.strip().lower() for item in str(raw).replace("\n", ",").split(",") if item.strip()}


def _today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


# ---------- database (Supabase REST) ----------
def db_request(method, params=None, payload=None):
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/users"
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    # New-style keys (sb_secret_...) go ONLY in the apikey header. Old-style
    # JWT keys (service_role, start with "eyJ") are also sent as a Bearer token.
    if str(SUPABASE_KEY).startswith("eyJ"):
        headers["Authorization"] = f"Bearer {SUPABASE_KEY}"
    try:
        return requests.request(method, url, headers=headers, params=params, json=payload, timeout=15)
    except requests.RequestException:
        raise RuntimeError("Could not reach the account database. Please try again in a moment.")


def db_get_user(email):
    response = db_request("GET", params={"email": f"eq.{email}", "select": "*"})
    if response.status_code != 200:
        raise RuntimeError("The account database returned an error. Please try again.")
    rows = response.json()
    return rows[0] if rows else None


def db_create_user(email, name, salt, password_hash):
    response = db_request(
        "POST",
        payload={"email": email, "name": name, "salt": salt, "password_hash": password_hash},
    )
    if response.status_code == 409:
        return False
    if response.status_code not in (200, 201):
        raise RuntimeError("Could not create the account. Please try again.")
    return True


def db_update_user(email, changes):
    response = db_request("PATCH", params={"email": f"eq.{email}"}, payload=changes)
    if response.status_code not in (200, 204):
        raise RuntimeError("Could not save the change. Please try again.")
    rows = response.json() if response.content else []
    return rows[0] if rows else None


# ---------- passwords ----------
def hash_password(password, salt=None):
    salt = salt or pysecrets.token_hex(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"), salt=bytes.fromhex(salt), n=2**14, r=8, p=1, dklen=32
    ).hex()
    return salt, digest


def password_matches(password, salt, expected_hash):
    _, digest = hash_password(password, salt)
    return hmac.compare_digest(digest, expected_hash)


def _parse_time(value):
    try:
        return datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def _start_session(row):
    st.session_state.auth_email = row["email"]
    st.session_state.user_row = row
    st.session_state.user_checked = time.time()


def sign_up(name, email, password, confirm):
    name = name.strip()
    email = email.strip().lower()
    if not name:
        return False, "Please enter your name."
    if not EMAIL_PATTERN.match(email):
        return False, "Please enter a valid email address."
    if len(password) < 8:
        return False, "Your password must be at least 8 characters."
    if password != confirm:
        return False, "The two passwords do not match."
    try:
        salt, digest = hash_password(password)
        if not db_create_user(email, name, salt, digest):
            return False, "An account with this email already exists. Please sign in."
        row = db_get_user(email)
    except RuntimeError as error:
        return False, str(error)
    if not row:
        return False, "Account created, but sign-in failed. Please sign in manually."
    _start_session(row)
    return True, ""


def sign_in(email, password):
    email = email.strip().lower()
    generic = "Wrong email or password."
    if not EMAIL_PATTERN.match(email) or not password:
        return False, generic
    try:
        row = db_get_user(email)
        if not row:
            return False, generic
        locked_until = _parse_time(row.get("locked_until"))
        now = datetime.datetime.now(datetime.timezone.utc)
        if locked_until and locked_until > now:
            minutes = int((locked_until - now).total_seconds() // 60) + 1
            return False, f"Too many failed attempts. Please try again in about {minutes} minute(s)."
        if not password_matches(password, row["salt"], row["password_hash"]):
            failed = int(row.get("failed_count") or 0) + 1
            changes = {"failed_count": failed}
            if failed >= MAX_FAILED_LOGINS:
                changes = {
                    "failed_count": 0,
                    "locked_until": (now + datetime.timedelta(minutes=LOCK_MINUTES)).isoformat(),
                }
            db_update_user(email, changes)
            return False, generic
        updated = db_update_user(email, {"failed_count": 0, "locked_until": None})
    except RuntimeError as error:
        return False, str(error)
    _start_session(updated or row)
    return True, ""


def logout_user():
    for key in ("auth_email", "user_row", "user_checked"):
        st.session_state.pop(key, None)
    st.session_state.messages = []
    st.session_state.pending_prompt = None


def current_user():
    """Return the signed-in member as a dict, or None."""
    if not AUTH_ENABLED:
        return None
    email = st.session_state.get("auth_email")
    if not email:
        return None
    row = st.session_state.get("user_row")
    if row is None or time.time() - st.session_state.get("user_checked", 0) > 60:
        try:
            fresh = db_get_user(email)
        except RuntimeError:
            fresh = row  # database hiccup: keep the last known data
        if fresh is None:
            logout_user()  # account was deleted
            return None
        row = fresh
        st.session_state.user_row = row
        st.session_state.user_checked = time.time()
    return {
        "email": row["email"],
        "name": row.get("name") or "",
        "paid_until": row.get("paid_until"),
        "used_date": row.get("used_date"),
        "used_count": row.get("used_count") or 0,
    }


def get_usage(user):
    """Questions asked today by this member."""
    if user.get("used_date") == _today():
        return int(user.get("used_count") or 0)
    return 0


def add_usage(user):
    try:
        row = db_update_user(user["email"], {"used_date": _today(), "used_count": get_usage(user) + 1})
        if row:
            st.session_state.user_row = row
            st.session_state.user_checked = time.time()
    except RuntimeError:
        pass


def admin_activate(email, days):
    """Give a member paid access for a number of days (adds to any remaining time)."""
    email = email.strip().lower()
    try:
        row = db_get_user(email)
        if not row:
            return False, "No account found with that email."
        start = datetime.date.today()
        if row.get("paid_until"):
            try:
                start = max(start, datetime.date.fromisoformat(str(row["paid_until"])))
            except ValueError:
                pass
        until = start + datetime.timedelta(days=int(days))
        db_update_user(email, {"paid_until": until.isoformat()})
    except RuntimeError as error:
        return False, str(error)
    return True, f"Paid access for {email} is active until {until.isoformat()}."


def admin_reset_password(email, new_password):
    email = email.strip().lower()
    if len(new_password) < 8:
        return False, "The new password must be at least 8 characters."
    try:
        if not db_get_user(email):
            return False, "No account found with that email."
        salt, digest = hash_password(new_password)
        db_update_user(email, {"salt": salt, "password_hash": digest, "failed_count": 0, "locked_until": None})
    except RuntimeError as error:
        return False, str(error)
    return True, f"Password for {email} was reset."


USER = current_user()
IS_ADMIN = bool(USER and USER["email"] in email_list("ADMIN_EMAILS"))
IS_PAID = (not LIMITS_ACTIVE) or IS_ADMIN or bool(
    USER
    and (
        USER["email"] in email_list("PAID_EMAILS")
        or (USER.get("paid_until") and str(USER["paid_until"]) >= _today())
    )
)
BLOCKED = bool(LIMITS_ACTIVE and not IS_PAID and USER and get_usage(USER) >= FREE_LIMIT)


def render_hero():
    """Top banner shown on every page."""
    st.markdown(
        """
        <div class="hero">
            <div class="hero-eyebrow">Medical Laboratory Technology • AI Learning</div>
            <div class="hero-title">MLT Medical AI Assistant</div>
            <p>
                Explore laboratory science, understand diagnostic tests, prepare for
                examinations, and strengthen your MLT knowledge with an AI-powered
                learning companion.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_paywall():
    st.warning(
        f"You have used your {FREE_LIMIT} free questions for today. "
        "They reset every day at 5:00 AM Pakistan time.\n\n"
        f"**Want unlimited access?** {PAYMENT_DETAILS}\n\n"
        f"Your account email: **{USER['email']}**"
    )


# Sign-in / sign-up screen: nothing else is shown until the visitor is signed in.
if AUTH_ENABLED and USER is None:
    render_hero()
    st.markdown('<div class="section-heading">Welcome</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-subtitle">Sign in or create a free account to start learning. '
        f'Free accounts get {FREE_LIMIT} questions per day.</div>',
        unsafe_allow_html=True,
    )
    tab_in, tab_up = st.tabs(["Sign in", "Create account"])
    with tab_in:
        with st.form("signin_form"):
            si_email = st.text_input("Email", key="si_email")
            si_password = st.text_input("Password", type="password", key="si_password")
            si_submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)
        if si_submit:
            ok, message = sign_in(si_email, si_password)
            if ok:
                st.rerun()
            else:
                st.error(message)
    with tab_up:
        with st.form("signup_form"):
            su_name = st.text_input("Your name", key="su_name")
            su_email = st.text_input("Email", key="su_email")
            su_password = st.text_input("Password (at least 8 characters)", type="password", key="su_password")
            su_confirm = st.text_input("Confirm password", type="password", key="su_confirm")
            su_submit = st.form_submit_button("Create free account", type="primary", use_container_width=True)
        if su_submit:
            ok, message = sign_up(su_name, su_email, su_password, su_confirm)
            if ok:
                st.rerun()
            else:
                st.error(message)
    st.markdown(
        """
        <div class="disclaimer">
            <strong>Educational use only:</strong> this assistant supports MLT learning.
            It does not diagnose, prescribe, or replace a qualified healthcare professional.
            Only your name, email and a securely hashed password are stored.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand-mark">
            <div class="brand-icon">🔬</div>
            <div>
                <div class="brand-name">MLT Medical AI</div>
                <div class="brand-sub">Laboratory learning assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio(
        "Choose a workspace",
        ["AI Assistant", "Lab Result Explainer", "About the Project"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### Developer")
    st.markdown("**Zeeshan Ali**")
    st.caption("Medical Laboratory Technology Student")
    st.caption("AI & Healthcare Technology Enthusiast")
    st.markdown("---")
    if USER:
        st.markdown(f"**{USER['name'] or USER['email']}**")
        st.caption(USER["email"])
        if IS_ADMIN:
            st.caption("Admin · unlimited access")
        elif IS_PAID:
            st.caption("Paid member · unlimited access")
        else:
            left = max(FREE_LIMIT - get_usage(USER), 0)
            st.caption(f"Free plan · {left} of {FREE_LIMIT} questions left today")
        st.button("Log out", on_click=logout_user, use_container_width=True)
        st.markdown("---")
    if USER and IS_ADMIN:
        st.markdown("### Admin")
        admin_email = st.text_input("Member email", key="admin_email")
        admin_days = st.number_input("Paid days", min_value=1, max_value=365, value=30, step=1, key="admin_days")
        if st.button("Activate paid access", use_container_width=True, key="admin_activate_btn"):
            ok, message = admin_activate(admin_email, admin_days)
            (st.success if ok else st.error)(message)
        admin_new_password = st.text_input("New password for this member", type="password", key="admin_new_password")
        if st.button("Reset password", use_container_width=True, key="admin_reset_btn"):
            ok, message = admin_reset_password(admin_email, admin_new_password)
            (st.success if ok else st.error)(message)
        st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()
    st.link_button("✉️ Share feedback", FEEDBACK_URL, use_container_width=True)
    admin_unlocked = IS_ADMIN
    if not admin_unlocked and st.query_params.get("admin") == "1" and get_secret("ADMIN_PASSWORD"):
        st.markdown("---")
        admin_entered = st.text_input("Admin password", type="password", key="admin_pw")
        admin_unlocked = bool(admin_entered) and admin_entered == get_secret("ADMIN_PASSWORD")
    if admin_unlocked:
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "rb") as feedback_handle:
                st.download_button(
                    "⬇️ Download feedback (CSV)",
                    data=feedback_handle.read(),
                    file_name="feedback_log.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        else:
            st.caption("No feedback yet.")
    st.caption("Educational support only • Not a diagnostic service")

# =========================================================
# MAIN HEADER
# =========================================================
render_hero()

if BLOCKED:
    show_paywall()

# =========================================================
# PAGE: AI ASSISTANT
# =========================================================
if page == "AI Assistant":
    st.markdown('<div class="section-heading">Your learning workspace</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Ask a question or choose a topic to get started.</div>',
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(3)
    cards = [
        ("CORE FOCUS", "MLT Education", "Laboratory science and diagnostics"),
        ("STUDY SUPPORT", "Notes & MCQs", "Concepts, revision and exam practice"),
    ]
    for col, (label, value, note) in zip(metric_cols[:2], cards):
        with col:
            st.markdown(
                f'<div class="info-card"><div class="card-label">{label}</div>'
                f'<div class="card-value">{value}</div>'
                f'<div class="card-note">{note}</div></div>',
                unsafe_allow_html=True,
            )
    with metric_cols[2]:
        st.markdown('<div class="provider-label">AI PROVIDER</div>', unsafe_allow_html=True)
        provider_names = list(PROVIDERS.keys()) if IS_PAID else ["Groq"]
        if st.session_state.provider not in provider_names:
            st.session_state.provider = provider_names[0]
        selected_provider = st.selectbox(
            "AI provider",
            provider_names,
            index=provider_names.index(st.session_state.provider),
            label_visibility="collapsed",
        )
        st.session_state.provider = selected_provider
        st.markdown(
            f'<div class="provider-note">Model: {PROVIDERS[selected_provider]["model"]}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("#### Explore a topic")
    quick_cols = st.columns(2)
    quick_prompts = [
        ("🩸 Hematology", "Explain the complete blood count (CBC), its parameters, and clinical significance in simple MLT student language."),
        ("🧫 Microbiology", "Explain Gram staining: principle, reagents, procedure, results, and common errors."),
        ("🧪 Clinical Biochemistry", "Explain liver function tests (LFTs), their components, and clinical significance in a clear table."),
        ("🧬 Molecular Diagnostics", "Explain PCR: principle, steps, components, applications, and common sources of error."),
    ]
    for index, (label, prompt) in enumerate(quick_prompts):
        with quick_cols[index % 2]:
            if st.button(label, key=f"quick_{index}", use_container_width=True, disabled=BLOCKED):
                st.session_state.pending_prompt = prompt
                st.rerun()

    st.markdown("---")
    st.markdown("#### Conversation")
    if not st.session_state.messages:
        st.info(
            "Welcome! Ask me about an MLT subject, laboratory test, practical "
            "technique, viva question, or exam topic."
        )
    for index, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                render_feedback(index)

    if st.session_state.pending_prompt:
        prompt_to_send = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
        submit_user_message(prompt_to_send)
        st.rerun()

    user_input = st.chat_input(
        "Write a Message...",
        disabled=BLOCKED,
    )
    if user_input:
        submit_user_message(user_input)
        st.rerun()

# =========================================================
# PAGE: LAB RESULT EXPLAINER
# =========================================================
elif page == "Lab Result Explainer":
    st.markdown('<div class="section-heading">Laboratory result explainer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Enter values from a report to receive an educational explanation. '
        'Use the reference interval printed by the reporting laboratory.</div>',
        unsafe_allow_html=True,
    )
    st.warning(
        "Do not enter patient names, phone numbers, addresses, CNIC numbers, "
        "hospital IDs, or other identifying information. This tool does not "
        "provide a medical diagnosis."
    )
    with st.form("lab_result_form"):
        col1, col2 = st.columns(2)
        with col1:
            test_name = st.text_input("Test name", placeholder="e.g. Hemoglobin")
            result_value = st.text_input("Your result", placeholder="e.g. 10.8")
            unit = st.text_input("Unit", placeholder="e.g. g/dL")
        with col2:
            lab_range = st.text_input(
                "Reference interval on your report",
                placeholder="e.g. 12.0–16.0",
            )
            age_group = st.selectbox(
                "Age group",
                ["Not specified", "Child", "Adult", "Older adult"],
            )
            context = st.text_area(
                "Additional non-identifying context (optional)",
                placeholder="e.g. Fasting sample; any relevant test context",
                height=90,
            )
        submitted = st.form_submit_button(
            "Explain this laboratory result",
            type="primary",
            use_container_width=True,
            disabled=BLOCKED,
        )

    if submitted:
        if not test_name.strip() or not result_value.strip():
            st.warning("Please enter at least the test name and result.")
        else:
            lab_question = f"""
Please explain this laboratory result for educational purposes.

Test: {test_name}
Result: {result_value}
Unit: {unit or "Not provided"}
Reference interval printed on report: {lab_range or "Not provided"}
Age group: {age_group}
Additional context: {context or "None provided"}

Please explain what the test measures, how this result compares with the
provided interval if one is available, possible factors that can affect it,
and what questions a patient may discuss with a qualified clinician.
Do not diagnose or prescribe. If the reference interval is missing, explain
why interpretation is limited.
"""
            submit_user_message(lab_question)
            st.rerun()

    st.markdown(
        """
        <div class="disclaimer">
            <strong>Important:</strong> Laboratory reference intervals differ between
            laboratories and patient groups. A result outside a reference interval
            does not automatically mean disease, and a result inside it does not
            rule out disease. A qualified clinician must interpret results in context.
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# PAGE: ABOUT
# =========================================================
else:
    st.markdown('<div class="section-heading">About this project</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">The purpose, creator, and scope of the MLT Medical AI Assistant.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="info-card">
            <div class="card-label">PROJECT</div>
            <div class="card-value">MLT Medical AI Assistant</div>
            <div class="card-note">An AI-powered educational companion for Medical Laboratory Technology.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Created by Zeeshan Ali")
    st.write(
        "Zeeshan Ali is a Medical Laboratory Technology student and AI enthusiast. "
        "He developed this project to bring together MLT learning and artificial "
        "intelligence in a simple, accessible study assistant."
    )
    st.markdown("### What it is designed to support")
    st.markdown(
        """
        - Understanding laboratory tests and their principles
        - Learning core MLT subjects
        - Preparing revision notes, MCQs, and viva questions
        - Explaining laboratory terminology and techniques
        - Understanding laboratory results for educational purposes
        """
    )
    st.markdown("### Important limitation")
    st.write(
        "This project is an educational tool. It is not a medical device, "
        "clinical laboratory information system, or substitute for a qualified "
        "healthcare professional. It does not independently verify laboratory "
        "results or provide a diagnosis."
    )
    st.markdown(
        """
        <div class="disclaimer">
            <strong>Medical safety notice:</strong> Do not use this assistant for
            emergency decisions, diagnosis, or treatment decisions. Seek qualified
            medical care for personal health concerns.
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        MLT Medical AI Assistant · Created by Zeeshan Ali · Built for learning
        <br>
        Educational information only — not a substitute for professional medical care.
    </div>
    """,
    unsafe_allow_html=True,
)
