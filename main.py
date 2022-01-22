from flask import Flask, render_template, request
from tools import json_read

app = Flask(__name__)

candidates = json_read("candidates.json")
settings = json_read("settings.json")


@app.route("/")
def main_page():
    return render_template("main.html", settings=settings)


@app.route("/candidate/<int:x>")
def candidate_page(x):
    return render_template("candidate.html", id=x, candidates=candidates)


@app.route("/list")
def list_page():
    return render_template("list.html", candidates=candidates)


@app.route("/search/")
def search_page():
    s = request.args.get("name")
    match = []
    if s is None:
        return "<h1>Введите параметр name</h1>"
    if settings["case-sensitive"]:
        s = s.lower()
        for dict_ in candidates:
            if s in dict_['name'].lower():
                match.append({"id": dict_["id"], "name": dict_["name"]})
    else:
        for dict_ in candidates:
            if s in dict_['name'].lower():
                match.append({"id": dict_["id"], "name": dict_["name"]})
    if len(match):
        return render_template("search.html", match=match, quantity=len(match))
    return "<h1>Ничего не найдено</h1>"


@app.route("/skill/<x>")
def skill_page(x):
    match = []
    for dict_ in candidates:
        if x in dict_["skills"].lower():
            match.append({"id": dict_["id"], "name": dict_["name"]})
    match = match[:settings["limit"]]
    return render_template("skill.html", id=x, match=match, quantity=len(match))


@app.errorhandler(404)
def not_found_page(error):
    return render_template("not_found_page.html"), 404


app.run()
