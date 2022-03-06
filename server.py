from unittest import result
from flask import Flask, redirect, render_template, request, send_file
from datetime import date
from main import search_jobs
from export import save_to_csv


app = Flask("SuperScrapper")

db = {}


@app.route("/")
def root():
    return render_template("main.html")


@app.route("/search")
def search():
    word = request.args.get("word")
    location = request.args.get("country")

    location = location.lower() if location else ""
    if word:
        word = word.lower()
        fromdb = db.get((word, location))
        if fromdb:
            jobs = fromdb
        else:
            jobs = search_jobs(word, location)
            db[(word, location)] = jobs
    else:
        return redirect("/")

    items_per_page = 50

    pages = (len(jobs) - 1) // items_per_page + 1 if len(jobs) > 0 else 1

    page = request.args.get("page")
    if not page:
        page = 1
    else:
        page = int(page)
        page = max(1, min(page, pages))

    return render_template(
        "search.html",
        searchFor=word,
        workWhere=location,
        resultsNum=len(jobs),
        jobs=jobs,
        page=page,
        pages=pages,
        items_per_page=items_per_page
    )


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        location = request.args.get("location")
        if not word:
            raise Exception()
        word = word.lower()
        location = location.lower() if location else ""
        jobs = db.get((word, location))
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        return send_file(
            f"jobs-{date.today()}.csv",
            as_attachment=True,
            download_name=f"report-{word}.csv",
        )
    except:
        return redirect("/")


app.run()
