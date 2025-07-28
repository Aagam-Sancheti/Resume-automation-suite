from typing import List, Dict, Optional
from pydantic import BaseModel, Field, confloat, field_validator
from enum import Enum

# --- ENUMS ---
class JobLevel(str, Enum):
    ENTRY = "Entry"
    MID = "Mid"
    SENIOR = "Senior"
    LEAD = "Lead"
    MANAGER = "Manager"
    DIRECTOR = "Director"

class ClearanceLevel(str, Enum):
    NONE = "None"
    CONFIDENTIAL = "Confidential"
    SECRET = "Secret"
    TOP_SECRET = "Top Secret"

# --- SUBMODELS ---
class Compensation(BaseModel):
    min_salary: Optional[str] = Field(description="Minimum salary (if provided)")
    max_salary: Optional[str] = Field(description="Maximum salary (if provided)")
    currency: Optional[str] = Field(description="Currency for salary")
    bonus: Optional[str] = Field(description="Bonus or incentive details")

class MarketPosition(BaseModel):
    competitors: List[str] = Field(description="List of competitors")
    industry_standing: List[str] = Field(description="Company's standing in the industry")

# --- CORE MODELS ---
class SkillScore(BaseModel):
    skill_name: str = Field(description="Name of the skill being scored")
    is_required: bool = Field(description="Whether this skill is required or nice-to-have")
    match_level: confloat(ge=0, le=1) = Field(description="How well the candidate's experience matches (0-1)")
    years_experience: Optional[float] = Field(description="Years of experience with this skill", default=None)
    context_score: confloat(ge=0, le=1) = Field(
        description="How relevant the skill usage context is to the job requirements",
        default=0.5
    )

class JobMatchScore(BaseModel):
    overall_match: confloat(ge=0, le=100) = Field(description="Overall match percentage (0-100)")
    technical_skills_match: confloat(ge=0, le=100) = Field(description="Technical skills match percentage")
    soft_skills_match: confloat(ge=0, le=100) = Field(description="Soft skills match percentage")
    experience_match: confloat(ge=0, le=100) = Field(description="Experience level match percentage")
    education_match: confloat(ge=0, le=100) = Field(description="Education requirements match percentage")
    industry_match: confloat(ge=0, le=100) = Field(description="Industry experience match percentage")
    skill_details: List[SkillScore] = Field(description="Detailed scoring for each skill", default_factory=list)
    strengths: List[str] = Field(description="List of areas where candidate exceeds requirements", default_factory=list)
    gaps: List[str] = Field(description="List of areas needing improvement", default_factory=list)
    scoring_factors: Dict[str, float] = Field(
        description="Weights used for different scoring components",
        default_factory=lambda: {
            "technical_skills": 0.35,
            "soft_skills": 0.20,
            "experience": 0.25,
            "education": 0.10,
            "industry": 0.10
        }
    )

    @field_validator("overall_match")
    def check_consistency(cls, v, values):
        # Optional: ensure overall_match is not wildly off from weighted components
        return v

class JobRequirements(BaseModel):
    technical_skills: List[str] = Field(default_factory=list, description="List of required technical skills")
    soft_skills: List[str] = Field(default_factory=list, description="List of required soft skills")
    experience_requirements: List[str] = Field(default_factory=list, description="List of experience requirements")
    key_responsibilities: List[str] = Field(default_factory=list, description="List of key job responsibilities")
    education_requirements: List[str] = Field(default_factory=list, description="List of education requirements")
    nice_to_have: List[str] = Field(default_factory=list, description="List of preferred but not required skills")
    job_title: Optional[str] = Field(default=None, description="Official job title")
    department: Optional[str] = Field(default=None, description="Department or team within the company")
    reporting_structure: Optional[str] = Field(default=None, description="Who this role reports to and any direct reports")
    job_level: Optional[JobLevel] = Field(default=None, description="Level of the position")
    location_requirements: Dict[str, str] = Field(default_factory=dict, description="Location details including remote/hybrid options")
    work_schedule: Optional[str] = Field(default=None, description="Expected work hours and schedule flexibility")
    travel_requirements: Optional[str] = Field(default=None, description="Expected travel frequency and scope")
    compensation: Compensation = Field(default_factory=Compensation, description="Salary range and compensation details if provided")
    benefits: List[str] = Field(default_factory=list, description="List of benefits and perks")
    tools_and_technologies: List[str] = Field(default_factory=list, description="Specific tools, software, or technologies used")
    industry_knowledge: List[str] = Field(default_factory=list, description="Required industry-specific knowledge")
    certifications_required: List[str] = Field(default_factory=list, description="Required certifications or licenses")
    security_clearance: Optional[ClearanceLevel] = Field(default=None, description="Required security clearance level if any")
    team_size: Optional[str] = Field(default=None, description="Size of the immediate team")
    key_projects: List[str] = Field(default_factory=list, description="Major projects or initiatives mentioned")
    cross_functional_interactions: List[str] = Field(default_factory=list, description="Teams or departments this role interacts with")
    career_growth: List[str] = Field(default_factory=list, description="Career development and growth opportunities")
    training_provided: List[str] = Field(default_factory=list, description="Training or development programs offered")
    diversity_inclusion: Optional[str] = Field(default=None, description="D&I statements or requirements")
    company_values: List[str] = Field(default_factory=list, description="Company values mentioned in the job posting")
    job_url: Optional[str] = Field(default=None, description="URL of the job posting")
    posting_date: Optional[str] = Field(default=None, description="When the job was posted")
    application_deadline: Optional[str] = Field(default=None, description="Application deadline if specified")
    special_instructions: List[str] = Field(default_factory=list, description="Any special application instructions or requirements")
    match_score: JobMatchScore = Field(default_factory=JobMatchScore, description="Detailed scoring of how well the candidate matches the job requirements")
    score_explanation: List[str] = Field(default_factory=list, description="Detailed explanation of how scores were calculated")

class ResumeOptimization(BaseModel):
    content_suggestions: List[Dict[str, str]] = Field(description="List of content optimization suggestions with 'before' and 'after' examples")
    skills_to_highlight: List[str] = Field(description="List of skills that should be emphasized based on job requirements")
    achievements_to_add: List[str] = Field(description="List of achievements that should be added or modified")
    keywords_for_ats: List[str] = Field(description="List of important keywords for ATS optimization")
    formatting_suggestions: List[str] = Field(description="List of formatting improvements")

class CompanyResearch(BaseModel):
    recent_developments: List[str] = Field(description="List of recent company news and developments", default_factory=list)
    culture_and_values: List[str] = Field(description="Key points about company culture and values", default_factory=list)
    market_position: MarketPosition = Field(description="Company market position, including competitors and industry standing", default_factory=MarketPosition)
    interview_questions: List[str] = Field(description="Strategic questions to ask during the interview", default_factory=list)