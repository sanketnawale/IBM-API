from fastapi import FastAPI
import subprocess
import main
app = FastAPI()

def get_zos_jobs():
    cmd = [
        'zowe', 'zos-jobs', 'list', 'jobs',
        '--user', 'Your id',
        '--password', 'Your pass',
        '--host', '204.90.115.200',
        '--port', '10443',
        '--ru', 'false'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def get_job_spool(jobid):
    cmd = [
        'zowe', 'zos-jobs', 'view', 'all-spool-content', jobid,
        '--user', 'your id',
        '--password', 'your password',
        '--host', '204.90.115.200',
        '--port', '10443',
        '--ru', 'false'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

@app.get("/jobs")
def list_jobs():
    jobs_data = get_zos_jobs()
    return {"jobs": jobs_data.splitlines()}

@app.get("/jobs/{jobid}/spool")
def view_spool(jobid: str):
    spool_content = get_job_spool(jobid)
    return {"spool": spool_content}
