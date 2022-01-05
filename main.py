from indeed import indeed_max_page, extract_indeed_jobs

last_indeed_page = indeed_max_page()
indeed_jobs = extract_indeed_jobs(last_indeed_page)
print(indeed_jobs)