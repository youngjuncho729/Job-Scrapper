import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from search.models import jobList
from utils import main, tocsv


def index(request):
    return render(request, "search/index.html")


def search(request):
    word = request.GET.get("word", None)
    location = request.GET.get("location", None)

    location = location.lower() if location else ""
    print(word, location)
    if word:
        word = word.lower()
        try:
            jobs = jobList.objects.get(word=word, location=location)
        except jobList.DoesNotExist:
            jobs_list = main.search_jobs(word, location)
            jobs_list = json.dumps(jobs_list)
            jobs = jobList(word=word, location=location, list=jobs_list)
            jobs.save()

    else:
        return redirect("/")

    jsonDec = json.decoder.JSONDecoder()
    jobs_List = jsonDec.decode(jobs.list)

    items_per_page = 50
    total_jobs = len(jobs_List)

    pages = (total_jobs - 1) // items_per_page + 1 if total_jobs > 0 else 1

    page = request.GET.get("page", None)
    if not page:
        page = 1
    else:
        page = int(page)
        page = max(1, min(page, pages))

    jobs_per_page = jobs_List[
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
        jobs = jobList.objects.get(word=word, location=location)
    except jobList.DoesNotExist:
        raise Exception()

    jsonDec = json.decoder.JSONDecoder()
    jobs_List = jsonDec.decode(jobs.list)

    tocsv.save_to_csv(jobs_List)

    filepath = "./jobs.csv"
    with open(filepath, "rb") as f:
        csv_bytes = f.read()

    response = HttpResponse(csv_bytes, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="job.csv"'
    return response
