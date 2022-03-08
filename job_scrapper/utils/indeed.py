from ctypes.wintypes import PINT
import requests
from bs4 import BeautifulSoup

LIMIT = 50


def get_last_page(URL, start=0):
    result = requests.get(f"{URL}&start={start * LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")

    # When there is no result
    country = soup.find("p", {"class": "oocs"})
    if country:
        country_link = country.find("a")["href"]
        return -1

    pagination = soup.find("div", {"class": "pagination"})
    # when there is only one page result
    if not pagination:
        return 1
    pages = pagination.find_all("a")

    next_page = pagination.find("a", {"aria-label": "Next"})
    if next_page:
        new_start = int(pages[-2].string)
        return get_last_page(URL, new_start)

    else:
        return int(pages[-1].string)


def extract_job_info(html):
    # extract the job link id
    job_id = html["data-jk"]

    result_content = html.find("td", {"class": "resultContent"})
    # extract the job title
    job_title = (
        result_content.find("h2", {"class": "jobTitle"}).find("span", title=True).string
    )
    # extract the company hiring
    job_company = html.find("span", {"class": "companyName"}).string
    # extract the job location
    location = html.find("div", {"class": "companyLocation"})
    job_location = ""
    for n in location.stripped_strings:
        job_location += " " + str(n)

    job_info = {
        "title": job_title,
        "company": job_company,
        "location": job_location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}",
    }

    return job_info


def extract_jobs(last_page, URL):
    job_list = []
    if last_page == -1:
        return job_list
    for page in range(last_page):
        print("Scrapping indeed page " + str(page + 1))
        result = requests.get(f"{URL}&start={page * 50}")
        result_soup = BeautifulSoup(result.text, "html.parser")
        job_cards = result_soup.find_all("a", {"data-jk": True})
        for job in job_cards:
            job = extract_job_info(job)
            job_list.append(job)
    return job_list


def get_indeed(job, location):
    URL = f"https://www.indeed.com/jobs?q={job}&l={location}&limit={LIMIT}"
    print("Finding the number of pages...")
    last_page = get_last_page(URL)
    indeed_jobs = extract_jobs(last_page, URL)
    print("Finished scrapping jobs on indeed")
    return indeed_jobs
