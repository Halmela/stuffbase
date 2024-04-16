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


@app.route("/admin")
def admin():
    if "user_id" not in session:
        return render_template("index.html")

    if users.is_admin(session["user_id"])[0]:
        return render_template("admin.html")

    inexistant = users.admin_does_not_exist()
    print(inexistant)
    if not inexistant[0]:
        return render_template("error.html", message=inexistant[1])

    success = users.promote_admin(session["user_id"])
    print(success)

    if not success[0]:
        return render_template("error.html", message=success[1])

    admin = users.is_admin(session["user_id"])
    print(admin)
    if admin[0]:
        return render_template("admin.html")
    else:
        return render_template("error.html", message=admin[1])


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


@app.route("/newproperty", methods=["POST"])
def new_property():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    description = request.form["description"]
    type = request.form["type"]

    admin = users.is_admin(session["user_id"])

    if not admin[0]:
        return redirect("error.html", message=admin[0])

    if type == "text":
        stuffs.new_text_property(name, description)
    elif type == "numeric":
        stuffs.new_numeric_property(name, description)
    else:
        return redirect("error.html", message="you did a funny")


@app.route("/stuff/<int:id>")
def stuff(id):
    if "user_id" not in session or id == session["root_id"]:
        return redirect("/")

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
        created = users.create_user(username, password1)
        if not created[0]:
            return render_template("error.html", message=created[1])

        logged = users.login(username, password1)
        if not logged[0]:
            return render_template("error.html", message=logged[1])

        return redirect("/")
