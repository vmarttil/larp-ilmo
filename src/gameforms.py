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
                ft.name AS field_type, \
                q.question_text AS text, \
                q.description, \
                q.is_default, \
                q.is_optional, \
                q.prefill_tag \
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
    form_questions = to_dict_list(result.fetchall())
    return form_questions

def get_question_options(question_id):
    sql =  "SELECT \
                qo.id, \
                o.option_text AS text \
            FROM Option as o \
                JOIN QuestionOption AS qo \
                    ON o.id = qo.option_id \
            WHERE qo.question_id = :question_id;"
    result = db.session.execute(sql, {"question_id":question_id}) 
    question_options = to_dict_list(result.fetchall())
    return question_options

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

def move_question_up(form_id, current_pos):
    sql_1 = "UPDATE FormQuestion \
                SET position = :current_pos - 1 \
             WHERE position = :current_pos \
                AND form_id = :form_id \
             RETURNING id"
    result = db.session.execute(sql_1, {"form_id": form_id, "current_pos": current_pos})
    moved_id = result.fetchone()[0]
    sql_2 = "UPDATE FormQuestion \
                 SET position = (:current_pos) \
             WHERE position = :current_pos - 1 \
                AND form_id = :form_id \
                AND id != :moved_id"
    db.session.execute(sql_2, {"form_id": form_id, "current_pos": current_pos, "moved_id": moved_id})
    db.session.commit()
    return True

def move_question_down(form_id, current_pos):
    sql_1 = "UPDATE FormQuestion \
                SET position = :current_pos + 1 \
             WHERE position = :current_pos \
                AND form_id = :form_id \
             RETURNING id"
    result = db.session.execute(sql_1, {"form_id": form_id, "current_pos": current_pos})
    moved_id = result.fetchone()[0]
    sql_2 = "UPDATE FormQuestion \
                 SET position = (:current_pos) \
             WHERE position = :current_pos + 1 \
                AND form_id = :form_id \
                AND id != :moved_id"
    db.session.execute(sql_2, {"form_id": form_id, "current_pos": current_pos, "moved_id": moved_id})
    db.session.commit()
    return True

def add_new_question(form_id, field_type, question_text, description):
    sql_pos = "SELECT MAX(position) FROM FormQuestion WHERE form_id = :form_id"
    result = db.session.execute(sql_pos, {"form_id": form_id})
    position = result.fetchone()[0] + 1
    sql_question = "INSERT INTO Question ( \
                        field_type, \
                        question_text, \
                        description, \
                        is_default, \
                        is_optional \
                        ) VALUES ( \
                        :field_type, \
                        :question_text, \
                        :description, \
                        false, \
                        true \
                        ) \
                    RETURNING id"
    result = db.session.execute(sql_question, {"field_type": field_type, "question_text":question_text, "description":description})
    question_id = result.fetchone()[0]
    sql_fq = "INSERT INTO FormQuestion (form_id, question_id, position) \
                VALUES (:form_id, :question_id, :position)"
    db.session.execute(sql_fq, {"form_id": form_id, "question_id":question_id, "position":position})
    db.session.commit()
    return True

# def add_new_option(option_text):
#     sql = "INSERT INTO Option (option_text) VALUES (:option_text) RETURNING id"
#     result = db.session.execute(sql, {"option_text": option_text})
#     option_id = result.fetchone()[0]
#     db.session.commit()
#     return option_id

# def get_option_texts(id_string):
#     print(id_string)
#     ids = id_string.split(",")
#     ids = tuple(map(int, ids))
#     # param_string = get_param_string(ids)
#     sql = "SELECT option_text FROM Option WHERE id IN :ids"
#     # sql += param_string
#     result = db.session.execute(sql, {"ids": ids})
#     optiontexts = extract_from_tuples(result.fetchall())
#     print(optiontexts)
#     return optiontexts

def save_answers(person_id, game_id, answer_list):
    sql_registration = "INSERT INTO Registration (person_id, game_id, submitted) \
                            VALUES (:person_id, :game_id, NOW()) \
                        RETURNING id;"
    result = db.session.execute(sql_registration, {"person_id": person_id, "game_id":game_id})
    registration_id = result.fetchone()[0]
    sql_text = "INSERT INTO Answer ( \
                    registration_id, \
                    formquestion_id, \
                    answer_text \
                    ) VALUES ( \
                        :registration_id, \
                        :formquestion_id, \
                        :answer_text \
                        );"
    sql_answer = "INSERT INTO Answer ( \
                    registration_id, \
                    formquestion_id \
                    ) VALUES ( \
                        :registration_id, \
                        :formquestion_id \
                        ) RETURNING id;"
    sql_option = "INSERT INTO AnswerOption ( \
                    answer_id, \
                    questionoption_id \
                    ) VALUES ( \
                        :answer_id, \
                        :questionoption_id \
                        );"
    last_question = 0
    answer_id = 0
    for answer in answer_list:
        if "answer_text" in answer:
            db.session.execute(sql_text, {"registration_id":registration_id, "formquestion_id":answer['formquestion_id'], "answer_text":answer['answer_text']})
        else:
            if last_question != answer['formquestion_id']:
                answer_id = db.session.execute(sql_answer, {"registration_id":registration_id, "formquestion_id":answer['formquestion_id']}).fetchone()[0]
                last_question = answer['formquestion_id']
            db.session.execute(sql_option, {"answer_id":answer_id, "questionoption_id":answer['questionoption_id']})
    db.session.commit()
    return True

def get_question_answer(registration_id, question_id, form_id):
    sql =  "SELECT \
                a.answer_text AS text, \
                ARRAY( \
                    SELECT questionoption_id \
                    FROM AnswerOption AS ao \
                    WHERE ao.answer_id = a.id \
                    ) AS options \
            FROM Answer as a \
                JOIN FormQuestion AS fq \
                    ON a.formquestion_id = fq.id \
            WHERE a.registration_id = :registration_id \
                AND fq.form_id = :form_id \
                AND fq.question_id = :question_id;"
    result = db.session.execute(sql, {"registration_id": registration_id, "question_id": question_id, "form_id": form_id})
    result = result.fetchone()
    if result[0] == None:
        answer = list(result[1])
    else:
        answer = result[0]
    print(answer)
    return answer

def get_field_types():
    # Since the selector fields are not yet implemented, they are excluded for now, as are the fields with options
    sql =  "SELECT \
                id, \
                display \
            FROM FieldType \
            WHERE name != 'SelectField' \
                AND name != 'SelectMultipleField' \
                AND name != 'RadioField' \
                AND name != 'CheckBoxListField' \
            ORDER BY display"
    result = db.session.execute(sql)
    field_types = to_dict_list(result.fetchall())
    return field_types

def get_field_type_name(id):
    sql =  "SELECT \
                display \
            FROM FieldType \
            WHERE id = :id"
    result = db.session.execute(sql, {"id": id})
    field_type_name = result.fetchone()[0]
    return field_type_name

def to_dict_list(result):
    itemlist = []
    for item in result:
        itemlist.append(dict(item))
    return itemlist

def extract_from_tuples(result):
    itemlist = []
    for item in result:
        itemlist.append(item[0])
    return itemlist

def get_param_string(list):
    string = "(%s"
    for count in range(0,len(list)-1):
        string += ",%s"
    string += ")"
    return string