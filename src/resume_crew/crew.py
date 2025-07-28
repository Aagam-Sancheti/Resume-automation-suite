from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
import yaml
import dotenv
import os
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))
import litellm
from .output_framework import (
    JobRequirements,
    ResumeOptimization,
    CompanyResearch
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
agents_path = os.path.join(BASE_DIR, "config/agents.yaml")
tasks_path = os.path.join(BASE_DIR, "config/tasks.yaml")

@CrewBase
class ResumeCrew():
    """ResumeCrew crew"""

    def __init__(self):
        from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
        self.resumePath = PDFKnowledgeSource(
        file_paths="software-engineer-resume-example.pdf",
        enable_embeddings=False
        )
        model_name = os.getenv("MODEL")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        litellm.model_alias_map = {"default": model_name}
        litellm.api_key = gemini_api_key
        self.model = "default"


        # Load YAML configurations
        with open(agents_path, "r") as f:
            self.agents_config = yaml.safe_load(f)
        with open(tasks_path, "r") as f:
            self.tasks_config = yaml.safe_load(f)



    @before_kickoff
    def before_kickoff(self, inputs):
        self.resumePath.load_content()
        documents = self.resumePath.content.get("documents", [])
        all_text = "\n".join(doc.get("page_content", "") for doc in documents)
        print(all_text[:500])  # Print first 500 characters
        return inputs

    # === Agents ===
    @agent
    def job_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['job_analyzer'],
            verbose=True,
            tools=[ScrapeWebsiteTool()],
            llm=self.model
        )

    @agent
    def resume_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_analyzer'],
            verbose=True,
            llm=self.model,
            knowledge_source=[self.resumePath]
        )
            
    @agent
    def company_researcher(self)-> Agent:
        return Agent(
            config=self.agents_config['company_researcher'],
            verbose=True,
            tools=[SerperDevTool()],
            llm=self.model,
        )

    @agent
    def resume_writer(self)-> Agent:
        return Agent(
            config=self.agents_config['resume_writer'],
            verbose=True,
            llm=self.model
        )
            
    @agent
    def report_generator(self)-> Agent:
        return Agent(
            config=self.agents_config['report_generator'],
            verbose=True,
            llm=self.model
        )

    # === Tasks ===
    @task
    def analyze_job_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_job_task'],
            output_file='output/job_analysis.json',
            output_pydantic=JobRequirements
        )

    @task
    def optimize_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config['optimize_resume_task'],
            output_file='output/resume_optimization.json',
            output_pydantic=ResumeOptimization
        )
            
    @task
    def research_company_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_company_task'],
            output_file='output/company_research.json',
            output_pydantic=CompanyResearch
        )
            
    @task
    def generate_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_resume_task'],
            output_file='output/optimized_resume.md'
        )
            
    @task
    def generate_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_task'],
            output_file='output/final_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResumeCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
        
    @after_kickoff
    def after_kickoff(self, result):
        return result