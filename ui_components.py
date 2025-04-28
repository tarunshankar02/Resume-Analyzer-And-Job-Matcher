import streamlit as st
from typing import Dict, List, Any, Optional

def render_header():
    """Render the application header"""
    st.title("📄 Resume Analyzer & Job Matcher")
    st.markdown("""
    Upload your resume to get personalized job matches, identify skill gaps, 
    and receive recommendations for improvement.
    """)
    st.divider()

def render_upload_section():
    """Render the file upload section"""
    st.subheader("Upload Your Resume")
    st.markdown("Supported formats: PDF, DOCX")
    
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        
        with st.expander("File Details"):
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
    
    return uploaded_file

def render_results_section(
    resume_data: Any, 
    job_matches: List[Dict[str, Any]], 
    skill_gaps: List[Dict[str, Any]], 
    improvement_tips: List[str]
):
    """Render the results section with analysis output"""
    st.divider()
    st.header("Analysis Results")
    
    # Create tabs for different result categories
    tab1, tab2, tab3 = st.tabs(["Job Matches", "Skill Gaps", "Resume Improvement"])
    
    # Tab 1: Job Matches
    with tab1:
        st.subheader("Recommended Job Roles")
        if not job_matches:
            st.info("No job matches found. Please try uploading a different resume.")
        else:
            for i, job in enumerate(job_matches):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {i+1}. {job.get('title', 'Unknown Job')}")
                        st.markdown(f"**Match Score:** {job.get('match_score', 'N/A')}%")
                        st.markdown(f"**Description:** {job.get('description', 'No description available')}")
                    with col2:
                        st.markdown("**Matching Skills:**")
                        for skill in job.get('key_matching_skills', []):
                            st.markdown(f"- {skill}")
                st.divider()
    
    # Tab 2: Skill Gaps
    with tab2:
        st.subheader("Skill Gap Analysis")
        if not skill_gaps:
            st.info("No skill gaps identified.")
        else:
            for skill_gap in skill_gaps:
                with st.container():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"### {skill_gap.get('skill', 'Unknown Skill')}")
                        st.markdown(f"**Importance:** {skill_gap.get('importance', 'Medium')}")
                    with col2:
                        st.markdown("**How to acquire this skill:**")
                        st.markdown(skill_gap.get('acquisition_recommendation', 'No recommendation available'))
                st.divider()
    
    # Tab 3: Resume Improvement
    with tab3:
        st.subheader("Resume Improvement Tips")
        if not improvement_tips:
            st.info("No improvement tips available.")
        else:
            for i, tip in enumerate(improvement_tips):
                st.markdown(f"**{i+1}.** {tip}")

def render_footer():
    """Render the application footer"""
    st.divider()
    st.markdown("""
    **Note:** This application uses AI to analyze your resume and provide recommendations. 
    The results should be considered as suggestions and may not be 100% accurate.
    """)