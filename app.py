import streamlit as st

st.set_page_config(
    page_title="SmartHire AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main { background-color: #0f1117; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1a1d27;
    border-right: 1px solid #2d2f3e;
}

/* Cards */
.sh-card {
    background: #1a1d27;
    border: 1px solid #2d2f3e;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}

.sh-card-highlight {
    background: linear-gradient(135deg, #1a1d27 0%, #1e2235 100%);
    border: 1px solid #4f46e5;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}

/* Score circle */
.score-container {
    text-align: center;
    padding: 20px;
}

.score-number {
    font-size: 64px;
    font-weight: 700;
    line-height: 1;
}

.score-label {
    font-size: 14px;
    color: #6b7280;
    margin-top: 8px;
}

/* Badges */
.badge-green {
    background: #052e16;
    color: #4ade80;
    border: 1px solid #166534;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    display: inline-block;
    margin: 2px;
}

.badge-red {
    background: #2d0a0a;
    color: #f87171;
    border: 1px solid #7f1d1d;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    display: inline-block;
    margin: 2px;
}

.badge-yellow {
    background: #1c1100;
    color: #fbbf24;
    border: 1px solid #78350f;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    display: inline-block;
    margin: 2px;
}

.badge-blue {
    background: #0c1a3d;
    color: #60a5fa;
    border: 1px solid #1e3a8a;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    display: inline-block;
    margin: 2px;
}

/* Metric cards */
.metric-card {
    background: #1a1d27;
    border: 1px solid #2d2f3e;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
}

.metric-label {
    font-size: 12px;
    color: #6b7280;
    margin-top: 4px;
}

/* Progress bar custom */
.progress-wrap {
    background: #2d2f3e;
    border-radius: 99px;
    height: 8px;
    margin: 8px 0;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.5s ease;
}

/* Section header */
.section-header {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
    margin-bottom: 12px;
    margin-top: 24px;
}

/* Keyword chip */
.keyword-chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
}

/* Hero */
.hero-title {
    font-size: 42px;
    font-weight: 700;
    line-height: 1.15;
    color: #ffffff;
}

.hero-sub {
    font-size: 16px;
    color: #9ca3af;
    margin-top: 12px;
    line-height: 1.6;
}

.hero-accent {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Divider */
.sh-divider {
    border: none;
    border-top: 1px solid #2d2f3e;
    margin: 20px 0;
}

/* Tag */
.tag {
    background: #1e2235;
    color: #a5b4fc;
    border: 1px solid #3730a3;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
    display: inline-block;
    margin: 2px;
}

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 500;
    font-size: 14px;
    transition: opacity 0.2s;
}

.stButton > button:hover {
    opacity: 0.9;
    color: white;
    border: none;
}

.stTextArea textarea {
    background: #1a1d27 !important;
    border: 1px solid #2d2f3e !important;
    border-radius: 8px !important;
    color: #e5e7eb !important;
    font-family: 'Inter', sans-serif !important;
}

.stFileUploader {
    background: #1a1d27 !important;
    border: 1px solid #2d2f3e !important;
    border-radius: 8px !important;
}

div[data-testid="stMetric"] {
    background: #1a1d27;
    border: 1px solid #2d2f3e;
    border-radius: 10px;
    padding: 16px;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1d27;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #2d2f3e;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    color: #9ca3af;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: #4f46e5 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-size: 20px; font-weight: 700; color: #fff;'>⚡ SmartHire AI</div>
        <div style='font-size: 12px; color: #6b7280; margin-top: 4px;'>Your AI placement assistant</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "📄 ATS Analyzer", "✏️ Resume Rewriter",
         "🔍 Job Matcher", "🎯 Interview Prep", "📊 Application Tracker"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #2d2f3e; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 11px; color: #4b5563; padding: 0 4px;'>
        Built with Python + Claude AI + AWS<br>
        <span style='color: #4f46e5;'>github.com/samarth/smarthire</span>
    </div>
    """, unsafe_allow_html=True)

# Route pages
if page == "🏠 Dashboard":
    from pages import dashboard
    dashboard.show()
elif page == "📄 ATS Analyzer":
    from pages import ats_analyzer
    ats_analyzer.show()
elif page == "✏️ Resume Rewriter":
    from pages import resume_rewriter
    resume_rewriter.show()
elif page == "🔍 Job Matcher":
    from pages import job_matcher
    job_matcher.show()
elif page == "🎯 Interview Prep":
    from pages import interview_prep
    interview_prep.show()
elif page == "📊 Application Tracker":
    from pages import tracker
    tracker.show()
