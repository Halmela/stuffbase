from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import stuffs


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return (False, "Invalid username")
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["root_id"] = stuffs.get_root()
            return (True, "")
        else:
            return (False, "Username and password do not match")


def logout():
    del session["user_id"]
    del session["username"]
    del session["root_id"]


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("""
            INSERT INTO users (username, password)
            VALUES (:username, :password)
            RETURNING id
        """)
        result = db.session.execute(sql, {"username": username,
                                          "password": hash_value})
        user_id = result.scalar()

        if not user_id:
            return (False, "User not created correctly")

        # user is not logged at this point, so we can't use stuffs.new_stuff()
        sql = text("""
            INSERT INTO Stuffs (name, description, owner)
            VALUES (:username, '', :owner)
            RETURNING id
            """)
        result = db.session.execute(sql, {"username": username,
                                          "owner": user_id})
        root_id = result.scalar()
        root = text("""
            INSERT INTO Roots (root, owner)
            VALUES (:root_id, :owner)
            """)
        db.session.execute(root, {"owner": user_id, "root_id": root_id})
        db.session.commit()
    except Exception as e:
        return (False, e)

    return login(username, password)


def user_id():
    return session.get("user_id", 0)
