from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import stuffs
import secrets
from result import Ok, Err


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return Err("Invalid username")
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["root_id"] = stuffs.get_root()
            session["csrf_token"] = secrets.token_hex(16)
            session["current"] = session["root_id"]
            return Ok(())
        else:
            return Err("Username and password do not match")


def logout():
    del session["user_id"]
    del session["username"]
    del session["root_id"]
    del session["csrf_token"]
    del session["current"]


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
            return Err("User not created correctly")

        # user is not logged at this point, so we can't use stuffs.new_stuff()
        sql = text("""
            INSERT INTO Stuffs (name, owner)
            VALUES (:username, :owner)
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
        return Ok(user_id)
    except Exception as e:
        return Err(e)


def promote_admin(id):
    try:
        sql = text("""
                INSERT INTO Admins
                VALUES (:id)
            """)
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return Ok(())
    except Exception as e:
        return Err(e)


def admin_does_not_exist():
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Admins
            """)
        result = db.session.execute(sql)

        return Ok(bool(int(result.scalar()))) \
            .check(lambda x: x, "Admin account exists")
    except Exception as e:
        return Err(e)


def is_admin(id):
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Admins
                WHERE id = :id
            """)
        result = db.session.execute(sql, {"id": id})

        return Ok(bool(int(result.scalar()))) \
            .check(lambda x: x, "You are not an admin")
    except Exception as e:
        return Err(e)
