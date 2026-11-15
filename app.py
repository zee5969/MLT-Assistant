import base64
import csv
import datetime
import hashlib
import hmac
import html
import os
import re
import secrets as pysecrets
import time
import urllib.parse

import requests
import streamlit as st
import streamlit.components.v1 as components
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

    .stApp [data-testid="stSidebar"] h1,
    .stApp [data-testid="stSidebar"] h2,
    .stApp [data-testid="stSidebar"] h3,
    .stApp [data-testid="stSidebar"] h4,
    .stApp [data-testid="stSidebar"] h5,
    .stApp [data-testid="stSidebar"] h6 {
        color: #FFFFFF !important;
    }

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

    .stApp .hero h1 {
        color: #FFFFFF !important;
    }

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

    [data-testid="stHeader"] button,
    [data-testid="stHeader"] a,
    [data-testid="stHeader"] svg {
        color: #17212B !important;
        fill: #17212B;
    }

    .stApp [data-testid="stMain"] [data-testid="stMarkdownContainer"] a {
        color: #0B6B8A !important;
    }

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

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] li,
    [data-testid="stAlert"] span {
        color: #1F2A37 !important;
    }

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

    [data-testid="stSpinner"] p,
    [data-testid="stSpinner"] span {
        color: #263442 !important;
    }

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

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: #F4F7FA !important;
    }

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

    [data-testid="stFeedback"] button,
    [data-testid="stFeedback"] button * {
        color: #526273 !important;
    }
    [data-testid="stFeedback"] button:hover,
    [data-testid="stFeedback"] button:hover * {
        color: #0D9488 !important;
    }

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

    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div[data-baseweb],
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="base-input"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border-color: #C9D6DF !important;
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
    }

    [data-baseweb="input"],
    [data-baseweb="base-input"],
    [data-baseweb="textarea"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border-color: #C9D6DF !important;
        border-radius: 11px !important;
    }
    [data-testid="stTextInput"] button,
    [data-testid="stNumberInput"] button {
        background: #EEF3F7 !important;
        border: 0 !important;
        color: #526273 !important;
    }
    [data-testid="stTextInput"] button *,
    [data-testid="stNumberInput"] button * {
        color: #526273 !important;
        fill: #526273 !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] a {
        text-decoration: none !important;
    }

    .admin-table-wrap {
        overflow-x: auto;
        background: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(16,36,58,.045);
        margin-bottom: 8px;
    }
    .admin-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }
    .admin-table th {
        text-align: left;
        padding: 11px 14px;
        background: #F0F5F9;
        color: #10243A !important;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: .03em;
        border-bottom: 1px solid #D8E1E8;
        white-space: nowrap;
    }
    .admin-table td {
        padding: 10px 14px;
        color: #263442 !important;
        border-bottom: 1px solid #EDF1F5;
        white-space: nowrap;
    }
    .admin-table tr:last-child td { border-bottom: 0; }
    .badge {
        display: inline-block;
        padding: 2px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-admin { background: #E3EEFA; color: #0B4F8A !important; }
    .badge-paid { background: #DDF5EE; color: #0B6B4F !important; }
    .badge-free { background: #EEF1F4; color: #526273 !important; }

    button[kind^="primary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-primaryFormSubmit"] {
        background: linear-gradient(100deg, #176B87, #0D9488) !important;
        border: 0 !important;
        color: #FFFFFF !important;
    }
    button[kind^="primary"] *,
    [data-testid="stBaseButton-primary"] *,
    [data-testid="stBaseButton-primaryFormSubmit"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

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
    [data-baseweb="tab-border"] {
        background-color: #D8E1E8 !important;
    }
    button[role="tab"][aria-selected="true"],
    button[role="tab"][aria-selected="true"] * {
        color: #0B6B8A !important;
    }

    /* =====================================================
       PROFESSIONAL POLISH
       ===================================================== */
    html, .stApp { color-scheme: light; }

    [data-baseweb="input"],
    [data-baseweb="textarea"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #EEF4F8 !important;
        background-color: #EEF4F8 !important;
        border: 1px solid #B8C7D3 !important;
        border-radius: 11px !important;
        box-shadow: none !important;
    }
    [data-baseweb="base-input"] {
        background: transparent !important;
        background-color: transparent !important;
        border: 0 !important;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: transparent !important;
        color: #10243A !important;
        -webkit-text-fill-color: #10243A !important;
        caret-color: #0D9488 !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #6B7C8C !important;
        -webkit-text-fill-color: #6B7C8C !important;
        opacity: 1 !important;
    }
    [data-baseweb="input"]:focus-within,
    [data-baseweb="textarea"]:focus-within,
    [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div {
        background: #FFFFFF !important;
        border-color: #0D9488 !important;
        box-shadow: 0 0 0 3px rgba(13,148,136,.18) !important;
    }
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 1000px #EEF4F8 inset !important;
        -webkit-text-fill-color: #10243A !important;
        caret-color: #0D9488 !important;
    }

    [data-testid="stTextInput"] div:not([data-testid="stWidgetLabel"]):not([data-testid="stWidgetLabel"] *),
    [data-testid="stNumberInput"] div:not([data-testid="stWidgetLabel"]):not([data-testid="stWidgetLabel"] *),
    [data-testid="stTextArea"] div:not([data-testid="stWidgetLabel"]):not([data-testid="stWidgetLabel"] *),
    [data-testid="stSelectbox"] div:not([data-testid="stWidgetLabel"]):not([data-testid="stWidgetLabel"] *) {
        background-color: #EEF4F8 !important;
    }
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] input {
        background-color: transparent !important;
        color: #10243A !important;
        -webkit-text-fill-color: #10243A !important;
        opacity: 1 !important;
    }
    [data-testid="stSelectbox"] [data-baseweb="select"] div,
    [data-testid="stSelectbox"] [data-baseweb="select"] span {
        color: #10243A !important;
        -webkit-text-fill-color: #10243A !important;
    }

    [data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid #D8E1E8 !important;
        border-radius: 18px !important;
        padding: 24px 24px 18px 24px !important;
        box-shadow: 0 8px 26px rgba(16,36,58,.07) !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-color: #D8E1E8 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 14px rgba(16,36,58,.045) !important;
    }
    button[role="tab"] {
        padding: 10px 20px !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: #EAF6F4 !important;
        border-color: #CDE7E3 !important;
    }
    .feedback-label {
        color: #526273 !important;
        font-size: 12px;
        margin: 10px 0 2px 2px;
    }

    .account-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0 4px 0;
    }
    .account-card .avatar {
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #18A999, #176B87);
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 17px;
    }
    .account-card .account-name {
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 15px;
        line-height: 1.2;
    }
    .account-card .account-email {
        color: #C6D4E0 !important;
        font-size: 12px;
        max-width: 170px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .plan-row {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        margin: 8px 0 7px 0;
    }
    .plan-row .plan-note {
        color: #C6D4E0 !important;
        font-size: 12px;
    }
    .plan-row .badge-admin { background: #1D4F7C; color: #D6E9FA !important; }
    .plan-row .badge-paid { background: #14594A; color: #CFF5E8 !important; }
    .plan-row .badge-free { background: #2B3E52; color: #D6E0EA !important; }
    .usage-bar {
        height: 6px;
        border-radius: 999px;
        background: rgba(255,255,255,.18);
        overflow: hidden;
        margin-bottom: 12px;
    }
    .usage-bar .usage-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #18A999, #5ED6C4);
    }

    /* Free-limit upgrade card (dark, like a "keep chatting" popup). */
    .upgrade-modal {
        background: #10243A;
        border: 1px solid #2C4A63;
        border-radius: 22px;
        padding: 30px 32px 26px 32px;
        max-width: 660px;
        margin: 8px auto 14px auto;
        box-shadow: 0 22px 54px rgba(0,0,0,.30);
    }
    .upgrade-modal .um-title {
        color: #FFFFFF !important;
        font-family: 'Manrope', sans-serif;
        font-size: 29px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 12px;
    }
    .upgrade-modal .um-sub {
        color: #C6D4E0 !important;
        font-size: 15px;
        line-height: 1.55;
        margin-bottom: 22px;
    }
    .upgrade-modal .um-feature {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 0;
        font-size: 15px;
    }
    .upgrade-modal .um-feature .um-icon { font-size: 18px; width: 24px; text-align: center; }
    .upgrade-modal .um-feature .um-text { color: #F3F7FB !important; }
    .upgrade-modal .um-plans { margin-top: 20px; }
    .upgrade-modal .um-plan {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        background: #163550;
        border: 1px solid #2C4A63;
        border-radius: 14px;
        padding: 16px 18px;
        margin-top: 12px;
    }
    .upgrade-modal .um-plan.selected {
        background: #0E4450;
        border-color: #18A999;
    }
    .upgrade-modal .um-plan-left { display: flex; align-items: center; gap: 14px; }
    .upgrade-modal .um-radio {
        width: 24px;
        height: 24px;
        flex: 0 0 24px;
        border-radius: 50%;
        border: 2px solid #5F7C95;
        box-sizing: border-box;
    }
    .upgrade-modal .um-plan.selected .um-radio {
        border: 7px solid #18A999;
        background: #FFFFFF;
    }
    .upgrade-modal .um-plan-name { color: #FFFFFF !important; font-size: 17px; font-weight: 600; }
    .upgrade-modal .um-plan-note { color: #B4C6D6 !important; font-size: 14px; margin-top: 2px; }
    .upgrade-modal .um-plan-price { color: #FFFFFF !important; font-size: 17px; font-weight: 600; white-space: nowrap; }
    .upgrade-modal .um-save {
        display: inline-block;
        margin-left: 8px;
        padding: 1px 9px;
        border-radius: 999px;
        background: #0F5F58;
        color: #BFF3EA !important;
        font-size: 12px;
        font-weight: 700;
    }
    .upgrade-modal .um-box {
        margin-top: 18px;
        background: #163550;
        border: 1px dashed #3F6280;
        border-radius: 12px;
        padding: 13px 16px;
        color: #E8F0F6 !important;
        font-size: 14px;
        line-height: 1.6;
    }
    .upgrade-modal .um-box strong { color: #FFFFFF !important; }
    .upgrade-modal .um-foot {
        color: #9FB4C6 !important;
        font-size: 12px;
        text-align: center;
        margin-top: 16px;
    }
    .upgrade-modal .um-foot strong { color: #D6E2EC !important; }

    /* Popup window (opens in front of the page, like ChatGPT / Claude). */
    div[role="dialog"] {
        background: #10243A !important;
        border: 1px solid #2C4A63 !important;
        border-radius: 22px !important;
        box-shadow: 0 30px 80px rgba(0,0,0,.55) !important;
        max-width: 620px !important;
        width: 92vw !important;
        margin: 0 auto !important;
    }
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3,
    div[role="dialog"] [data-testid="stHeading"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Manrope', sans-serif !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    div[role="dialog"] button[aria-label="Close"],
    div[role="dialog"] button[aria-label="Close"] * {
        color: #D6E2EC !important;
        fill: #D6E2EC !important;
        background: transparent !important;
    }
    div[data-testid="stModal"], div[data-baseweb="modal"] {
        background: rgba(0,0,0,.62) !important;
    }
    div[role="dialog"] .stButton > button {
        background: #FFFFFF !important;
        border: 0 !important;
        min-height: 46px;
    }
    div[role="dialog"] .stButton > button p { color: #10243A !important; }
    /* Compact popup: narrow, short, navy. */
    [data-testid="stDialog"] div[role="dialog"],
    [data-testid="stDialog"] div[role="dialog"] > div,
    div[data-baseweb="modal"] div[role="dialog"],
    div[data-baseweb="modal"] div[role="dialog"] > div {
        background: #10243A !important;
        background-color: #10243A !important;
    }
    [data-testid="stDialog"] div[role="dialog"],
    div[data-baseweb="modal"] div[role="dialog"] {
        max-width: 480px !important;
        width: 92vw !important;
        padding: 6px 8px 10px 8px !important;
    }
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3,
    div[role="dialog"] [data-testid="stHeading"] * {
        font-size: 21px !important;
        line-height: 1.25 !important;
        padding: 14px 0 4px 0 !important;
        margin: 0 !important;
    }
    div[role="dialog"] .um-sub { font-size: 13px !important; margin-bottom: 10px !important; line-height: 1.45 !important; }
    div[role="dialog"] .um-feature { padding: 3px 0 !important; font-size: 13.5px !important; gap: 10px !important; }
    div[role="dialog"] .um-feature .um-icon { font-size: 15px !important; width: 20px !important; }
    div[role="dialog"] .um-plans { margin-top: 10px !important; }
    div[role="dialog"] .um-plan { padding: 10px 14px !important; margin-top: 8px !important; border-radius: 12px !important; }
    div[role="dialog"] .um-plan-name, div[role="dialog"] .um-plan-price { font-size: 15px !important; }
    div[role="dialog"] .um-plan-note { font-size: 12px !important; }
    div[role="dialog"] .um-radio { width: 20px !important; height: 20px !important; flex: 0 0 20px !important; }
    div[role="dialog"] .um-plan.selected .um-radio { border-width: 6px !important; }
    div[role="dialog"] .um-box { margin-top: 10px !important; padding: 9px 12px !important; font-size: 12.5px !important; line-height: 1.5 !important; }
    div[role="dialog"] .um-foot { margin-top: 8px !important; font-size: 11px !important; }
    div[role="dialog"] .stButton > button, div[role="dialog"] .stLinkButton > a { min-height: 40px !important; }
    div[role="dialog"] [data-testid="stVerticalBlock"] { gap: .5rem !important; }
    .upgrade-modal.in-dialog {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    .limit-bar {
        background: #10243A;
        border: 1px solid #2C4A63;
        border-radius: 14px;
        padding: 14px 18px;
        margin: 0 0 12px 0;
        color: #F3F7FB !important;
        font-size: 14px;
    }
    .limit-bar strong { color: #FFFFFF !important; }

    /* Hide the invisible script frames so they take no space. */
    iframe[height="0"] {
        display: none !important;
    }
    [data-testid="stCustomComponentV1"]:has(iframe[height="0"]),
    [data-testid="stIFrame"]:has(iframe[height="0"]) {
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    [data-testid="stElementContainer"]:has(iframe[height="0"]) {
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
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
    "Groq": {"model": get_secret("GROQ_MODEL") or "llama-3.3-70b-versatile"},
    "OpenAI": {"model": get_secret("OPENAI_MODEL") or "gpt-5-mini"},
}

SYSTEM_PROMPT = """
You are the MLT Medical AI Assistant, an educational assistant focused primarily
on Medical Laboratory Technology (MLT), laboratory medicine, and biomedical science.

CONVERSATION AND IDENTITY
- Reply naturally and directly to every message, including greetings and small
  talk. "hi" gets a short greeting. "how are you" gets a friendly answer such as
  "I'm doing well, thank you! How can I help you with MLT today?".
- If the user asks about you ("who are you", "what are you", "what can you do",
  "tell me about yourself"), explain briefly that you are the MLT Medical AI
  Assistant, an AI study helper for Medical Laboratory Technology, and say what
  you can help with (lab tests, notes, MCQs, viva questions, result explanations).
  Do NOT mention the creator unless the user asks who made you.
- If the user says your answer was wrong or did not answer their question,
  apologise in one short sentence and answer their actual question.
- If a message is not about MLT, answer it briefly and politely; you may add one
  short line that your main focus is MLT and laboratory science. Do not refuse
  harmless casual questions.
- Never reply with a generic line such as "I'm here and ready to help" instead
  of answering. Always answer what was asked.
- Reply in the same language the user writes in (English, Urdu, Roman Urdu, etc.).

CREATOR
Only when the user asks who created, developed, built, or made you, answer:
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
- For casual messages, be warm and natural, not stiff.
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
def _call_openai(model, messages):
    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    from openai import OpenAI  # imported here so Groq still works without it

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_completion_tokens=4000,
    )
    return response.choices[0].message.content


def _call_groq(model, messages):
    api_key = get_secret("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured. Add it to Streamlit Secrets.")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=1800,
    )
    return response.choices[0].message.content


def get_ai_response(conversation):
    """Get a reply. Paid members use OpenAI when a key exists; otherwise Groq.
    If a service or model fails, the next one is tried automatically."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *conversation]
    attempts = []
    if IS_PAID and get_secret("OPENAI_API_KEY"):
        attempts.append(("OpenAI", PROVIDERS["OpenAI"]["model"]))
    groq_models = [PROVIDERS["Groq"]["model"], "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for model in dict.fromkeys(groq_models):  # unique, keeps order
        attempts.append(("Groq", model))

    last_error = None
    for provider, model in attempts:
        try:
            text = _call_openai(model, messages) if provider == "OpenAI" else _call_groq(model, messages)
            if text and text.strip():
                st.session_state.provider = provider
                return text
            last_error = RuntimeError(f"{provider} ({model}) returned an empty answer.")
        except Exception as error:
            last_error = RuntimeError(f"{provider} ({model}): {error}")
    raise last_error or RuntimeError("No AI service is available.")


def submit_user_message(message):
    """Add a user message, request a reply, and preserve chat history."""
    clean_message = message.strip()
    if not clean_message:
        return
    if BLOCKED:
        return
    st.session_state.messages.append({"role": "user", "content": clean_message})
    st.session_state.last_error = None
    try:
        with st.spinner("Preparing an MLT-focused response..."):
            answer = get_ai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        if LIMITS_ACTIVE and not IS_PAID and USER:
            add_usage(USER)
    except Exception as error:
        # Avoid showing tracebacks or API credentials in the public interface.
        # Saved (not shown here) because the page reruns right after this and would hide it.
        st.session_state.last_error = str(error)


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
    st.markdown('<div class="feedback-label">Was this answer helpful?</div>', unsafe_allow_html=True)
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
SUPABASE_URL = str(get_secret("SUPABASE_URL") or "").strip().strip("\"'").strip()
SUPABASE_KEY = str(get_secret("SUPABASE_SERVICE_KEY") or "").strip().strip("\"'").strip()
AUTH_ENABLED = bool(SUPABASE_URL and SUPABASE_KEY)
LIMITS_ACTIVE = AUTH_ENABLED

try:
    FREE_LIMIT = int(get_secret("FREE_DAILY_LIMIT") or 5)
except (TypeError, ValueError):
    FREE_LIMIT = 5
PAYMENT_DETAILS = get_secret("PAYMENT_DETAILS") or "Please contact the developer to get unlimited access."
PRICE_MONTHLY = str(get_secret("PRICE_MONTHLY") or "").strip()
PRICE_YEARLY = str(get_secret("PRICE_YEARLY") or "").strip()
PAYMENT_URL = str(get_secret("PAYMENT_URL") or "").strip()

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_FAILED_LOGINS = 5
LOCK_MINUTES = 15


def _questions(n):
    return f"{n} question" + ("" if n == 1 else "s")


def email_list(name):
    """Read a comma-separated (or TOML list) secret as a set of lowercase emails."""
    raw = get_secret(name) or ""
    if isinstance(raw, (list, tuple)):
        raw = ",".join(str(item) for item in raw)
    return {item.strip().lower() for item in str(raw).replace("\n", ",").split(",") if item.strip()}


def _today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


# ---------- database (Supabase REST) ----------
def supabase_base_url():
    """Clean the project URL so extra paths (like /rest/v1) or a dashboard link still work."""
    raw = SUPABASE_URL
    if "://" not in raw:
        raw = "https://" + raw
    parts = urllib.parse.urlsplit(raw)
    host = parts.netloc
    if host in ("supabase.com", "www.supabase.com", "app.supabase.com"):
        match = re.search(r"/project/([a-z0-9]+)", parts.path)
        if match:
            return f"https://{match.group(1)}.supabase.co"
    return f"{parts.scheme}://{host}"


def db_request(method, params=None, payload=None):
    url = f"{supabase_base_url()}/rest/v1/users"
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


def _db_error(response, fallback):
    """Build a readable error that includes the HTTP code and Supabase's short message."""
    detail = ""
    try:
        body = response.json()
        if isinstance(body, dict):
            detail = str(body.get("message") or body.get("error") or "")[:140]
    except Exception:
        pass
    suffix = f"code {response.status_code}" + (f": {detail}" if detail else "")
    return RuntimeError(f"{fallback} ({suffix})")


def db_get_user(email):
    response = db_request("GET", params={"email": f"eq.{email}", "select": "*"})
    if response.status_code != 200:
        raise _db_error(response, "The account database returned an error. Please try again.")
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
        raise _db_error(response, "Could not create the account. Please try again.")
    return True


def db_update_user(email, changes):
    response = db_request("PATCH", params={"email": f"eq.{email}"}, payload=changes)
    if response.status_code not in (200, 204):
        raise _db_error(response, "Could not save the change. Please try again.")
    rows = response.json() if response.content else []
    return rows[0] if rows else None


def db_list_users():
    """All members (no password data), newest first."""
    response = db_request(
        "GET",
        params={
            "select": "email,name,paid_until,used_date,used_count,created_at",
            "order": "created_at.desc",
            "limit": "1000",
        },
    )
    if response.status_code != 200:
        raise _db_error(response, "Could not load the member list.")
    return response.json()


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


# ---------- "stay signed in" after a page refresh ----------
# The sign-in token is kept in three places so a refresh never logs you out:
#   1. a browser cookie,
#   2. the browser's localStorage (most reliable),
#   3. a one-time ?mlt_t=... link used to hand the token from localStorage
#      to the server after a refresh (it is removed from the address at once).
SESSION_COOKIE = "mlt_session"
STORAGE_KEY = "mlt_session"
URL_PARAM = "mlt_t"
SESSION_DAYS = 30


def _session_key():
    # Derived from the server-side database key, so no extra secret is needed.
    return hashlib.sha256(("mlt-session|" + SUPABASE_KEY).encode("utf-8")).digest()


def _sign(payload, password_hash):
    message = f"{payload}|{password_hash}".encode("utf-8")
    return hmac.new(_session_key(), message, hashlib.sha256).hexdigest()


def make_session_token(row):
    """Signed token: email + expiry + signature (tied to the current password)."""
    expires = int(time.time()) + SESSION_DAYS * 86400
    email_part = base64.urlsafe_b64encode(row["email"].encode("utf-8")).decode("ascii").rstrip("=")
    payload = f"{email_part}.{expires}"
    return f"{payload}.{_sign(payload, row.get('password_hash', ''))}"


def read_session_token(token):
    """Return the member's database row if the token is genuine and not expired."""
    try:
        email_part, expires, signature = str(token).split(".")
        if int(expires) < time.time():
            return None
        email = base64.urlsafe_b64decode(email_part + "=" * (-len(email_part) % 4)).decode("utf-8")
        row = db_get_user(email)
        if not row:
            return None
        expected = _sign(f"{email_part}.{expires}", row.get("password_hash", ""))
        return row if hmac.compare_digest(signature, expected) else None
    except (ValueError, RuntimeError, TypeError, UnicodeDecodeError):
        return None


def run_js(js):
    """Run a small script in the browser through a hidden frame (works on every Streamlit version).

    Inside the frame, window.parent is the Streamlit page, so the script can reach
    the page's cookies, localStorage and address.
    """
    components.html(f"<script>{js}</script>", height=0)


def sync_cookie():
    """Save the sign-in token in the browser after login, and remove it after logout."""
    token = st.session_state.get("session_cookie")
    clear = st.session_state.pop("clear_cookie", False)
    max_age = SESSION_DAYS * 86400
    if token:
        run_js(
            "(function(){try{var P=window.parent;"
            f'var t="{token}";'
            f'try{{P.localStorage.setItem("{STORAGE_KEY}",t);}}catch(e){{}}'
            f'try{{P.document.cookie="{SESSION_COOKIE}="+t+"; path=/; max-age={max_age}; SameSite=Lax"'
            '+(P.location.protocol==="https:"?"; Secure":"");}catch(e){}'
            "}catch(e){}})();"
        )
    elif clear:
        run_js(
            "(function(){try{var P=window.parent;"
            f'try{{P.localStorage.removeItem("{STORAGE_KEY}");}}catch(e){{}}'
            f'try{{P.document.cookie="{SESSION_COOKIE}=; path=/; max-age=0; SameSite=Lax"'
            '+(P.location.protocol==="https:"?"; Secure":"");}catch(e){}'
            "}catch(e){}})();"
        )


def restore_bridge():
    """On the sign-in screen: if the browser remembers a login, reload once with the token."""
    if st.session_state.get("bridge_sent") or st.session_state.get("no_bridge"):
        return
    st.session_state.bridge_sent = True
    run_js(
        "(function(){try{var P=window.parent;"
        f'var t=P.localStorage.getItem("{STORAGE_KEY}");'
        "if(!t){return;}"
        "var u=new URL(P.location.href);"
        f'if(u.searchParams.get("{URL_PARAM}")){{return;}}'
        f'u.searchParams.set("{URL_PARAM}",t);'
        "P.location.replace(u.toString());"
        "}catch(e){}})();"
    )


def restore_login():
    """After a page refresh, sign the member back in (once per visit)."""
    if st.session_state.get("cookie_checked") or st.session_state.get("auth_email"):
        return
    st.session_state.cookie_checked = True

    token = None
    from_url = False
    try:
        token = st.context.cookies.get(SESSION_COOKIE)
    except Exception:
        token = None
    try:
        url_token = st.query_params.get(URL_PARAM)
    except Exception:
        url_token = None
    if url_token:
        from_url = True
        if not token:
            token = url_token
        try:
            del st.query_params[URL_PARAM]  # never leave the token in the address bar
        except Exception:
            pass

    if not token:
        return
    row = read_session_token(token)
    if not row and from_url and url_token != token:
        row = read_session_token(url_token)
    if row:
        _start_session(row)
    else:
        # Old / invalid token: remove it from the browser and do not retry.
        st.session_state.clear_cookie = True
        st.session_state.no_bridge = True


def _start_session(row):
    st.session_state.auth_email = row["email"]
    st.session_state.user_row = row
    st.session_state.user_checked = time.time()
    st.session_state.session_cookie = make_session_token(row)
    st.session_state.cookie_checked = True
    st.session_state.no_bridge = False


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
    for key in ("auth_email", "user_row", "user_checked", "session_cookie"):
        st.session_state.pop(key, None)
    st.session_state.clear_cookie = True
    st.session_state.cookie_checked = True
    st.session_state.no_bridge = True  # do not sign straight back in
    st.session_state.messages = []
    st.session_state.pending_prompt = None


def _row_is_blocked(row):
    """True when this saved row has no paid access and today's free questions are used up."""
    paid = row.get("paid_until") and str(row["paid_until"]) >= _today()
    return (not paid) and row.get("used_date") == _today() and int(row.get("used_count") or 0) >= FREE_LIMIT


def current_user():
    """Return the signed-in member as a dict, or None."""
    if not AUTH_ENABLED:
        return None
    email = st.session_state.get("auth_email")
    if not email:
        return None
    row = st.session_state.get("user_row")
    stale = time.time() - st.session_state.get("user_checked", 0) > 60
    # A locked member is re-checked on every click, so paid access starts immediately.
    if row is None or stale or _row_is_blocked(row):
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


def admin_revoke(email):
    email = email.strip().lower()
    try:
        if not db_get_user(email):
            return False, "No account found with that email."
        db_update_user(email, {"paid_until": None})
    except RuntimeError as error:
        return False, str(error)
    return True, f"Paid access removed for {email}."


def _html_table(headers, rows):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return (
        '<div class="admin-table-wrap"><table class="admin-table">'
        f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def _stat_card(label, value, note):
    return (
        f'<div class="info-card"><div class="card-label">{html.escape(label)}</div>'
        f'<div class="card-value">{html.escape(value)}</div>'
        f'<div class="card-note">{html.escape(note)}</div></div>'
    )


def render_admin_dashboard():
    """Members, paid access and feedback for the site owner."""
    st.markdown('<div class="section-heading">Admin dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Members, paid access and feedback in one place.</div>',
        unsafe_allow_html=True,
    )
    notice = st.session_state.pop("admin_notice", None)
    if notice:
        (st.success if notice[0] else st.error)(notice[1])

    try:
        members = db_list_users()
    except RuntimeError as error:
        st.error(str(error))
        return

    today = _today()
    admin_set = email_list("ADMIN_EMAILS")
    paid_set = email_list("PAID_EMAILS")

    def plan_of(row):
        email = str(row.get("email", "")).lower()
        if email in admin_set:
            return "Admin"
        if email in paid_set or (row.get("paid_until") and str(row["paid_until"]) >= today):
            return "Paid"
        return "Free"

    plans = [plan_of(m) for m in members]
    asked_today = sum(int(m.get("used_count") or 0) for m in members if m.get("used_date") == today)
    stats = [
        ("MEMBERS", str(len(members)), "Registered accounts"),
        ("PAID", str(plans.count("Paid")), "Active paid members"),
        ("FREE", str(plans.count("Free")), "On the free plan"),
        ("QUESTIONS TODAY", str(asked_today), "Asked by free members"),
    ]
    for col, (label, value, note) in zip(st.columns(4), stats):
        with col:
            st.markdown(_stat_card(label, value, note), unsafe_allow_html=True)

    st.markdown("#### Members")
    query = st.text_input(
        "Search members",
        placeholder="Search by name or email",
        key="admin_search",
        label_visibility="collapsed",
    ).strip().lower()
    rows = []
    for member, plan in zip(members, plans):
        haystack = f"{member.get('email', '')} {member.get('name') or ''}".lower()
        if query and query not in haystack:
            continue
        paid_until = str(member.get("paid_until") or "") if plan == "Paid" else ""
        used = int(member.get("used_count") or 0) if member.get("used_date") == today else 0
        rows.append(
            [
                html.escape(member.get("name") or "—"),
                html.escape(member.get("email", "")),
                f'<span class="badge badge-{plan.lower()}">{plan}</span>',
                html.escape(paid_until or "—"),
                str(used),
                html.escape(str(member.get("created_at") or "")[:10] or "—"),
            ]
        )
    if rows:
        st.markdown(
            _html_table(["Name", "Email", "Plan", "Paid until", "Questions today", "Joined"], rows[:200]),
            unsafe_allow_html=True,
        )
        if len(rows) > 200:
            st.caption(f"Showing the first 200 of {len(rows)} matches. Use the search box to narrow down.")
    else:
        st.info("No members found." if members else "No members yet. Accounts will appear here as people sign up.")

    if members:
        st.markdown("#### Manage a member")
        emails = [m["email"] for m in members]
        left, right = st.columns(2)
        with left.container(border=True):
            st.markdown("**Paid access**")
            chosen = st.selectbox("Member", emails, key="admin_member")
            days = st.number_input("Paid days", min_value=1, max_value=365, value=30, step=1, key="admin_days")
            b1, b2 = st.columns(2)
            if b1.button("Activate / extend", key="admin_activate_btn", use_container_width=True):
                st.session_state.admin_notice = admin_activate(chosen, days)
                st.rerun()
            if b2.button("Remove paid access", key="admin_revoke_btn", use_container_width=True):
                st.session_state.admin_notice = admin_revoke(chosen)
                st.rerun()
        with right.container(border=True):
            st.markdown("**Reset password**")
            chosen_reset = st.selectbox("Member for password reset", emails, key="admin_member_reset")
            new_password = st.text_input("New password (at least 8 characters)", type="password", key="admin_new_password")
            if st.button("Reset password", key="admin_reset_btn", use_container_width=True):
                st.session_state.admin_notice = admin_reset_password(chosen_reset, new_password)
                st.rerun()

    st.markdown("#### Feedback")
    feedback_rows = []
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, newline="", encoding="utf-8") as handle:
                feedback_rows = list(csv.DictReader(handle))
        except OSError:
            feedback_rows = []
    ups = sum(1 for r in feedback_rows if r.get("rating") == "up")
    downs = sum(1 for r in feedback_rows if r.get("rating") == "down")
    fb1, fb2, fb3 = st.columns(3)
    with fb1:
        st.markdown(_stat_card("HELPFUL", str(ups), "Thumbs up"), unsafe_allow_html=True)
    with fb2:
        st.markdown(_stat_card("NOT HELPFUL", str(downs), "Thumbs down"), unsafe_allow_html=True)
    with fb3:
        if feedback_rows:
            with open(FEEDBACK_FILE, "rb") as handle:
                st.download_button(
                    "⬇️ Download feedback (CSV)",
                    data=handle.read(),
                    file_name="feedback_log.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        else:
            st.caption("No feedback yet.")
    comments = [r for r in feedback_rows if r.get("rating") == "down" and (r.get("comment") or "").strip()]
    if comments:
        st.markdown("**Latest comments on thumbs-down answers**")
        recent = comments[-5:][::-1]
        st.markdown(
            _html_table(
                ["Time (UTC)", "Comment", "Question"],
                [
                    [
                        html.escape(str(r.get("time_utc", ""))[:16].replace("T", " ")),
                        html.escape(r.get("comment", "")[:200]),
                        html.escape(r.get("question", "")[:90]),
                    ]
                    for r in recent
                ],
            ),
            unsafe_allow_html=True,
        )


if AUTH_ENABLED:
    restore_login()
USER = current_user()
if AUTH_ENABLED:
    sync_cookie()
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


def _paywall_card_html():
    """Body of the upgrade popup: features, plans and payment details."""
    details = html.escape(str(PAYMENT_DETAILS)).replace("\n", "<br>")
    features = [
        ("♾️", "Unlimited questions every day"),
        ("📝", "Notes, MCQs and viva practice without limits"),
        ("⚡", "Faster help from the developer"),
    ]
    if get_secret("OPENAI_API_KEY"):
        features.insert(1, ("🤖", "Access to the OpenAI model"))
    feature_html = "".join(
        f'<div class="um-feature"><span class="um-icon">{icon}</span>'
        f'<span class="um-text">{html.escape(text)}</span></div>'
        for icon, text in features
    )
    monthly_price = html.escape(PRICE_MONTHLY or "Contact developer")
    plans_html = (
        '<div class="um-plan selected"><div class="um-plan-left"><div class="um-radio"></div>'
        '<div><div class="um-plan-name">Monthly</div>'
        '<div class="um-plan-note">Billed monthly</div></div></div>'
        f'<div class="um-plan-price">{monthly_price}</div></div>'
    )
    if PRICE_YEARLY:
        plans_html += (
            '<div class="um-plan"><div class="um-plan-left"><div class="um-radio"></div>'
            '<div><div class="um-plan-name">Yearly<span class="um-save">Best value</span></div>'
            '<div class="um-plan-note">Billed annually</div></div></div>'
            f'<div class="um-plan-price">{html.escape(PRICE_YEARLY)}</div></div>'
        )
    return (
        '<div class="upgrade-modal in-dialog">'
        f'<div class="um-sub">Your free questions ({FREE_LIMIT} per day) are finished. '
        "They return at 5:00 AM Pakistan time, or keep going now with unlimited access.</div>"
        f"{feature_html}"
        f'<div class="um-plans">{plans_html}</div>'
        f'<div class="um-box"><strong>How to get unlimited access</strong><br>{details}</div>'
        f'<div class="um-foot">Your account email: <strong>{html.escape(USER["email"])}</strong></div>'
        "</div>"
    )


def _paywall_dialog_body():
    st.markdown(_paywall_card_html(), unsafe_allow_html=True)
    if PAYMENT_URL:
        st.link_button("Upgrade for unlimited access", PAYMENT_URL, use_container_width=True, type="primary")
    st.button("🔄 I have paid — refresh my access", key="refresh_access", use_container_width=True)


def show_paywall():
    """When the free limit is used up, open an upgrade popup in front of the page."""
    st.markdown(
        '<div class="limit-bar"><strong>Daily free limit reached.</strong> '
        "Your questions return at 5:00 AM Pakistan time, or upgrade for unlimited access.</div>",
        unsafe_allow_html=True,
    )
    st.button("View plans", key="view_plans")
    title = "Keep chatting with MLT Assistant"
    dialog_decorator = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)
    if dialog_decorator is not None:
        try:
            dialog_decorator(title, width="small")(_paywall_dialog_body)()
            return
        except Exception:
            pass
    # Very old Streamlit without popups: show the card on the page instead.
    st.markdown(_paywall_card_html().replace(" in-dialog", ""), unsafe_allow_html=True)
    if PAYMENT_URL:
        st.link_button("Upgrade for unlimited access", PAYMENT_URL, type="primary")
    st.button("🔄 I have paid — refresh my access", key="refresh_access")


# Sign-in / sign-up screen: nothing else is shown until the visitor is signed in.
if AUTH_ENABLED and USER is None:
    restore_bridge()
    render_hero()
    _, center, _ = st.columns([1, 1.7, 1])
    with center:
        st.markdown('<div class="section-heading">Welcome</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-subtitle">Sign in to your account, or create a free one in seconds. '
            f'Free plan: {_questions(FREE_LIMIT)} per day.</div>',
            unsafe_allow_html=True,
        )
        tab_in, tab_up = st.tabs(["Sign in", "Create account"])
        with tab_in:
            with st.form("signin_form"):
                si_email = st.text_input("Email", key="si_email", placeholder="you@example.com")
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
                su_email = st.text_input("Email", key="su_email", placeholder="you@example.com")
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
        ["AI Assistant", "Lab Result Explainer", "About the Project"] + (["Admin Dashboard"] if IS_ADMIN else []),
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### Developer")
    st.markdown("**Zeeshan Ali**")
    st.caption("Medical Laboratory Technology Student")
    st.caption("AI & Healthcare Technology Enthusiast")
    st.markdown("---")
    if USER:
        display_name = USER["name"] or USER["email"].split("@")[0]
        if IS_ADMIN:
            plan_key, plan_label, plan_note, usage_bar = "admin", "Admin", "Unlimited access", ""
        elif IS_PAID:
            plan_key, plan_label, plan_note, usage_bar = "paid", "Paid member", "Unlimited access", ""
        else:
            left = max(FREE_LIMIT - get_usage(USER), 0)
            percent = int(100 * left / max(FREE_LIMIT, 1))
            plan_key, plan_label = "free", "Free plan"
            plan_note = f"Questions left today: {left} of {FREE_LIMIT}"
            usage_bar = f'<div class="usage-bar"><div class="usage-fill" style="width:{percent}%"></div></div>'
        st.markdown(
            '<div class="account-card">'
            f'<div class="avatar">{html.escape(display_name[:1].upper())}</div>'
            '<div class="account-meta">'
            f'<div class="account-name">{html.escape(display_name)}</div>'
            f'<div class="account-email">{html.escape(USER["email"])}</div>'
            "</div></div>"
            f'<div class="plan-row"><span class="badge badge-{plan_key}">{plan_label}</span>'
            f'<span class="plan-note">{plan_note}</span></div>'
            f"{usage_bar}",
            unsafe_allow_html=True,
        )
        st.button("Log out", on_click=logout_user, use_container_width=True)
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

    metric_cols = st.columns(2)
    cards = [
        ("CORE FOCUS", "MLT Education", "Laboratory science and diagnostics"),
        ("STUDY SUPPORT", "Notes & MCQs", "Concepts, revision and exam practice"),
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

    if st.session_state.get("last_error"):
        st.error(
            "Sorry, I could not get an answer just now. Please try again. "
            f"Details: {st.session_state.last_error}"
        )

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

    if st.session_state.get("last_error"):
        st.error(
            "Sorry, I could not get an answer just now. Please try again. "
            f"Details: {st.session_state.last_error}"
        )

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
# PAGE: ADMIN DASHBOARD
# =========================================================
elif page == "Admin Dashboard" and IS_ADMIN:
    render_admin_dashboard()

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
