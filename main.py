from indeed import get_indeed
from stackoverflow import get_stackoverflow

indeed_jobs = get_indeed()
stackoverflow_jobs = get_stackoverflow()
jobs = indeed_jobs + stackoverflow_jobs
print(jobs)
