import streamlit as st
from src.matcher import compute_match_score
from src.extractor import extract_keywords
from src.llm_feedback import get_llm_feedback
from src.visualizer import plot_skill_gap, plot_score_gauge
import time

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume-Job Match Scorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1A56DB, #7E3AF2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .score-box {
        background: linear-gradient(135deg, #EFF6FF, #EDE9FE);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #BFDBFE;
    }
    .score-num {
        font-size: 3.5rem;
        font-weight: 800;
        color: #1A56DB;
    }
    .tag {
        display: inline-block;
        background: #EDE9FE;
        color: #5B21B6;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 2px;
    }
    .missing-tag {
        display: inline-block;
        background: #FEF2F2;
        color: #991B1B;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 2px;
    }
    .matched-tag {
        display: inline-block;
        background: #ECFDF5;
        color: #065F46;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 2px;
    }
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    div[data-testid="stTextArea"] textarea {
        border-radius: 10px;
        border: 1.5px solid #E5E7EB;
        font-size: 0.9rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1A56DB, #7E3AF2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2.5rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=60)
    st.markdown("### ⚙️ Settings")
    use_llm = st.toggle("Enable AI Feedback (LLM)", value=True)
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("""
    1. Paste your resume text
    2. Paste the job description
    3. Click **Analyse Match**
    4. Get your score + AI tips
    """)
    st.markdown("---")
    st.markdown("**Built by:** Fathimathu Nasna SP")
    st.markdown("**Stack:** Python · NLP · Groq LLaMA 3 · Streamlit")
    st.markdown("**Internship:** PypSpiders / TestYantra")

# ── Header ────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🎯 AI Resume–Job Match Scorer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste your resume and a job description — get an instant compatibility score, skill gap analysis, and AI-powered improvement tips.</div>', unsafe_allow_html=True)

# ── Input columns ─────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📄 Your Resume")
    resume_text = st.text_area(
        label="resume",
        placeholder="Paste your full resume text here...\n\nInclude: skills, experience, education, projects, certifications.",
        height=320,
        label_visibility="collapsed"
    )
    uploaded = st.file_uploader("Or upload a .txt resume file", type=["txt"])
    if uploaded:
        resume_text = uploaded.read().decode("utf-8")
        st.success("✅ Resume loaded from file!")

with col2:
    st.markdown("#### 💼 Job Description")
    job_text = st.text_area(
        label="job",
        placeholder="Paste the full job description here...\n\nInclude: required skills, responsibilities, qualifications.",
        height=320,
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
analyse_btn = st.button("🚀 Analyse Match", use_container_width=True)

# ── Sample data button ────────────────────────────────────────────
if st.button("📋 Load Sample Data (Demo)", use_container_width=False):
    with open("sample_data/sample_resume.txt", "r") as f:
        resume_text = f.read()
    with open("sample_data/sample_job.txt", "r") as f:
        job_text = f.read()
    st.rerun()

# ── Analysis ──────────────────────────────────────────────────────
if analyse_btn:
    if not resume_text.strip() or not job_text.strip():
        st.error("⚠️ Please provide both resume text and job description before analysing.")
        st.stop()

    with st.spinner("🔍 Analysing your resume against the job description..."):
        time.sleep(0.5)
        score, matched_kw, missing_kw, all_jd_kw = compute_match_score(resume_text, job_text)
        resume_kw = extract_keywords(resume_text)

    st.markdown("---")
    st.markdown("## 📊 Match Results")

    # Score + gauge
    r1, r2, r3 = st.columns([1, 2, 1])
    with r1:
        if score >= 75:
            verdict = "🟢 Strong Match"
            color = "#065F46"
        elif score >= 50:
            verdict = "🟡 Moderate Match"
            color = "#92400E"
        else:
            verdict = "🔴 Weak Match"
            color = "#991B1B"

        st.markdown(f"""
        <div class="score-box">
            <div class="score-num">{score}%</div>
            <div style="font-size:1.1rem; font-weight:600; color:{color};">{verdict}</div>
            <div style="color:#6B7280; font-size:0.85rem; margin-top:0.4rem;">Compatibility Score</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        fig = plot_score_gauge(score)
        st.plotly_chart(fig, use_container_width=True)

    with r3:
        st.metric("✅ Matched Keywords", len(matched_kw))
        st.metric("❌ Missing Keywords", len(missing_kw))
        st.metric("📋 JD Keywords Total", len(all_jd_kw))

    st.markdown("<br>", unsafe_allow_html=True)

    # Keyword breakdown
    kw1, kw2 = st.columns(2)
    with kw1:
        st.markdown("#### ✅ Skills You Have")
        if matched_kw:
            tags_html = " ".join([f'<span class="matched-tag">{k}</span>' for k in sorted(matched_kw)])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.info("No direct keyword matches found.")

    with kw2:
        st.markdown("#### ❌ Skills You're Missing")
        if missing_kw:
            tags_html = " ".join([f'<span class="missing-tag">{k}</span>' for k in sorted(missing_kw)])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.success("🎉 You match all required keywords!")

    # Skill gap chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📉 Skill Gap Analysis")
    fig2 = plot_skill_gap(matched_kw, missing_kw)
    st.plotly_chart(fig2, use_container_width=True)

    # LLM Feedback
    if use_llm:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🤖 AI-Powered Improvement Tips")
        with st.spinner("🧠 Getting personalised feedback from LLaMA 3..."):
            feedback = get_llm_feedback(resume_text, job_text, score, list(missing_kw), list(matched_kw))

        st.markdown(f"""
        <div class="section-card">
        {feedback}
        </div>
        """, unsafe_allow_html=True)

    # Download report
    st.markdown("<br>", unsafe_allow_html=True)
    report = f"""AI RESUME-JOB MATCH REPORT
================================
Match Score     : {score}%
Verdict         : {verdict}
Matched Skills  : {', '.join(sorted(matched_kw))}
Missing Skills  : {', '.join(sorted(missing_kw))}

AI FEEDBACK:
{feedback if use_llm else 'Enable LLM feedback to get personalised tips.'}
"""
    st.download_button(
        label="📥 Download Report (.txt)",
        data=report,
        file_name="match_report.txt",
        mime="text/plain"
    )
