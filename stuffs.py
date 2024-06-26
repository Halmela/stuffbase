from db import db
from sqlalchemy.sql import text
from flask import session
from result import Ok, Err
from properties import attach_numeric_property, attach_text_property


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
        attach_numeric_property(id, 1, id)
        attach_text_property(id, 1, name)

        db.session.commit()
        return Ok(id)
    except Exception as e:
        return Err(e)


def is_owner(stuff_id):
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Stuffs
                WHERE id = COALESCE(:stuff_id,0)
                  AND owner = COALESCE(:user_id,0)
            """)
        result = db.session.execute(sql, {"stuff_id": stuff_id,
                                          "user_id": session["user_id"]})
        owner = bool(int(result.scalar()))
        if owner:
            return Ok(stuff_id)
        else:
            return Err(f"You do not own #{stuff_id}")
    except Exception as e:
        return Err(e)
