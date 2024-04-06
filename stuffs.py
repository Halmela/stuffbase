from db import db
from sqlalchemy.sql import text
from flask import session


def get_root():
    sql = text("SELECT root FROM Roots WHERE owner=:user_id")
    result = db.session.execute(sql, {"user_id": session["user_id"]})
    return result.fetchone().root


def get_stuff(stuff_id):
    sql = text("""
        SELECT id, name, description
        FROM Stuffs
        WHERE id=:stuff_id AND owner=:user_id
    """)
    result = db.session.execute(sql, {"stuff_id": stuff_id, "user_id": session["user_id"]})
    return result.fetchone()


def get_information(stuff_id):
    sql = text("""
    SELECT S.id, S.name, S.description, I.description
    FROM Stuffs S, Informations I
    WHERE I.stuff=:stuff_id AND S.owner=:user_id
    """)
    result = db.session.execute(sql, {"stuff_id": stuff_id, "user_id": session["user_id"]})
    return result.fetchall()
