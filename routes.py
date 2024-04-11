from app import app
from flask import render_template, request, redirect, session, abort
import users, stuffs


@app.route("/")
def index():
    if "root_id" in session:
        root_info = stuffs.get_information(session["root_id"])
        print(root_info)
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


@app.route("/stuff/<int:id>")
def stuff(id):
    if "user_id" not in session or id == session["root_id"]:
        return redirect("/")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stuff = stuffs.get_stuff(id)
    if not stuff:
        return render_template("error.html",
                               message=f"you do not have stuff with id {id}")

    info = stuffs.get_information(id)
    rev_info = stuffs.get_reverse_information(id)
    return render_template("stuff.html", stuff=stuff,
                           info=info, rev_info=rev_info)


@app.route("/newinformation", methods=["POST"])
def new_info():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    new_name = request.form["name"]
    new_description = request.form["description"]
    info_description = request.form["information"]
    stuff_id = request.form["stuff_id"]
    result = stuffs.new_information(new_name, new_description,
                                    info_description, stuff_id)

    if result[0]:
        return redirect(f"/stuff/{stuff_id}")
    else:
        return render_template("error.html", message=result[1])


@app.route("/newrootstuff", methods=["POST"])
def new_rootstuff():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    description = request.form["description"]
    result = stuffs.new_information(name, description, "", session["root_id"])

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
