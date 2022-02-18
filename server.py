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
    country = request.args.get("country")
    if word:
        word = word.lower()
        # country = country.lower()
        fromdb = db.get(word)
        if fromdb:
            jobs = fromdb
        else:
            jobs = search_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "search.html",
        searchFor=word,
        workWhere=country,
        resultsNum=len(jobs),
        jobs=jobs,
    )


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
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
