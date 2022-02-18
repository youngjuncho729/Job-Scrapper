import requests
from bs4 import BeautifulSoup


def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    if pagination:
        pages = pagination.find_all("a")
        last_span = pages[-1].find("span").string
        if last_span == "next":
            return int(pages[-2].find("span").string)
        else:
            return int(last_span)
    else:
        return 1


def extract_job_info(html):
    content = html.find("div", {"class": "flex--item fl1"})
    job_id = html["data-jobid"]
    job_title = content.find("h2").find("a").string
    job_company = content.find("h3").find("span").get_text(strip=True)
    job_location = (
        content.find("h3").find("span", {"class": "fc-black-500"}).get_text(strip=True)
    )

    job_info = {
        "title": job_title,
        "company": job_company,
        "location": job_location,
        "link": f"https://stackoverflow.com/jobs/{job_id}",
    }
    return job_info


def extract_jobs(last_page, URL):
    job_list = []
    for page in range(last_page):
        print("Scrapping StackOverflow page " + str(page + 1))
        result = requests.get(f"{URL}&pg={page + 1})")
        soup = BeautifulSoup(result.text, "html.parser")
        total_jobs = soup.find(
            "span", {"class": "description fc-light fs-body1"}
        ).get_text(strip=True)
        # Return empty list when there is 0 result
        if total_jobs == "0 jobs":
            return []
        jobs = soup.find_all("div", {"data-jobid": True})
        for job in jobs:
            job = extract_job_info(job)
            job_list.append(job)
    return job_list


def get_stackoverflow(job, location):
    URL = f"https://stackoverflow.com/jobs?q={job}&l={location}"
    print("Finding the number of pages...")
    last_page = get_last_page(URL)
    SOF_jobs = extract_jobs(last_page, URL)
    print("Finished scrapping jobs on StackOverflow")
    return SOF_jobs
