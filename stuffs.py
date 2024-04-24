from db import db
from sqlalchemy.sql import text
from flask import session
from result import Ok, Err


def get_root():
    sql = text("SELECT root FROM Roots WHERE owner=:user_id")
    result = db.session.execute(sql, {"user_id": session["user_id"]})
    return result.fetchone().root


def get_stuff(stuff_id):
    sql = text("""
        SELECT id, name
        FROM Stuffs
        WHERE id=:stuff_id AND owner=:user_id
    """)
    result = db.session.execute(sql, {"stuff_id": stuff_id,
                                      "user_id": session["user_id"]})
    return result.fetchone()


def new_rootstuff(name):
    try:
        sql = text("""
                INSERT INTO Stuffs (name, owner)
                VALUES (:name, :owner)
                RETURNING id
            """)
        result = db.session.execute(sql, {"name": name,
                                          "owner": session["user_id"]})
        sql = text("""
                INSERT INTO Relations (relator, relatee, owner)
                VALUES (:relator, :relatee, :owner)
            """)
        db.session.execute(sql, {"relator": session["root_id"],
                                 "relatee": result.scalar(),
                                 "owner": session["user_id"]})
        db.session.commit()
        return Ok(())
    except Exception as e:
        return Err(e)


# returns (True, int) or (False, str)
# as in (True, stuff_id) or (False, error message)
def new_stuff(name):
    try:
        sql = text("""
                INSERT INTO Stuffs (name, owner)
                VALUES (:name, :owner)
                RETURNING id
            """)
        result = db.session.execute(sql, {"name": name,
                                          "owner": session["user_id"]})
        id = result.scalar()
        db.session.commit()
        return Ok(id)
    except Exception as e:
        return Err(e)


def is_owner(user_id, stuff_id):
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Stuffs
                WHERE id = :stuff_id AND owner = :user_id
            """)
        result = db.session.execute(sql, {"stuff_id": stuff_id,
                                          "user_id": user_id})
        owner = bool(int(result.scalar()))
        if owner:
            return Ok(())
        else:
            return Err("You are not the owner of that")
    except Exception as e:
        return Err(e)
