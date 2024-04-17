from db import db
from sqlalchemy.sql import text
from flask import session


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


def get_relations(stuff_id):
    sql = text("""
            SELECT DISTINCT S.id, S.name, RI.description
            FROM Relation_informations RI, Stuffs S
                JOIN Relations R
                ON S.id = R.relatee
            WHERE R.relator = :stuff_id
                AND S.owner=:user_id
                AND R.info_id = RI.id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id,
                                      "user_id": session["user_id"]})
    return result.fetchall()


def get_reverse_relations(stuff_id):
    sql = text("""
            SELECT DISTINCT S.id, S.name, RI.description
            FROM Relation_informations RI, Stuffs S
                JOIN Relations R
                ON S.id = R.relator
            WHERE R.relatee = :stuff_id
                AND S.owner=:user_id
                AND R.info_id = RI.id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id,
                                      "user_id": session["user_id"]})
    return result.fetchall()


def get_stuff_text_properties(stuff_id):
    sql = text("""
            SELECT I.name, P.text
            FROM Text_property_informations I, Text_properties P
            WHERE P.stuff_id = :stuff_id AND P.property_id = I.id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id})

    return result.fetchall()


def get_stuff_numeric_properties(stuff_id):
    sql = text("""
            SELECT I.name, P.number
            FROM Numeric_property_informations I, Numeric_properties P
            WHERE P.stuff_id = :stuff_id AND P.property_id = I.id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id})

    return result.fetchall()


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
        return (True, "")
    except Exception as e:
        return (False, e)


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
        return (True, id)
    except Exception as e:
        return (False, e)


def new_relation(new_name, relation_description, stuff_id):
    relatee_id = new_stuff(new_name)
    if not relatee_id[0]:
        return relatee_id

    return attach_relation(stuff_id, relatee_id[1], relation_description)


def attach_relation(relator_id, relatee_id, description):
    try:
        sql = text("""
                INSERT INTO Relation_informations (description)
                VALUES (:description)
                RETURNING id
            """)
        result = db.session.execute(sql,
                                    {"description": description})
        info_id = result.scalar()

        sql = text("""
                INSERT INTO Relations (info_id, relator, relatee)
                VALUES (:info_id, :relator, :relatee)
            """)
        db.session.execute(sql,
                           {"info_id": info_id,
                            "relator": relator_id,
                            "relatee": relatee_id
                            })

        db.session.commit()
        return (True, info_id)
    except Exception as e:
        return (False, e)


def new_text_property(name, description):
    try:
        sql = text("""
                INSERT INTO Text_property_informations (name, description)
                VALUES (:name, :description)
            """)
        db.session.execute(sql, {"name": name,
                                 "description": description})
        db.session.commit()
        return (True, id)
    except Exception as e:
        return (False, e)


def attach_text_property(stuff_id, property_id, prop_text):
    owner = is_owner(session["user_id"], stuff_id)
    if not owner[0]:
        return owner

    try:
        print(stuff_id, property_id, text)
        sql = text("""
                INSERT INTO Text_properties
                VALUES (:stuff_id, :property_id, :text)
            """)
        print("text tehty")
        db.session.execute(sql,
                           {"stuff_id": stuff_id,
                            "property_id": property_id,
                            "text": prop_text})
        print("exec läpi")
        db.session.commit()
        return (True, "")
    except Exception as e:
        return (False, e)


def new_numeric_property(name, description):
    try:
        sql = text("""
                INSERT INTO Numeric_property_informations(name, description)
                VALUES (:name, :description)
            """)
        db.session.execute(sql, {"name": name,
                                 "description": description})
        db.session.commit()
        return (True, id)
    except Exception as e:
        return (False, e)


def attach_numeric_property(stuff_id, property_id, number):
    owner = is_owner(session["user_id"], stuff_id)
    if not owner[0]:
        return owner

    try:
        sql = text("""
                INSERT INTO Numeric_properties
                VALUES (:stuff_id, :property_id, :number)
            """)
        db.session.execute(sql,
                           {"stuff_id": stuff_id,
                            "property_id": property_id,
                            "number": number})
        db.session.commit()
        return (True, "")
    except Exception as e:
        return (False, e)


def get_text_properties():
    try:
        sql = text("""
                SELECT id, name
                FROM Text_property_informations
            """)
        result = db.session.execute(sql)
        return (True, result.fetchall())
    except Exception as e:
        return (False, e)


def get_numeric_properties():
    try:
        sql = text("""
                SELECT id, name
                FROM Numeric_property_informations
            """)
        result = db.session.execute(sql)
        return (True, result.fetchall())
    except Exception as e:
        return (False, e)


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
        return (owner, "" if owner else "You are not the owner of that stuff")
    except Exception as e:
        return(False, e)
