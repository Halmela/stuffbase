from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import stuffs
import secrets
from os import getenv


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
            session["csrf_token"] = secrets.token_hex(16)
            return (True, "")
        else:
            return (False, "Username and password do not match")


def logout():
    del session["user_id"]
    del session["username"]
    del session["root_id"]
    del session["csrf_token"]


def create_user(username, password):
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
        return (True, user_id)
    except Exception as e:
        return (False, e)


def promote_admin(id):
    try:
        sql = text("""
                INSERT INTO Admins
                VALUES (:id)
            """)
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return (True, None)
    except Exception as e:
        return (False, e)


def admin_exists():
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Admins
            """)
        result = db.session.execute(sql)
        admin = bool(int(result.scalar()))

        if admin:
            return (False, "Admin account already exists")
        return (True, "")
    except Exception as e:
        return (False, e)


def is_admin(id):
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Admins
                WHERE id = :id
            """)
        result = db.session.execute(sql, {"id": id})
        admin = bool(int(result.scalar()))
        return (admin, "" if admin else "You are not a admin")
    except Exception as e:
        return (False, e)


def create_admin():
    username = getenv("ADMIN_USERNAME")
    password = generate_password_hash(getenv("ADMIN_PASSWORD"))
    created = create_user(username, password)
    if not created[0]:
        print("Something went wrong with creating admin account:")
        print(created[1])
        return (False, created[1])

    promoted = promote_admin(created[1])
    if not promoted[0]:
        print("Something went wrong with promoting admin account:")
        print(promoted[1])
        return (False, created[1])

    return login(username, password)
