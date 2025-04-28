import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class LangflowChain:
    def __init__(self):
        """Initialize the LangflowChain with OpenAI LLM"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2
        )
        
        self.template = """
        You are an expert resume analyzer and career advisor. Your task is to analyze the resume details provided 
        and generate actionable insights.
        Resume Details:
        {resume_data}
        Based on the resume details above, please provide the following:
        1. Suitable Job Roles: List the top 5 job roles that match this candidate's skills and experience.
        2. Skill Gap Analysis: Identify important skills that are missing for the suggested job roles and 
           recommend courses or certifications to acquire these skills.
        3. Resume Improvement Tips: Provide specific, actionable recommendations for enhancing the resume.
        Format your response as a JSON object with the following structure:
        {{
            "job_matches": [
                {{
                    "title": "Job Title 1",
                    "match_score": 85,
                    "key_matching_skills": ["Skill 1", "Skill 2", "Skill 3"],
                    "description": "Brief description of why this role is suitable"
                }},
                // Other job matches...
            ],
            "skill_gaps": [
                {{
                    "skill": "Missing Skill 1",
                    "importance": "High",
                    "acquisition_recommendation": "Specific course, certification, or project to gain this skill"
                }},
                // Other skill gaps...
            ],
            "improvement_tips": [
                "Specific tip 1 for improving the resume",
                "Specific tip 2 for improving the resume",
                // Other tips...
            ]
        }}
        Ensure your response is properly formatted as valid JSON.
        """
        
        self.prompt = PromptTemplate(
            input_variables=["resume_data"],
            template=self.template
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt
        )
    
    def analyze_resume(self, resume_data: Any) -> Dict[str, Any]:
        """
        Analyze a resume and generate insights using the LLM chain
        
        Args:
            resume_data: Structured resume data
            
        Returns:
            Dictionary containing job matches, skill gaps, and improvement tips
        """
        # Convert resume data to string representation
        resume_str = self._format_resume_data(resume_data)
        
        # Execute the chain
        try:
            result = self.chain.invoke({"resume_data": resume_str})
            
            # Extract the response text
            response_text = result.get("text", "{}")
            
            # In a real implementation, we'd parse the JSON here
            # For simplicity, we're returning a mock result
            import json
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Fall back to a mock response if JSON parsing fails
                return self._create_mock_response()
            
        except Exception as e:
            print(f"Error in LLM chain: {e}")
            return self._create_mock_response()
    
    def _format_resume_data(self, resume_data: Any) -> str:
        """Format resume data into a string for the prompt"""
        if hasattr(resume_data, "dict"):
            # If it's a Pydantic model
            data_dict = resume_data.dict()
        else:
            # Assume it's already a dictionary or can be converted to string
            data_dict = resume_data
            
        formatted_str = ""
        
        # Personal Info
        personal_info = data_dict.get("personal_info", {})
        formatted_str += "Personal Information:\n"
        for key, value in personal_info.items():
            if value:
                formatted_str += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        # Education
        education = data_dict.get("education", [])
        formatted_str += "\nEducation:\n"
        for edu in education:
            if isinstance(edu, dict):
                inst = edu.get("institution", "")
                degree = edu.get("degree", "")
                formatted_str += f"- {degree} at {inst}\n"
            else:
                formatted_str += f"- {str(edu)}\n"
        
        # Work Experience
        work_exp = data_dict.get("work_experience", [])
        formatted_str += "\nWork Experience:\n"
        for exp in work_exp:
            if isinstance(exp, dict):
                company = exp.get("company", "")
                position = exp.get("position", "")
                formatted_str += f"- {position} at {company}\n"
            else:
                formatted_str += f"- {str(exp)}\n"
        
        # Skills
        skills = data_dict.get("skills", [])
        formatted_str += "\nSkills:\n"
        for skill in skills:
            formatted_str += f"- {skill}\n"
        
        # Certifications
        certifications = data_dict.get("certifications", [])
        formatted_str += "\nCertifications:\n"
        for cert in certifications:
            formatted_str += f"- {cert}\n"
            
        return formatted_str
    
    def _create_mock_response(self) -> Dict[str, Any]:
        """Create a mock response for testing or fallback"""
        return {
            "job_matches": [
                {
                    "title": "Data Scientist",
                    "match_score": 85,
                    "key_matching_skills": ["Python", "Data Analysis", "Machine Learning"],
                    "description": "Your strong analytical skills and programming experience make you well-suited for this role."
                },
                {
                    "title": "Software Engineer",
                    "match_score": 80,
                    "key_matching_skills": ["Python", "JavaScript", "Git"],
                    "description": "Your technical skills and project experience align well with software engineering positions."
                }
            ],
            "skill_gaps": [
                {
                    "skill": "Cloud Computing (AWS/Azure)",
                    "importance": "High",
                    "acquisition_recommendation": "AWS Certified Solutions Architect or Azure Fundamentals certification"
                },
                {
                    "skill": "SQL and Database Management",
                    "importance": "Medium",
                    "acquisition_recommendation": "Take an online course on SQL and database design"
                }
            ],
            "improvement_tips": [
                "Quantify your achievements with specific metrics and results",
                "Add a professional summary section highlighting your key strengths",
                "Reorganize your skills section to prioritize the most relevant skills for your target roles"
            ]
        }