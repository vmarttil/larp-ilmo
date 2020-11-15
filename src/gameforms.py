from db import db
import games
import users

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

def get_default_questions():
    sql =  "SELECT \
                q.id, \
                ft.name, \
                q.question_text AS text, \
                q.description \
            FROM Question AS q \
                JOIN FieldType AS ft \
                    ON q.field_type = ft.id \
            WHERE q.is_default = True;"
    result = db.session.execute(sql)
    default_questions = to_dict_list(result.fetchall())
    return default_questions

def get_form_questions(form_id):
    sql =  "SELECT \
                fq.id, \
                ft.name AS field_type, \
                q.question_text AS text, \
                q.description, \
                fq.position \
            FROM Question AS q \
                JOIN FieldType AS ft \
                    ON q.field_type = ft.id \
                JOIN FormQuestion AS fq \
                    ON q.id = fq.question_id \
            WHERE fq.form_id = :form_id \
            ORDER BY fq.position;"
    result = db.session.execute(sql, {"form_id":form_id})
    option_list = result.fetchall()
    form_questions = to_dict_list(option_list)
    return form_questions

def get_question_options(question_id):
    sql =  "SELECT \
                o.id, \
                o.option_text AS text \
            FROM Option as o \
                JOIN QuestionOption AS qo \
                    ON o.id = qo.option_id \
            WHERE qo.question_id = 7;"
    result = db.session.execute(sql, {"question_id":question_id})
    option_list = result.fetchall()
    print("Optiolistan pituus funktiossa: " + str(len(option_list)))
    question_options = to_dict_list(option_list)
    print("Optiodictlistan pituus funktiossa: " + str(len(question_options)))
    return question_options

def publish_form(form_id):
    sql = "UPDATE Form SET published = true WHERE id = :form_id;"
    db.session.execute(sql, {"form_id":form_id})
    db.session.commit()

def cancel_form(form_id):
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

def save_answers(answer_list):
    sql_text = "INSERT INTO Answer ( \
                    person_id, \
                    formquestion_id, \
                    answer_text \
                    ) VALUES ( \
                        :person_id, \
                        :formquestion_id, \
                        :answer_text \
                        );"
    sql_answer = "INSERT INTO Answer ( \
                    person_id, \
                    formquestion_id \
                    ) VALUES ( \
                        :person_id, \
                        :formquestion_id \
                        ) RETURNING id;"
    sql_option = "INSERT INTO AnswerOption ( \
                    answer_id, \
                    questionoption_id \
                    ) VALUES ( \
                        :answer_id, \
                        :questionoption_id \
                        );"        
    for answer in answer_list:
        if "answer_text" in answer:
            db.session.execute(sql_text, {"person_id":answer['person_id'], "formquestion_id":answer['formquestion_id'], "answer_text":answer['answer_text']})
        else:
            answer_id = db.session.execute(sql_answer, {"person_id":answer['person_id'], "formquestion_id":answer['formquestion_id']}).fetchone()[0]
            db.session.execute(sql_option, {"answer_id":answer_id, "questionoption_id":answer['questionoption_id']})
    db.session.commit()
    return True

def to_dict_list(result):
    itemlist = []
    for item in result:
        itemlist.append(dict(item))
    return itemlist