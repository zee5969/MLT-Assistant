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

    /* Hide Streamlit's built-in menu/footer. The Community Cloud Fork control
       is platform-rendered and is not reliably controlled by app CSS. */
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
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

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

RESPONSE STYLE
- Explain concepts in clear, student-friendly language.
- Use headings, concise bullet points, tables, and stepwise explanations when useful.
- For laboratory tests, explain purpose, specimen, principle, procedure overview,
  clinical significance, and limitations when relevant.
- For MCQs, provide four options, identify the correct answer, and explain why.
- Distinguish established facts from uncertain or context-dependent information.
- Do not invent references, guideline quotations, citations, or laboratory ranges.
- Encourage checking the relevant textbook, laboratory SOP, and current official
  guidance for academic or clinical work.

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
- Remind users not to share names, phone numbers, addresses, identity numbers,
  or other identifying information from medical reports.
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
# GROQ CLIENT & RESPONSE
# =========================================================
def get_groq_client():
    """Create the Groq client without exposing the API key."""
    api_key = None
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass
    api_key = api_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def get_ai_response(conversation):
    """Send the conversation to Groq and return the assistant response."""
    client = get_groq_client()
    if client is None:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to Streamlit Secrets "
            "or your environment variables."
        )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *conversation],
        temperature=0.4,
        max_tokens=1800,
    )
    return response.choices[0].message.content or "I couldn't generate a response. Please try again."


def submit_user_message(message):
    """Add a user message, request a reply, and preserve chat history."""
    clean_message = message.strip()
    if not clean_message:
        return
    st.session_state.messages.append({"role": "user", "content": clean_message})
    try:
        with st.spinner("Preparing an MLT-focused response..."):
            answer = get_ai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as error:
        # Avoid showing tracebacks or API credentials in the public interface.
        st.error(f"Unable to generate a response. Please check your Groq API configuration and try again. Details: {error}")


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
    cards = [
        ("CORE FOCUS", "MLT Education", "Laboratory science and diagnostics"),
        ("STUDY SUPPORT", "Notes & MCQs", "Concepts, revision and exam practice"),
        ("AI ENGINE", MODEL_NAME, "Powered by Groq"),
    ]
    for col, (label, value, note) in zip(metric_cols, cards):
        with col:
            st.markdown(
                f'<div class="info-card"><div class="card-label">{label}</div>'
                f'<div class="card-value">{value}</div>'
                f'<div class="card-note">{note}</div></div>',
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
