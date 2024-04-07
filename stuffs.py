from db import db
from sqlalchemy.sql import text
from flask import session


def get_root():
    sql = text("SELECT root FROM Roots WHERE owner=:user_id")
    result = db.session.execute(sql, {"user_id": session["user_id"]})
    return result.fetchone().root


def get_stuff(stuff_id):
    sql = text("""
        SELECT id, name, description, owner
        FROM Stuffs
        WHERE id=:stuff_id AND owner=:user_id
    """)
    result = db.session.execute(sql, {"stuff_id": stuff_id,
                                      "user_id": session["user_id"]})
    return result.fetchone()


def get_information(stuff_id):
    sql = text("""
    SELECT DISTINCT S.id, S.name, S.description, I.description
    FROM Stuffs S JOIN Informations I
                  ON S.id=I.information
    WHERE I.stuff=:stuff_id AND S.owner=:user_id
    """)
    result = db.session.execute(sql, {"stuff_id": stuff_id,
                                      "user_id": session["user_id"]})
    return result.fetchall()


def new_rootstuff(name, description):
    try:
        sql = text("""
                INSERT INTO Stuffs (name, description, owner)
                VALUES (:name, :description, :owner)
                RETURNING id
            """)
        result = db.session.execute(sql, {"name": name,
                                          "description": description,
                                          "owner": session["user_id"]})
        sql = text("""
                INSERT INTO Informations (stuff, information, owner)
                VALUES (:stuff, :information, :owner)
            """)
        db.session.execute(sql, {"stuff": session["root_id"],
                                 "information": result.scalar(),
                                 "owner": session["user_id"]})
        db.session.commit()
        return (True, "")
    except Exception as e:
        return (False, e)


# returns (True, int) or (False, str)
# as in (True, stuff_id) or (False, error message)
def new_stuff(name, description):
    try:
        sql = text("""
                INSERT INTO Stuffs (name, description, owner)
                VALUES (:name, :description, :owner)
                RETURNING id
            """)
        result = db.session.execute(sql, {"name": name,
                                          "description": description,
                                          "owner": session["user_id"]})
        id = result.scalar()
        db.session.commit()
        return (True, id)
    except Exception as e:
        return (False, e)


def new_information(stuff_id, information_id, description):
    # TODO: do this with SQL; probably check constraint with separate function
    test = text("""
        SELECT CAST(COUNT(*) AS BIT)
        FROM Stuffs S, Stuffs I
        WHERE S.id=:stuff_id
          AND I.id=:information_id
          AND S.owner=I.owner
          AND S.owner=:user_id
        """)
    result = db.session.execute(test,
                                {"stuff_id": stuff_id,
                                 "information_id": information_id,
                                 "user_id": session["user:id"]})
    if not result.scalar():
        return (False, "You are not the owner of that stuff!!")

    try:
        sql = text("""
                INSERT INTO Informations (stuff, information, owner)
                VALUES (:stuff, :information, :owner)
            """)
        db.session.execute(sql,
                           {"stuff": stuff_id,
                            "information": information_id,
                            "owner": session["user_id"]})
        db.session.commit()
        return (True, "")
    except Exception as e:
        return (False, e)
