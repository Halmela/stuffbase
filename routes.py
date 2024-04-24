from app import app
from flask import render_template, request, redirect, session, abort
import users, stuffs, properties, relations
from result import Ok, Err


@app.route("/")
def index():
    if "root_id" in session:
        root_info = relations.get_relations(session["root_id"])
        print(root_info)
        return render_template("index.html", root_info=root_info)
    else:
        return render_template("index.html")


@app.route("/admin")
def admin():
    if "user_id" not in session:
        return render_template("index.html")

    if users.is_admin(session["user_id"]):
        return render_template("admin.html")

    inexistant = users.admin_does_not_exist()
    print(inexistant)
    if not inexistant:
        return render_template("error.html", message=inexistant)

    success = users.promote_admin(session["user_id"])
    print(success)

    if not success:
        return render_template("error.html", message=success)

    admin = users.is_admin(session["user_id"])
    print(admin)
    if admin:
        return render_template("admin.html")
    else:
        return render_template("error.html", message=admin)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        logged = users.login(username, password)
        if logged:
            return redirect("/")
        else:
            return render_template("error.html", message=logged)


@app.route("/newrelation", methods=["POST"])
def new_relation():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    description = request.form["description"]
    converse_description = request.form["converse-description"]

    result = relations.new_relation(description, converse_description)
    if result:
        return redirect("/admin")
    return render_template("error.html", message=result)


@app.route("/newproperty", methods=["POST"])
def new_property():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    description = request.form["description"]
    type = request.form["type"]

    admin = users.is_admin(session["user_id"])

    if not admin:
        return redirect("error.html", message=admin)

    if type == "text":
        result = properties.new_text_property(name, description)
    elif type == "numeric":
        result = properties.new_numeric_property(name, description)
    else:
        return redirect("error.html", message="you did a funny")

    if result:
        return redirect("/admin")
    else:
        return render_template("error.html", message=result)


@app.route("/attachtextproperty", methods=["POST"])
def attach_text_property():
    print(request.form)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stuff_id = request.form["stuff_id"]
    property_id = request.form["property_id"]
    text = request.form["text"]

    result = properties.attach_text_property(stuff_id, property_id, text)
    print(result)
    if not result:
        return render_template("error.html", message=result)

    return redirect(f"/stuff/{stuff_id}")


@app.route("/attachnumericproperty", methods=["POST"])
def attach_numeric_property():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stuff_id = request.form["stuff_id"]
    property_id = request.form["property_id"]
    number = request.form["number"]

    result = properties.attach_numeric_property(stuff_id, property_id, number)
    if not result:
        return render_template("error.html", message=result)

    return redirect(f"/stuff/{stuff_id}")


@app.route("/stuff/<int:id>")
def stuff(id):
    if "user_id" not in session or id == session["root_id"]:
        return redirect("/")

    stuff = stuffs.get_stuff(id)
    if not stuff:
        return render_template("error.html",
                               message=f"you do not have stuff with id {id}")

    info = relations.get_relations(id)
    rev_info = relations.get_reverse_relations(id)
    root_attached = any(filter(lambda x: x[0] == session["root_id"],
                               rev_info))
    rev_info = list(filter(lambda x: x[0] != session["root_id"], rev_info))
    stuff_text_props = properties.get_stuff_text_properties(id)
    stuff_num_props = properties.get_stuff_numeric_properties(id)
    stuff_props = stuff_text_props + stuff_num_props
    text_props = properties.get_text_properties().value
    num_props = properties.get_numeric_properties().value
    rel_infos = relations.get_relation_informations()
    print(rel_infos)

    return render_template("stuff.html", stuff=stuff,
                           relations=info,
                           reverse_relations=rev_info,
                           root_attached=root_attached,
                           stuff_props=stuff_props,
                           text_props=text_props,
                           num_props=num_props,
                           rel_infos=rel_infos)


@app.route("/attachrelation", methods=["POST"])
def attach_relation():
    print(request.form)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    info_id = request.form["info_id"]
    relator = request.form["relator_id"]
    new_name = request.form["name"]

    if not new_name:
        return render_template("error.html", message="empty relatee")
    if new_name[0] == '#':
        relatee = Ok(new_name[1:])
    else:
        relatee = stuffs.new_stuff(new_name)

    if relatee:
        result = relations.attach_relation(info_id, relator, relatee.value)
    else:
        return render_template("error.html", message=relatee)

    if result:
        return redirect(f"/stuff/{relator}")
    else:
        return render_template("error.html", message=result)


@app.route("/newrootstuff", methods=["POST"])
def new_rootstuff():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    stuff_id = stuffs.new_stuff(name)
    if stuff_id:
        result = relations.attach_relation(1, session["root_id"],
                                           stuff_id.value)
    else:
        return render_template("error.html", message=stuff_id)

    if result:
        return redirect("/")
    else:
        return render_template("error.html", message=result)


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
        if not created:
            return render_template("error.html", message=created)

        logged = users.login(username, password1)
        if not logged:
            return render_template("error.html", message=logged)

        return redirect("/")
