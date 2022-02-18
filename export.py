import csv
from datetime import date


def save_to_csv(jobs):
    file = open(f"jobs-{date.today()}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
