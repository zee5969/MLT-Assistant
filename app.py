import os
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
# BRANDING & THEME
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --navy: #10243A;
        --blue: #176B87;
        --teal: #20A39E;
        --ink: #172B3A;
        --muted: #627586;
        --line: #E4EBF0;
        --surface: #F5F8FA;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #F6F9FB;
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(246, 249, 251, 0.92);
    }

    [data-testid="stSidebar"] {
        background: #10243A;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #EAF2F7;
    }

    [data-testid="stSidebar"] .stCaption {
        color: #B8C9D6 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.16);
    }

    .brand-mark {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 18px 0;
    }

    .brand-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #20A39E, #176B87);
        color: white;
        font-size: 23px;
        box-shadow: 0 8px 20px rgba(32,163,158,0.22);
    }

    .brand-name {
        font-family: 'Manrope', sans-serif;
        color: white;
        font-size: 17px;
        line-height: 1.2;
        font-weight: 800;
    }

    .brand-sub {
        color: #B8C9D6;
        font-size: 11px;
        margin-top: 4px;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .hero {
        background: linear-gradient(120deg, #10243A 0%, #174D68 58%, #168A8A 100%);
        border-radius: 22px;
        padding: 30px 34px;
        color: white;
        margin: 4px 0 24px 0;
        box-shadow: 0 14px 34px rgba(16,36,58,0.13);
    }

    .hero-eyebrow {
        color: #BFE9E5;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .hero h1 {
        color: white;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(26px, 3vw, 38px);
        font-weight: 800;
        line-height: 1.15;
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #E2EEF3;
        font-size: 15px;
        margin: 0;
        max-width: 760px;
        line-height: 1.6;
    }

    .section-heading {
        color: #10243A;
        font-family: 'Manrope', sans-serif;
        font-size: 21px;
        font-weight: 800;
        margin: 8px 0 4px 0;
    }

    .section-subtitle {
        color: #627586;
        font-size: 13px;
        margin-bottom: 16px;
    }

    .info-card {
        background: white;
        border: 1px solid #E4EBF0;
        border-radius: 16px;
        padding: 17px 18px;
        min-height: 108px;
        box-shadow: 0 4px 14px rgba(16,36,58,0.035);
    }

    .info-card .card-label {
        color: #627586;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .info-card .card-value {
        color: #10243A;
        font-family: 'Manrope', sans-serif;
        font-size: 17px;
        font-weight: 800;
    }

    .info-card .card-note {
        color: #718392;
        font-size: 11px;
        margin-top: 5px;
    }

    .stButton > button {
        border-radius: 11px;
        border: 1px solid #D8E4EA;
        font-weight: 600;
        min-height: 42px;
        transition: all .15s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #176B87, #20A39E);
        border: 0;
        color: white;
    }

    .stButton > button:hover {
        border-color: #20A39E;
        color: #176B87;
    }

    .stChatMessage {
        background: white;
        border: 1px solid #E7EDF1;
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    [data-testid="stChatInput"] {
        border-color: #D8E4EA;
    }

    [data-testid="stExpander"] {
        background: white;
        border: 1px solid #E4EBF0;
        border-radius: 14px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E4EBF0;
        padding: 14px;
        border-radius: 14px;
    }

    .disclaimer {
        background: #FFF8E9;
        border: 1px solid #F3DFB3;
        color: #75551C;
        border-radius: 12px;
        padding: 13px 16px;
        font-size: 12px;
        line-height: 1.55;
        margin-top: 18px;
    }

    .footer {
        color: #82919D;
        text-align: center;
        font-size: 11px;
        padding: 22px 0 8px 0;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# APPLICATION CONFIGURATION
# =========================================================
CREATOR_NAME = "Zeeshan Ali"
CREATOR_DESCRIPTION = (
    "Medical Laboratory Technology student and AI enthusiast. "
    "Creator of the MLT Medical AI Assistant."
)
FEEDBACK_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSdFPi-G7vvQmojacHAh1GXs1kjWcAtgp3M1x-XGHuYW_DEkQA/viewform?usp=header"
)

# Keep the model configurable in Streamlit Secrets or environment variables.
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

SYSTEM_PROMPT = """
You are the MLT Medical AI Assistant, an educational assistant focused primarily
on Medical Laboratory Technology (MLT), laboratory medicine, and biomedical
science.

CREATOR
If a user asks who created, developed, built, or made you, answer clearly:
"I was developed by Zeeshan Ali, a Medical Laboratory Technology student and
AI enthusiast. This project combines MLT education with artificial intelligence
to support students and learners in understanding laboratory science."
Do not claim that the creator is a doctor, physician, hospital, or medical
institution.

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

RESPONSE STYLE
- Explain concepts in clear, student-friendly language.
- Use headings, concise bullet points, tables, and stepwise explanations when useful.
- For laboratory tests, explain purpose, specimen, principle, procedure overview,
  clinical significance, and important limitations when relevant.
- For MCQs, provide four options, identify the correct answer, and explain why.
- Distinguish established facts from uncertain or context-dependent information.
- Do not invent references, guideline quotations, citations, or laboratory ranges.
- Encourage checking the relevant textbook, laboratory SOP, and current official
  guidance for academic or clinical work.

LABORATORY RESULTS AND REFERENCE INTERVALS
- Reference intervals vary by laboratory, method, instrument, age, sex, pregnancy
  status, population, and clinical context.
- Prefer the reference interval printed on the user's own laboratory report.
- Never label a result as a diagnosis based on one value alone.
- Explain possible interpretations cautiously and identify when clinician review
  is important.
- Do not describe every reference value as a universal WHO standard.

MEDICAL SAFETY
- You are an educational AI tool, not a doctor or a diagnostic service.
- Do not diagnose a user or claim certainty about a disease.
- Do not prescribe medicines, recommend changing doses, or advise stopping
  prescribed treatment.
- Do not interpret symptoms as a confirmed diagnosis.
- For emergency warning signs (for example severe chest pain, severe breathing
  difficulty, stroke signs, unconsciousness, or severe bleeding), advise seeking
  emergency medical care immediately.
- Protect privacy: remind users not to share names, phone numbers, addresses,
  identity numbers, or other identifying information from medical reports.
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

# =========================================================
# GROQ CLIENT
# =========================================================
def get_groq_client():
    """Create the Groq client without exposing the API key."""
    api_key = None

    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


def get_ai_response(conversation):
    """Send conversation to Groq and return the assistant response."""
    client = get_groq_client()
    if client is None:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to Streamlit Secrets "
            "or your environment variables."
        )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation,
        ],
        temperature=0.4,
        max_tokens=1800,
    )
    return response.choices[0].message.content


def submit_user_message(message):
    """Add a user message, request a reply, and preserve chat history."""
    clean_message = message.strip()
    if not clean_message:
        return

    st.session_state.messages.append(
        {"role": "user", "content": clean_message}
    )

    try:
        with st.spinner("Preparing an MLT-focused response..."):
            answer = get_ai_response(st.session_state.messages)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
    except Exception as error:
        # Keep the user question in history, but do not expose secrets or tracebacks.
        st.error(f"Unable to generate a response: {error}")


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
    st.markdown("### Learning areas")
    st.markdown(
        """
        - Hematology
        - Clinical Biochemistry
        - Microbiology
        - Histopathology
        - Immunology & Serology
        - Molecular Diagnostics
        - Parasitology
        - Quality Assurance
        """
    )

    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.link_button("✉️ Share feedback", FEEDBACK_URL, use_container_width=True)
    st.caption("Educational support only • Not a diagnostic service")

# =========================================================
# MAIN HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Medical Laboratory Technology • AI Learning</div>
        <h1>MLT Medical AI Assistant</h1>
        <p>
            Explore laboratory science, understand diagnostic tests, prepare for
            examinations, and strengthen your MLT knowledge with an AI-powered
            learning companion.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
    with metric_cols[0]:
        st.markdown(
            '<div class="info-card"><div class="card-label">CORE FOCUS</div>'
            '<div class="card-value">MLT Education</div>'
            '<div class="card-note">Laboratory science and diagnostics</div></div>',
            unsafe_allow_html=True,
        )
    with metric_cols[1]:
        st.markdown(
            '<div class="info-card"><div class="card-label">STUDY SUPPORT</div>'
            '<div class="card-value">Notes & MCQs</div>'
            '<div class="card-note">Concepts, revision and exam practice</div></div>',
            unsafe_allow_html=True,
        )
    with metric_cols[2]:
        st.markdown(
            '<div class="info-card"><div class="card-label">AI ENGINE</div>'
            f'<div class="card-value">{MODEL_NAME}</div>'
            '<div class="card-note">Powered by Groq</div></div>',
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
            if st.button(label, key=f"quick_{index}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()

    st.markdown("---")
    st.markdown("#### Conversation")

    if not st.session_state.messages:
        st.info(
            "Welcome! Ask me about an MLT subject, laboratory test, practical "
            "technique, viva question, or exam topic."
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.pending_prompt:
        prompt_to_send = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
        submit_user_message(prompt_to_send)
        st.rerun()

    user_input = st.chat_input(
        "Ask about an MLT topic, laboratory test, or practical..."
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

    st.markdown("### Technology")
    st.markdown(
        """
        - **Python** — application logic
        - **Streamlit** — user interface
        - **Groq API** — AI response generation
        - **GitHub** — source-code hosting and version control
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
