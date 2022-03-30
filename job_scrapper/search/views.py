import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from search.models import JobList
from utils import main, tocsv


def index(request):
    return render(request, "search/index.html")


def search(request):
    word = request.GET.get("word", None)
    location = request.GET.get("location", None)

    location = location.strip().lower() if location else ""
    if word:
        word = word.strip().lower()
        try:
            jobList = JobList.objects.get(word=word, location=location)
            if jobList.date != datetime.date.today():
                jobList.date = datetime.date.today()
                search_result = main.search_jobs(word, location)
                search_result = json.dumps(search_result)
                jobList.list = search_result
                jobList.save()
        except JobList.DoesNotExist:
            search_result = main.search_jobs(word, location)
            search_result = json.dumps(search_result)
            jobList = JobList(word=word, location=location, list=search_result)
            jobList.save()
    else:
        return redirect("/")

    jsonDec = json.decoder.JSONDecoder()
    search_result = jsonDec.decode(jobList.list)

    items_per_page = 50
    total_jobs = len(search_result)

    pages = (total_jobs - 1) // items_per_page + 1 if total_jobs > 0 else 1

    page = request.GET.get("page", None)
    if not page:
        page = 1
    else:
        page = int(page)
        page = max(1, min(page, pages))

    jobs_per_page = search_result[
        (page - 1) * items_per_page : min(page * items_per_page, total_jobs)
    ]

    data_dict = {
        "searchFor": word,
        "workWhere": location,
        "resultsNum": total_jobs,
        "jobs": jobs_per_page,
        "page": page,
        "pages": pages,
        "items_per_page": items_per_page,
    }

    return render(
        request,
        "search/result.html",
        context=data_dict,
    )


def export(request):

    word = request.GET.get("word", None)
    location = request.GET.get("location", None)

    word = word.lower()
    location = location.lower() if location else ""
    try:
        jobList = JobList.objects.get(word=word, location=location)
    except JobList.DoesNotExist:
        raise Exception()

    jsonDec = json.decoder.JSONDecoder()
    search_result = jsonDec.decode(jobList.list)

    tocsv.save_to_csv(search_result)

    filepath = "./jobs.csv"
    with open(filepath, "rb") as f:
        csv_bytes = f.read()

    response = HttpResponse(csv_bytes, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="job.csv"'
    return response
