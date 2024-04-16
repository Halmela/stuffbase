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
        result = stuffs.new_text_property(name, description)
    elif type == "numeric":
        result = stuffs.new_numeric_property(name, description)
    else:
        return redirect("error.html", message="you did a funny")

    if result[0]:
        return redirect("/admin")
    else:
        return render_template("error.html", message=result[1])


@app.route("/attachtextproperty", methods=["POST"])
def attach_text_property():
    print(request.form)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stuff_id = request.form["stuff_id"]
    property_id = request.form["property_id"]
    text = request.form["text"]

    result = stuffs.attach_text_property(stuff_id, property_id, text)
    print(result)
    if not result[0]:
        return render_template("error.html", message=result[1])

    return redirect(f"/stuff/{stuff_id}")


@app.route("/attachnumericproperty", methods=["POST"])
def attach_numeric_property():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stuff_id = request.form["stuff_id"]
    property_id = request.form["property_id"]
    number = request.form["number"]

    result = stuffs.attach_numeric_property(stuff_id, property_id, number)
    if not result[0]:
        return render_template("error.html", message=result[1])

    return redirect(f"/stuff/{stuff_id}")


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
    stuff_text_props = stuffs.get_stuff_text_properties(id)
    stuff_num_props = stuffs.get_stuff_numeric_properties(id)
    stuff_props = stuff_text_props + stuff_num_props
    text_props = stuffs.get_text_properties()[1]
    num_props = stuffs.get_numeric_properties()[1]

    return render_template("stuff.html", stuff=stuff,
                           info=info, rev_info=rev_info,
                           stuff_props=stuff_props,
                           text_props=text_props,
                           num_props=num_props)


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
