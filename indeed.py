import requests
from bs4 import BeautifulSoup

JOB = "python"
LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?q={JOB}&limit={LIMIT}"
headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
}


def get_last_page(start=0):
    result = requests.get(f"{INDEED_URL}&start={start * 50}", headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find("div", {"class": "pagination"})

    pages = pagination.find_all("a")

    next_page = pagination.find("a", {"aria-label": "Next"})
    if next_page:
        new_start = int(pages[-2].string)
        return get_last_page(new_start)

    else:
        return int(pages[-1].string)


def extract_job_info(html):
    # extract the job link id
    job_id = html["data-jk"]

    result_content = html.find("td", {"class": "resultContent"})
    # extract the job title
    job_title = result_content.find("h2", {
        "class": "jobTitle"
    }).find("span", title=True).string
    # extract the company hiring
    job_company = html.find("span", {"class": "companyName"}).string
    # extract the job location
    location = html.find("div", {"class": "companyLocation"})
    job_location = ""
    for n in location.stripped_strings:
        job_location += (" " + str(n))

    job_info = {
        "title": job_title,
        "company": job_company,
        "location": job_location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}"
    }

    return job_info


def extract_jobs(last_page):
    job_list = []
    for page in range(last_page):
        print("Scrapping indeed page " + str(page + 1))
        result = requests.get(f"{INDEED_URL}&start={page * 50}",
                              headers=headers)
        result_soup = BeautifulSoup(result.text, "html.parser")
        job_cards = result_soup.find_all("a", {"data-jk": True})
        for job in job_cards:
            job = extract_job_info(job)
            job_list.append(job)
    return job_list


def get_indeed():
    print("Finding the number of pages...")
    last_page = get_last_page()
    indeed_jobs = extract_jobs(last_page)
    print("Finished scrapping jobs on indeed")
    return indeed_jobs
