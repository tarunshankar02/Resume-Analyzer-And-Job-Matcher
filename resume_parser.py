import PyPDF2
import docx
import io
import re
from pydantic import BaseModel
from typing import List, Optional, Dict

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    graduation_date: Optional[str] = None

class WorkExperience(BaseModel):
    company: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

class ResumeData(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    work_experience: List[WorkExperience]
    skills: List[str]
    certifications: List[str]
    raw_text: str

class ResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
        self.github_pattern = r'github\.com/([A-Za-z0-9_-]+)'
        self.linkedin_pattern = r'linkedin\.com/in/([A-Za-z0-9_-]+)'

    def parse(self, uploaded_file) -> ResumeData:
        """Parse the uploaded resume file and extract key information"""
        # Extract text from file
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            raw_text = self._extract_text_from_pdf(uploaded_file)
        elif file_extension in ['docx', 'doc']:
            raw_text = self._extract_text_from_docx(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")
        
        # Extract components
        personal_info = self._extract_personal_info(raw_text)
        education = self._extract_education(raw_text)
        work_experience = self._extract_work_experience(raw_text)
        skills = self._extract_skills(raw_text)
        certifications = self._extract_certifications(raw_text)
        
        # Create and return ResumeData
        resume_data = ResumeData(
            personal_info=personal_info,
            education=education,
            work_experience=work_experience,
            skills=skills,
            certifications=certifications,
            raw_text=raw_text
        )
        
        return resume_data
    
    def _extract_text_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    def _extract_text_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(io.BytesIO(file.getvalue()))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_personal_info(self, text) -> PersonalInfo:
        """Extract personal information from resume text"""
        # Basic extraction with regex
        email = re.search(self.email_pattern, text)
        phone = re.search(self.phone_pattern, text)
        github = re.search(self.github_pattern, text)
        linkedin = re.search(self.linkedin_pattern, text)
        
        # First line often contains the name
        lines = text.split('\n')
        name = lines[0].strip() if lines else None
        
        return PersonalInfo(
            name=name,
            email=email.group(0) if email else None,
            phone=phone.group(0) if phone else None,
            github=github.group(1) if github else None,
            linkedin=linkedin.group(1) if linkedin else None
        )
    
    def _extract_education(self, text) -> List[Education]:
        """Extract education information from resume text"""
        # Simple implementation - in a real system this would be more sophisticated
        education_section = self._extract_section(text, ["EDUCATION", "Education", "ACADEMIC BACKGROUND"])
        if not education_section:
            return []
        
        # Very basic parsing - a real implementation would use more sophisticated NLP
        educations = []
        lines = education_section.split('\n')
        current_education = None
        
        for line in lines:
            if not line.strip():
                continue
                
            if any(degree in line for degree in ["Bachelor", "Master", "PhD", "B.S.", "M.S.", "Ph.D"]):
                if current_education:
                    educations.append(current_education)
                
                parts = line.split(',')
                degree = parts[0].strip() if parts else line.strip()
                institution = parts[1].strip() if len(parts) > 1 else ""
                
                current_education = Education(
                    institution=institution,
                    degree=degree
                )
        
        if current_education:
            educations.append(current_education)
            
        return educations
    
    def _extract_work_experience(self, text) -> List[WorkExperience]:
        """Extract work experience from resume text"""
        experience_section = self._extract_section(text, ["EXPERIENCE", "Experience", "WORK EXPERIENCE", "EMPLOYMENT"])
        if not experience_section:
            return []
        
        # Simple implementation
        experiences = []
        lines = experience_section.split('\n')
        current_experience = None
        
        for line in lines:
            if not line.strip():
                continue
                
            if re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b', line):
                if current_experience:
                    experiences.append(current_experience)
                
                # Very simplistic parsing
                company_match = re.search(r'([A-Za-z0-9\s]+)', line)
                company = company_match.group(1).strip() if company_match else "Unknown Company"
                
                position_match = re.search(r'([A-Za-z\s]+)', line)
                position = position_match.group(1).strip() if position_match else "Unknown Position"
                
                current_experience = WorkExperience(
                    company=company,
                    position=position
                )
        
        if current_experience:
            experiences.append(current_experience)
            
        return experiences
    
    def _extract_skills(self, text) -> List[str]:
        """Extract skills from resume text"""
        skills_section = self._extract_section(text, ["SKILLS", "Skills", "TECHNICAL SKILLS"])
        if not skills_section:
            return []
        
        # Simple split by commas and cleanup
        skills_text = skills_section.replace('\n', ' ')
        skills = [skill.strip() for skill in re.split(r'[,•]', skills_text) if skill.strip()]
        
        return skills
    
    def _extract_certifications(self, text) -> List[str]:
        """Extract certifications from resume text"""
        cert_section = self._extract_section(text, ["CERTIFICATIONS", "Certifications", "CERTIFICATES"])
        if not cert_section:
            return []
        
        # Simple split by newlines and cleanup
        certifications = [cert.strip() for cert in cert_section.split('\n') if cert.strip()]
        
        return certifications
    
    def _extract_section(self, text, section_headers) -> str:
        """Extract a section from the resume text based on headers"""
        lines = text.split('\n')
        section_text = ""
        in_section = False
        
        for i, line in enumerate(lines):
            # Check if this line contains a section header
            if any(header in line for header in section_headers):
                in_section = True
                continue
            
            # Check if we've reached the next section
            if in_section and i < len(lines) - 1:
                next_line = lines[i+1]
                if next_line.isupper() and len(next_line.strip()) > 0:
                    break
            
            if in_section:
                section_text += line + "\n"
        
        return section_text.strip()