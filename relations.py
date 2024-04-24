from db import db
from sqlalchemy.sql import text
from flask import session
from result import Ok, Err


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


def get_relation_informations():
    sql = text("""
            SELECT id, description
            FROM Relation_informations
            WHERE NOT (id = 1 OR id = 2)
        """)
    result = db.session.execute(sql)
    return result.fetchall()


def new_relation(description, converse_description):
    try:
        if converse_description:
            sql = text("""
                    SELECT create_converse_relations(:description,
                                                    :converse_description)
                """)
        else:
            sql = text("""
                    INSERT INTO Relation_informations (description)
                    VALUES (:description)
                """)

        db.session.execute(sql,
                           {"description": description,
                            "converse_description": converse_description
                            })
        db.session.commit()
        return Ok(())
    except Exception as e:
        return Err(e)


def attach_relation(info_id, relator_id, relatee_id):
    try:
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
        return Ok(info_id)
    except Exception as e:
        return Err(e)
