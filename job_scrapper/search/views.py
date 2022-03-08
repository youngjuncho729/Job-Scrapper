from tkinter import E
from django.http import HttpResponse
from django.shortcuts import render, redirect
from utils import main, tocsv

# Create your views here.

db = {}


def index(request):
    return render(request, "search/index.html")


def search(request):
    word = request.GET.get("word", None)
    location = request.GET.get("country", None)

    location = location.lower() if location else ""

    if word:
        word = word.lower()
        fromdb = db.get((word, location))
        if fromdb:
            jobs = fromdb
        else:
            jobs = main.search_jobs(word, location)
            db[(word, location)] = jobs
    else:
        return redirect("/")

    items_per_page = 50
    total_jobs = len(jobs)

    pages = (len(jobs) - 1) // items_per_page + 1 if len(jobs) > 0 else 1

    page = request.GET.get("page", None)
    if not page:
        page = 1
    else:
        page = int(page)
        page = max(1, min(page, pages))

    jobs = jobs[(page - 1) * items_per_page : min(page * items_per_page, total_jobs)]

    data_dict = {
        "searchFor": word,
        "workWhere": location,
        "resultsNum": total_jobs,
        "jobs": jobs,
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
    jobs = db.get((word, location))
    if not jobs:
        raise Exception()
    tocsv.save_to_csv(jobs)

    filepath = "./jobs.csv"
    with open(filepath, "rb") as f:
        csv_bytes = f.read()

    response = HttpResponse(csv_bytes, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="job.csv"'
    return response
