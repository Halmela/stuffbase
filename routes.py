from app import app
from flask import render_template, request, redirect, session, abort
import users, stuffs, properties, relations
from result import Ok, Err, to_result


@app.route("/")
def index():
    if "root_id" in session:
        return redirect(f"/stuff/{session['root_id']}")
    else:
        return render_template("index.html")


@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect("/")

    if users.is_admin(session["user_id"]):
        return render_template("admin.html")

    inexistant = users.admin_does_not_exist()
    if not inexistant:
        return error(inexistant.error)

    success = users.promote_admin(session["user_id"])
    if not success:
        return error(success.error)

    admin = users.is_admin(session["user_id"])
    if admin:
        return render_template("admin.html")
    else:
        return error(admin.error)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        return (to_result([request.form.get("username")],
                          error="Supply an username")
                + to_result([request.form.get("password")],
                            error="Supply an password")) \
            .then(lambda l: users.login(l[0], l[1])) \
            .conclude(lambda _: redirect("/"), error)


@app.route("/newrelation", methods=["POST"])
def new_relation():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    description = request.form["description"]
    converse_description = request.form["converse-description"]

    return relations.new_relation(description, converse_description) \
        .conclude(lambda _: redirect("/admin"), error)


@app.route("/newproperty", methods=["POST"])
def new_property():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    description = request.form["description"]
    type = request.form["type"]

    admin = users.is_admin(session["user_id"])

    if not admin:
        return error(admin.error)

    if type == "text":
        result = properties.new_text_property(name, description)
    elif type == "numeric":
        result = properties.new_numeric_property(name, description)
    else:
        return error("you did a funny")

    if result:
        return redirect("/admin")
    else:
        return error(result.error)


@app.route("/attachtextproperty", methods=["POST"])
def attach_text_property():
    print(request.form)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stuff_id = to_result(request.form.get("stuff_id")) \
        .then(lambda x: int(x), error="Stuff id is not a number") \
        .then(stuffs.is_owner)
    if stuff_id:
        stuff_id = stuff_id.value
    else:
        return error(stuff_id.error)

    property_id = to_result(request.form.get("property_id")) \
        .then(lambda x: int(x), error="Property id is not a number") \
        .then(properties.text_property_exists)
    if property_id:
        property_id = property_id.value
    else:
        return error(property_id.error)

    text = to_result(request.form.get("text")) \
        .check(lambda x: bool(x), "Supply text for the property")
    if text:
        text = text.value
    else:
        return error(text.error)

    result = properties.attach_text_property(stuff_id, property_id, text)
    print(result)
    if not result:
        return error(result.error)

    return redirect(f"/stuff/{stuff_id}")


@app.route("/attachnumericproperty", methods=["POST"])
def attach_numeric_property():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stuff_id = to_result(request.form.get("stuff_id")) \
        .then(lambda x: int(x), error="Stuff id is not a number") \
        .then(stuffs.is_owner)
    if stuff_id:
        stuff_id = stuff_id.value
    else:
        return error(stuff_id.error)

    property_id = to_result(request.form.get("property_id")) \
        .then(lambda x: int(x), error="Property id is not a number") \
        .then(properties.numeric_property_exists)
    if property_id:
        property_id = property_id.value
    else:
        return error(property_id.error)

    number = to_result(request.form.get("number")) \
        .then(lambda x: int(x), error="Supply a numeric value")
    if number:
        number = number.value
    else:
        return error(number.error)

    result = properties.attach_numeric_property(stuff_id, property_id, number)
    if not result:
        return error(result.error)

    return redirect(f"/stuff/{stuff_id}")


@app.route("/stuff/<int:id>")
def stuff(id):
    if "user_id" not in session:
        return redirect("/")

    stuff = stuffs.get_stuff(id)
    if not stuff:
        return error(f"you do not have stuff with id {id}")

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

    session["current"] = id

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

    stuff_relates = request.form.get("stuff_relates")
    if stuff_relates == "true":
        stuff_relates = True
    elif stuff_relates == "false":
        stuff_relates = False
    else:
        return error("misused form")

    stuff_id = to_result(request.form.get("stuff_id")) \
        .then(lambda x: int(x), error="Invalid stuff id") \
        .then(stuffs.is_owner)
    if stuff_id:
        stuff_id = stuff_id.value
    else:
        return error(stuff_id.error)

    info_id = to_result(request.form["info_id"]) \
        .then(lambda x: int(x), error="Invalid relation id") \
        .then(relations.relation_exists)
    if info_id:
        info_id = info_id.value
    else:
        return error(info_id.error)

    new = to_result(request.form["name"]) \
        .check(lambda name: len(name) > 1,
               "name should be 2 or more chars") \
        .check(lambda name: len(name) < 20,
               "name should be less than 20 chars") \
        .branch(lambda name: name[0] == '#',
                lambda r: stuffs.is_owner(r[1:]),
                stuffs.new_stuff)
    if new:
        new = new.value
    else:
        return error(new.error)

    if stuff_relates:
        rel = relations.attach_relation(info_id, stuff_id, new)
    else:
        rel = relations.attach_relation(info_id, new, stuff_id)

    return rel.conclude(lambda _: redirect(f"/stuff/{session['current']}"),
                        error)


@app.route("/newrootstuff", methods=["POST"])
def new_rootstuff():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    result = to_result(request.form.get("name")) \
        .check(lambda x: len(x) < 40, "Too long name") \
        .then(lambda x: stuffs.new_stuff(x)) \
        .then(lambda x: relations.attach_relation(1, session["root_id"], x))

    if result:
        return redirect("/")
    else:
        return error(result.error)


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        return (to_result([request.form.get("username")],
                error="supply an username")
                + to_result([request.form.get("password1")],
                error="supply a password")
                + to_result([request.form.get("password2")],
                error="supply the password twice")) \
            .check(lambda f: f[1] == f[2], "Passwords are not the same") \
            .then(lambda f: users.create_user(f[0], f[1])) \
            .then(lambda u: users.login(u[0], u[1])) \
            .conclude(lambda _: redirect("/"), error)

        # username = request.form["username"]
        # password1 = request.form["password1"]
        # password2 = request.form["password2"]
        # if password1 != password2:
        #     return error("Passwords are not the same")

        # created = users.create_user(username, password1)
        # if not created:
        #     return error(created.error)

        # logged = users.login(username, password1)
        # if not logged:
        #     return error(logged.error)

        # return redirect("/")


def error(message):
    return render_template("error.html", message=message)
