#!/usr/bin/env python
import os
from resume_crew.crew import ResumeCrew

def run():
    job_url = os.getenv("JOB_URL", "https://www.google.com/about/careers/applications/jobs/results/123886131107242694-technical-program-manager-ii-data-operations-geo")
    company_name = os.getenv("COMPANY_NAME", "Google")

    inputs = {
        'job_url': job_url,
        'company_name': company_name
    }
    
    crew_instance = ResumeCrew()
    result = crew_instance.crew().kickoff(inputs=inputs)
    return result

if __name__ == "__main__":
    run()