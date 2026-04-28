import streamlit as st
import json
import os
from utils import extract_text_from_pdf, clean_json_string, create_pdf_report
from agent_logic import analyze_resume, generate_roadmap

# 1. Page Configuration
st.set_page_config(
    page_title="AI Skill-Gap Strategist",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session State to prevent refresh issues
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.data = None
    st.session_state.feedback = None
    st.session_state.roadmap = None

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Header Section
st.title("🤖 AI Skill-Gap Strategist")
st.subheader("AI Agent for Intelligent Skill Gap Analysis and ATS Optimization")

# --- ARCHITECTURE OVERVIEW (Visible for Internship Review) ---
with st.expander("🛠️ System Architecture: Multi-Agent Orchestration", expanded=False):
    st.write("""
    This tool utilizes a **Decoupled Agentic Architecture**:
    - **Analyst Agent (Llama 3.3):** Optimized for high-speed structured data extraction.
    - **Strategist Agent (Gemini 3.1):** Performs semantic reasoning and gap identification.
    - **Mentorship Agent (Gemini 3.1):** Generates personalized, time-bound upskilling roadmaps.
    """)
st.markdown("---")

# 3. Input Section
col1, col2 = st.columns(2)
with col1:
    st.header("📄 1. Upload Resume")
    resume_file = st.file_uploader("Upload your Resume (PDF format)", type="pdf")

with col2:
    st.header("📝 2. Job Description")
    jd_text = st.text_area("Paste the target Job Description (JD) here...", height=215)

# 4. Analysis Logic
if st.button(" Run Intelligence Analysis", use_container_width=True):
    if resume_file and jd_text:
        with st.spinner("Our AI Agents are collaborating on your profile..."):
            try:
                # Step A: Extraction
                resume_text = extract_text_from_pdf(resume_file)
                
                # Step B: LLM Analysis
                skills_json_raw, feedback_raw = analyze_resume(resume_text, jd_text)
                
                # Step C: Cleaning & Parsing
                cleaned_json = clean_json_string(skills_json_raw)
                data = json.loads(cleaned_json)
                
                # Step D: Process Feedback & Roadmap
                feedback = feedback_raw[0]['text'] if isinstance(feedback_raw, list) else feedback_raw
                missing_list = data.get("missing_skills", [])
                roadmap_raw = generate_roadmap(missing_list)
                roadmap = roadmap_raw[0]['text'] if isinstance(roadmap_raw, list) else roadmap_raw

                # SAVE TO SESSION STATE
                st.session_state.data = data
                st.session_state.feedback = feedback
                st.session_state.roadmap = roadmap
                st.session_state.analysis_done = True
                
            except Exception as e:
                st.error("Analysis failed. Please check your API keys or file format.")
                st.exception(e)
    else:
        st.warning("Please provide both documents.")

# 5. Persistent Display Section (Prevents Refresh Loss)
if st.session_state.analysis_done:
    data = st.session_state.data
    feedback = st.session_state.feedback
    roadmap = st.session_state.roadmap

    st.success("Analysis Complete!")
    
    # Big Match Score
    score = data.get("match_percentage", 0)
    st.metric(label="Overall ATS Match Score", value=f"{score}%")
    
    # Skills Columns
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### ✅ Matched Skills")
        for skill in data.get("matched_skills", []):
            st.success(f"**{skill}**")
    
    with c2:
        st.markdown("### 🚩 Missing Skills")
        for skill in data.get("missing_skills", []):
            st.error(f"**{skill}**")

    # Feedback
    st.markdown("---")
    st.header("👔 Recruiter Feedback & ATS Tips")
    st.markdown(feedback)

    # Roadmap
    st.markdown("---")
    st.header("📅 4-Week 'Path to Hired' Roadmap")
    with st.expander("View Your Personalized Study Plan", expanded=True):
        st.markdown(roadmap)

    # PDF Download (Now stable because data is in Session State)
    st.markdown("---")
    full_report_content = f"{feedback}\n\n" + "="*40 + "\nPERSONALIZED 4-WEEK ROADMAP\n" + "="*40 + f"\n\n{roadmap}"
    report_path = create_pdf_report(score, data.get("matched_skills", []), data.get("missing_skills", []), full_report_content)
    
    with open(report_path, "rb") as f:
        st.download_button(
            label=" Download Full Intelligence Report (PDF)",
            data=f,
            file_name=f"Resume_Analysis_{score}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.caption("Powered by Gemini 3.1 Flash-Lite & Llama 3.3 | Built by Deeksha D Shenoy")