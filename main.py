from indeed import get_indeed
from stackoverflow import get_stackoverflow
from export import save_to_csv

JOB = "python"

# Extract jobs from indeed.com
indeed_jobs = get_indeed(JOB)
# Extract jobs from stackoverflow.com
stackoverflow_jobs = get_stackoverflow(JOB)

jobs = indeed_jobs + stackoverflow_jobs

# Save results into csv file
save_to_csv(jobs)
