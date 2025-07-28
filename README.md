# Resume-automation Crew (Using CrewAI)

Welcome to the my Resume-automation Crew project, made using CrewAI.
This tool is designed to help you tailor and optimize your Resume according to company's job profile.
<img width="1243" height="632" alt="Screenshot 2025-07-28 at 9 12 22 PM" src="https://github.com/user-attachments/assets/5d347e14-57a4-43b2-95bc-3aa7dfa2047b" />
  
## How it'll help you:

**Job Analysis:** Analyzes what skills and qualifications are required for this job.
**Resume Matching:** Grades the resume and checks whether the resume is relavant to job or not. Thus suggesting improvements.
**Company researcher:** Gathers company insights, a brief background check and provides potential interview questions.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

1. First, if you haven't already, install uv:

```bash
pip install uv
```

2. Next, Clone this project repository and install the dependencies:

```bash
git clone https://github.com/Aagam-Sancheti/Resume-automation-suite.git
cd Resume-automation-suite
```
3. Setup a virtual python environment (if you don't already have one or don't know how to make one)

```bash
python3 -m venv .venv
source .venv/bin/activate
```
   
4. Lock the dependencies (this will happen automatically as you run this command) and install them by using the CLI command:

```bash
crewai install
```

## Environment Setup and Customizing :

1. Copy .env.example to .env:

```bash
cp .env.example .env
```

2.Add your API keys to .env:
* Required:
  + OPENAI_API_KEY: OpenAI API key
  + SERPER_API_KEY: Serper API key for web search

**Note**: For Gemini models, use the model name without prefix (e.g., `gemini-2.0-flash`)

## Running the Project

1. Save your resume as PDF in the knowledge directory
   You can try with my sample resume which I downloaded from sample resume site.

2. To specify the job profile and company name, modify 'job_url' and 'company_name' in ==main.py== 

3. Then to kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```
This command initializes the resume-crew Crew, assembling the agents and assigning them tasks as defined in your configuration.
This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

My resume-automation-suite Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

The system uses five specialized AI agents:

  1. Job Analyzer: Extracts and analyzes job requirements
  2. Resume Analyzer: Scores resume match and suggests improvements
  3. Company Researcher: Gathers company information for interviews
  4. Resume Writer: Gives out the optimized resume
  5. Final report generator: Generates a summarised final report based on given resume and comapny job profile

## Support

For support, questions, or feedback regarding the Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)
