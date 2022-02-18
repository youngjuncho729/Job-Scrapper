import re
from indeed import get_indeed
from stackoverflow import get_stackoverflow
from export import save_to_csv


def search_jobs(job):
    # Extract jobs from indeed.com
    indeed_jobs = get_indeed(job)
    # Extract jobs from stackoverflow.com
    stackoverflow_jobs = get_stackoverflow(job)

    jobs = indeed_jobs + stackoverflow_jobs
    return jobs


if __name__ == "__main__":
    # Save results into csv file
    jobs = search_jobs("python")
    save_to_csv(jobs)
