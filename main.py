from indeed import get_indeed
from stackoverflow import get_stackoverflow
from export import save_to_csv

# Extract jobs from indeed.com
indeed_jobs = get_indeed()
# Extract jobs from stackoverflow.com
stackoverflow_jobs = get_stackoverflow()

jobs = indeed_jobs + stackoverflow_jobs

# Save results into csv file
save_to_csv(jobs)
