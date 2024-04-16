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
            FROM Informations I, Stuffs S
                JOIN InformationRelations IR
                ON S.id = IR.information
            WHERE IR.stuff = :stuff_id
                AND S.owner=:user_id
                AND I.id = IR.info_id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id,
                                      "user_id": session["user_id"]})
    return result.fetchall()


def get_reverse_information(stuff_id):
    sql = text("""
            SELECT DISTINCT S.id, S.name, S.description, I.description
            FROM Informations I, Stuffs S
                JOIN InformationRelations IR
                ON S.id = IR.stuff
            WHERE IR.information = :stuff_id
                AND S.owner=:user_id
                AND I.id = IR.info_id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id,
                                      "user_id": session["user_id"]})
    return result.fetchall()


def get_stuff_text_properties(stuff_id):
    sql = text("""
            SELECT I.name, P.text
            FROM Text_property_informations I, Text_properties P
            WHERE P.stuff_id = stuff_id AND P.property_id = I.id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id})

    return result.fetchall()


def get_stuff_numeric_properties(stuff_id):
    sql = text("""
            SELECT I.name, P.number
            FROM Numeric_property_informations I, Numeric_properties P
            WHERE P.stuff_id = stuff_id AND P.property_id = I.id
        """)
    result = db.session.execute(sql, {"stuff_id": stuff_id})

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


def new_information(new_name, new_description, info_description, stuff_id):
    info_id = new_stuff(new_name, new_description)
    if not info_id[0]:
        return info_id

    return attach_information(stuff_id, info_id[1], info_description)


def attach_information(stuff_id, information_id, description):
    try:
        sql = text("""
                INSERT INTO Informations (description, owner)
                VALUES (:description, :owner)
                RETURNING id
            """)
        result = db.session.execute(sql,
                                    {"description": description,
                                     "owner": session["user_id"]})
        info_id = result.scalar()

        sql = text("""
                INSERT INTO InformationRelations (info_id, stuff, information)
                VALUES (:info_id, :stuff, :information)
            """)
        db.session.execute(sql,
                           {"info_id": info_id,
                            "stuff": stuff_id,
                            "information": information_id
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
