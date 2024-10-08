import requests
from django.shortcuts import render

def job_list(request):
    # Fetch data from the FastAPI backend
    response = requests.get("http://127.0.0.1:3000/jobs")
    jobs_raw = response.json()["jobs"]
    
    # Parse the job data to make it structured
    jobs = []
    for job in jobs_raw:
        parts = job.split(maxsplit=4)  # Split each line into 5 parts (jobid, retcode, jobname, and status)
        if len(parts) == 5:  # Ensure the line contains all required parts
            job_data = {
                "jobid": parts[0],   # JOB ID
                "retcode": parts[1] + ' ' + parts[2],  # Return code (e.g., CC 0008)
                "jobname": parts[3],  # Job name
                "status": parts[4]    # Status (e.g., OUTPUT)
            }
            jobs.append(job_data)

    return render(request, "jobs/job_list.html", {"jobs": jobs})

def parse_spool_content(spool_content):
    # Split the spool content into sections based on "Spool file" labels
    spool_sections = []
    current_section = None
    
    for line in spool_content.splitlines():
        if line.startswith("Spool file:"):
            if current_section:
                spool_sections.append(current_section)
            current_section = {"title": line, "content": []}
        elif current_section:
            current_section["content"].append(line)
    
    # Append the last section if exists
    if current_section:
        spool_sections.append(current_section)
    
    return spool_sections

def view_spool(request, jobid):
    # Fetch the spool content for the selected job
    response = requests.get(f"http://127.0.0.1:3000/jobs/{jobid}/spool")
    spool_content = response.json()["spool"]
    
    # Parse the spool content into sections
    spool_sections = parse_spool_content(spool_content)
    
    return render(request, "jobs/job_spool.html", {"jobid": jobid, "spool_sections": spool_sections})
