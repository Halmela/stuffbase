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
        """)
        db.session.execute(sql, {"username": username, "password": hash_value})
    except Exception as e:
        return (False, e)

    try:
        user_id = text("SELECT id FROM users WHERE username=:username")
        result = db.session.execute(user_id, {"username": username})
        user_id = result.fetchone().id
        if not user_id:
            return (False, "User not created correctly")
        sql = text("""
            INSERT INTO Stuffs (name, description, owner)
            VALUES ('Root', 'Root node', :owner)
            """)
        db.session.execute(sql, {"owner": user_id})
        root = text("""
            INSERT INTO Roots (root, owner)
            VALUES ((SELECT id FROM Stuffs WHERE name='Root' AND owner=:owner),:owner)
            """)
        db.session.execute(root, {"owner": user_id})
        db.session.commit()
    except Exception as e:
        return (False, e)

    return login(username, password)


def user_id():
    return session.get("user_id", 0)