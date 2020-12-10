from db import db
import utils

def create_game_form(game_id):
    sql =  "INSERT INTO Form (game_id, name, published) \
                VALUES (:game_id, (SELECT CONCAT((SELECT name FROM Game WHERE id = :game_id), ': Ilmoittautuminen')), False) \
            RETURNING id, name, published;"
    result = db.session.execute(sql, {"game_id":game_id})
    db.session.commit()
    form = result.fetchone()
    return form

def insert_default_questions(form_id):
    sql =  "CREATE TEMPORARY SEQUENCE serial START 1; \
            INSERT INTO FormQuestion (form_id, question_id, position) \
            SELECT :form_id AS form_id, q.id AS question_id, nextval('serial') AS position \
            FROM Question AS q \
            WHERE is_default = True \
            ORDER BY q.id;"
    db.session.execute(sql, {"form_id":form_id})
    db.session.commit()

def get_game_form(game_id):
    sql = "SELECT id, name, published FROM Form WHERE game_id = :game_id;"
    result = db.session.execute(sql, {"game_id":game_id})
    try:
        result = dict(result.fetchone())
    except Exception as ex:
        result = None
    return result

def get_form_by_id(form_id):
    sql = "SELECT id, name, published FROM Form WHERE id = :form_id;"
    result = db.session.execute(sql, {"form_id":form_id})
    try:
        result = dict(result.fetchone())
    except Exception as ex:
        result = None
    return result

def get_form_questions(form_id):
    sql =  "SELECT \
                fq.id, \
                ft.name AS field_type, \
                q.question_text AS text, \
                q.description, \
                fq.position, \
                q.is_default, \
                q.is_optional, \
                q.prefill_tag \
            FROM Question AS q \
                JOIN FieldType AS ft \
                    ON q.field_type = ft.id \
                JOIN FormQuestion AS fq \
                    ON q.id = fq.question_id \
            WHERE fq.form_id = :form_id \
            ORDER BY fq.position;"
    result = db.session.execute(sql, {"form_id":form_id})
    form_questions = utils.to_dict_list(result.fetchall())
    return form_questions

def publish_form(form_id):
    sql = "UPDATE Form SET published = true WHERE id = :form_id;"
    db.session.execute(sql, {"form_id":form_id})
    db.session.commit()

def unpublish_form(form_id):
    sql = "UPDATE Form SET published = false WHERE id = :form_id;"
    db.session.execute(sql, {"form_id":form_id})
    db.session.commit()

def is_published(game_id):
    sql =  "SELECT (CASE \
                    WHEN published = true THEN True \
                    ELSE False \
                END) \
            FROM Form \
            WHERE game_id = :game_id;"
    result = db.session.execute(sql, {"game_id":game_id})
    try:
        result = result.fetchone()[0]
    except Exception as ex:
        result = None
    return result

def get_last_position(form_id):
    sql_pos = "SELECT MAX(position) FROM FormQuestion WHERE form_id = :form_id"
    result = db.session.execute(sql_pos, {"form_id": form_id})
    return result.fetchone()[0] + 1
    
def get_field_types():
    sql =  "SELECT \
                id, \
                display \
            FROM FieldType \
            ORDER BY display"
    result = db.session.execute(sql)
    field_types = utils.to_dict_list(result.fetchall())
    return field_types

def get_field_type_name(id):
    sql =  "SELECT \
                display \
            FROM FieldType \
            WHERE id = :id"
    result = db.session.execute(sql, {"id": id})
    field_type_name = result.fetchone()[0]
    return field_type_name