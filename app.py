import streamlit as st
import json
import re

from services.pdf_parser import extract_text_from_pdf
from services.llm_service import analyze_resume

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Load CSS
# -----------------------------
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -----------------------------
# Header
# -----------------------------
st.title("🤖 AI Resume Reviewer")
st.caption("Compare your resume against a job description using Gemini AI.")

st.divider()

# -----------------------------
# Input Section
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf", "docx", "doc"]
    )

with col2:
    job_description = st.text_area(
        "💼 Paste Job Description",
        height=250
    )

st.divider()

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🚀 Analyze Resume", use_container_width=True):

    if not resume or not job_description:
        st.error("Please upload your resume and paste a job description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        with open("uploads/resume.pdf", "wb") as f:
            f.write(resume.read())

        resume_text = extract_text_from_pdf("uploads/resume.pdf")

        response = analyze_resume(
            resume_text,
            job_description
        )

    # -----------------------------
    # Parse JSON Response
    # -----------------------------
    try:
        clean_response = re.sub(r"```json|```", "", response).strip()
        result = json.loads(clean_response)

    except Exception:
        st.error("Unable to parse AI response.")
        st.code(response)
        st.stop()

    st.success("✅ Analysis Complete!")

    st.divider()

    # -----------------------------
    # Match Score
    # -----------------------------
    score = result.get("match_score", 0)

    st.metric(
        label="🎯 Resume Match Score",
        value=f"{score}%"
    )

    st.progress(score / 100)

    st.divider()

    # -----------------------------
    # Skills
    # -----------------------------
    left, right = st.columns(2)

    with left:

        st.subheader("✅ Matching Skills")

        for skill in result.get("matching_skills", []):
            st.success(skill)

    with right:

        st.subheader("❌ Missing Skills")

        for skill in result.get("missing_skills", []):
            st.warning(skill)

    st.divider()

    # -----------------------------
    # Strengths
    # -----------------------------
    st.subheader("💪 Strengths")

    for strength in result.get("strengths", []):
        st.info(strength)

    st.divider()

    # -----------------------------
    # Weaknesses
    # -----------------------------
    st.subheader("⚠️ Weaknesses")

    for weakness in result.get("weaknesses", []):
        st.error(weakness)

    st.divider()

    # -----------------------------
    # Suggestions
    # -----------------------------
    st.subheader("💡 Resume Improvement Suggestions")

    for suggestion in result.get("resume_improvements", []):
        st.info(suggestion)

    st.divider()

    # -----------------------------
    # Raw JSON (Optional)
    # -----------------------------
    with st.expander("📄 View Raw AI Response"):
        st.json(result)