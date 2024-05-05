from db import db
from sqlalchemy.sql import text
from flask import session
from result import Ok, Err


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


def new_text_property(name, description):
    try:
        sql = text("""
                INSERT INTO Text_property_informations (name, description)
                VALUES (:name, :description)
            """)
        db.session.execute(sql, {"name": name,
                                 "description": description})
        db.session.commit()
        return Ok(id)
    except Exception as e:
        return Err(e)


def attach_text_property(stuff_id, property_id, prop_text):
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
        return Ok(())
    except Exception as e:
        return Err(e)


def new_numeric_property(name, description):
    try:
        sql = text("""
                INSERT INTO Numeric_property_informations(name, description)
                VALUES (:name, :description)
            """)
        db.session.execute(sql, {"name": name,
                                 "description": description})
        db.session.commit()
        return Ok(id)
    except Exception as e:
        return Err(e)


def attach_numeric_property(stuff_id, property_id, number):
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
        return Ok(())
    except Exception as e:
        return Err(e)


def get_text_properties():
    try:
        sql = text("""
                SELECT id, name
                FROM Text_property_informations
            """)
        result = db.session.execute(sql)
        return Ok(result.fetchall())
    except Exception as e:
        return Err(e)


def get_numeric_properties():
    try:
        sql = text("""
                SELECT id, name
                FROM Numeric_property_informations
            """)
        result = db.session.execute(sql)
        return Ok(result.fetchall())
    except Exception as e:
        return Err(e)


def text_property_exists(id):
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Text_property_informations
                WHERE id = COALESCE(:id,0)
            """)

        result = db.session.execute(sql, {"id": id})
        exists = bool(int(result.scalar()))
        if exists:
            print("prop exists")
            return Ok(id)
        else:
            return Err(f"Text propery T{id} does not exist ")
            print("prop does not exist")
    except Exception as e:
        print(f"prop exception {e}")
        return Err(e)


def numeric_property_exists(id):
    try:
        sql = text("""
                SELECT CAST(COUNT(*) AS BIT)
                FROM Numeric_property_informations
                WHERE id = COALESCE(:id,0)
            """)

        result = db.session.execute(sql, {"id": id})
        exists = bool(int(result.scalar()))
        if exists:
            return Ok(id)
        else:
            return Err(f"Numeric propery N{id} does not exist ")
    except Exception as e:
        return Err(e)
