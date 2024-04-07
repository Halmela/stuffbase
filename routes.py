from app import app
from flask import render_template, request, redirect, session
import users, stuffs


@app.route("/")
def index():
    if "root_id" in session:
        root_info = stuffs.get_information(session["root_id"])
        return render_template("index.html", root_info=root_info)
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        logged = users.login(username, password)
        if logged[0]:
            return redirect("/")
        else:
            return render_template("error.html", message=logged[1])


@app.route("/newrootstuff", methods=["POST"])
def new_rootstuff():
    name = request.form["name"]
    description = request.form["description"]
    result = stuffs.new_rootstuff(name, description)

    if result[0]:
        return redirect("/")
    else:
        return render_template("error.html", message=result[1])


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html",
                                   message="Passwords are not the same")
        result = users.register(username, password1)
        if result[0]:
            return redirect("/")
        else:
            return render_template("error.html", message=result[1])
