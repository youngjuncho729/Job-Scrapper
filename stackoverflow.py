import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
}


def get_last_page(URL):
    result = requests.get(URL, headers=headers)
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
        return 0


def extract_job_info(html):
    content = html.find("div", {"class": "flex--item fl1"})
    job_id = html["data-jobid"]
    job_title = content.find("h2").find("a").string
    job_company = content.find("h3").find("span").get_text(strip=True)
    job_location = content.find("h3").find("span", {
        "class": "fc-black-500"
    }).get_text(strip=True)

    job_info = {
        "title": job_title,
        "company": job_company,
        "location": job_location,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }
    return job_info


def extract_jobs(last_page, URL):
    job_list = []
    for page in range(last_page):
        print("Scrapping StackOverflow page " + str(page + 1))
        result = requests.get(f"{URL}&pg={page + 1})", headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")
        jobs = soup.find_all("div", {"data-jobid": True})
        for job in jobs:
            job = extract_job_info(job)
            job_list.append(job)
    return job_list


def get_stackoverflow(JOB):
    URL = f"https://stackoverflow.com/jobs?q={JOB}"
    print("Finding the number of pages...")
    last_page = get_last_page(URL)
    SOF_jobs = extract_jobs(last_page, URL)
    print("Finished scrapping jobs on StackOverflow")
    return SOF_jobs
