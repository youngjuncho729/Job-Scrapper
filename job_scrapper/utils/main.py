from .indeed import get_indeed
from .stackoverflow import get_stackoverflow
from .tocsv import save_to_csv


def search_jobs(job, location):
    # Extract jobs from indeed.com
    indeed_jobs = get_indeed(job, location)

    # Extract jobs from stackoverflow.com
    stackoverflow_jobs = get_stackoverflow(job, location)

    jobs = indeed_jobs + stackoverflow_jobs
    return jobs


if __name__ == "__main__":
    # Save results into csv file
    jobs = search_jobs("python", "california")
    save_to_csv(jobs)
