import streamlit as st
from resume_parser import ResumeParser
from job_matcher import JobMatcher
from langflow_chain import LangflowChain
from ui_components import (
    render_header,
    render_upload_section,
    render_results_section,
    render_footer
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    st.error("Please set your OPENAI_API_KEY in the .env file")
    st.stop()

# Set page configuration
st.set_page_config(
    page_title="Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
    st.session_state.job_matches = None
    st.session_state.skill_gaps = None
    st.session_state.improvement_tips = None
    st.session_state.processed = False

def main():
    # Render header
    render_header()
    
    # Render upload section
    uploaded_file = render_upload_section()
    
    # Process the uploaded file
    if uploaded_file is not None and st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            # Parse resume
            resume_parser = ResumeParser()
            resume_data = resume_parser.parse(uploaded_file)
            st.session_state.resume_data = resume_data
            
            # Process with LLM
            langflow_chain = LangflowChain()
            analysis_results = langflow_chain.analyze_resume(resume_data)
            
            # Match jobs
            job_matcher = JobMatcher()
            job_matches = job_matcher.find_matches(analysis_results)
            
            # Store results in session state
            st.session_state.job_matches = analysis_results.get("job_matches", [])
            st.session_state.skill_gaps = analysis_results.get("skill_gaps", [])
            st.session_state.improvement_tips = analysis_results.get("improvement_tips", [])
            st.session_state.processed = True
            
            st.success("Resume analyzed successfully!")
    
    # Render results
    if st.session_state.processed:
        render_results_section(
            st.session_state.resume_data,
            st.session_state.job_matches,
            st.session_state.skill_gaps,
            st.session_state.improvement_tips
        )
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
