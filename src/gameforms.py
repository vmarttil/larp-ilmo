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

# def get_default_questions():
#     sql =  "SELECT \
#                 q.id, \
#                 ft.name AS field_type, \
#                 q.question_text AS text, \
#                 q.description, \
#                 q.is_default, \
#                 q.is_optional, \
#                 q.prefill_tag \
#             FROM Question AS q \
#                 JOIN FieldType AS ft \
#                     ON q.field_type = ft.id \
#             WHERE q.is_default = True;"
#     result = db.session.execute(sql)
#     default_questions = to_dict_list(result.fetchall())
#     return default_questions

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

def get_question(formquestion_id):
    sql =  "SELECT \
                fq.id, \
                fq.form_id, \
                q.field_type, \
                q.question_text AS text, \
                q.description, \
                q.is_default, \
                fq.position \
            FROM formquestion as fq \
                JOIN Question AS q \
                    ON fq.question_id = q.id \
            WHERE fq.id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id}) 
    question = dict(result.fetchone())
    question['options'] = get_question_options(formquestion_id)
    return question

def get_question_id(formquestion_id):
    sql = "SELECT question_id FROM FormQuestion WHERE id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id}) 
    return result.fetchone()[0]

def get_question_text(formquestion_id):
    sql =  "SELECT question_text \
            FROM Question AS q \
                JOIN FormQuestion AS fq \
                    ON q.id = fq.question_id \
            WHERE fq.id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id}) 
    return result.fetchone()[0]

def get_question_options(formquestion_id):
    sql =  "SELECT \
                o.id, \
                o.option_text AS text \
            FROM Option as o \
                JOIN Question AS q \
                    ON o.question_id = q.id \
                JOIN FormQuestion AS fq \
                    ON q.id = fq.question_id \
            WHERE fq.id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id}) 
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

def is_default(formquestion_id):
    sql =  "SELECT \
                is_default \
            FROM Question AS q \
                JOIN FormQuestion AS fq \
                    ON q.id = fq.question_id \
            WHERE fq.id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id})
    return result.fetchone()[0]

def is_used(question_id):
    sql =  "SELECT \
                COUNT(1) \
            FROM FormQuestion \
            WHERE question_id = :question_id;"
    result = db.session.execute(sql, {"question_id":question_id})
    if result.fetchone()[0] == 0:
        return False
    else:
        return True

def count_forms_for_question(formquestion_id):
    sql = "SELECT COUNT(DISTINCT form_id) FROM FormQuestion WHERE id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id})
    return result.fetchone()[0]

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

def delete_question(formquestion_id):
    default = is_default(formquestion_id)
    question_id = get_question_id(formquestion_id)
    form_position = remove_question(formquestion_id)
    sql_move = "UPDATE FormQuestion SET position = position - 1 WHERE form_id = :form_id AND position > :position;"
    db.session.execute(sql_move, {"form_id": form_position[0], "position": form_position[1]})
    if default == False and is_used(question_id) == False:
        delete_options(question_id)
        sql_delete = "DELETE FROM Question WHERE id = :question_id;"
        db.session.execute(sql_delete, {"question_id": question_id})
    db.session.commit()
    return True

def delete_options(question_id):
    sql = "DELETE FROM Option WHERE question_id = :question_id;"
    db.session.execute(sql, {"question_id": question_id})
    return True

def remove_question(formquestion_id):
    sql = "DELETE FROM FormQuestion WHERE id = :formquestion_id RETURNING form_id, position;"
    result = db.session.execute(sql, {"formquestion_id": formquestion_id})
    form_position = result.fetchone()
    db.session.commit()
    return form_position

def get_last_position(form_id):
    sql_pos = "SELECT MAX(position) FROM FormQuestion WHERE form_id = :form_id"
    result = db.session.execute(sql_pos, {"form_id": form_id})
    return result.fetchone()[0] + 1
    
def add_new_question(form_id, field_type, question_text, description, options, position):
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
                VALUES (:form_id, :question_id, :position);"
    db.session.execute(sql_fq, {"form_id": form_id, "question_id":question_id, "position":position})
    add_new_options(question_id, options)
    db.session.commit()
    return True

def add_new_options(question_id, options):
    sql_option =   "INSERT INTO Option ( \
                        question_id, \
                        option_text \
                        ) VALUES ( \
                        :question_id, \
                        :option_text \
                        );"
    for option in options:
        db.session.execute(sql_option, {"question_id": question_id, "option_text":option})
    db.session.commit()
    return True    

def update_question(formquestion_id, question_text, description, options):
    if is_default(formquestion_id) or count_forms_for_question(formquestion_id) > 1:
        old_question = get_question(formquestion_id)
        add_new_question(old_question['form_id'], old_question['field_type'], question_text, description, options, old_question['position'])
        remove_question(formquestion_id)
    else:
        question_id = get_question_id(formquestion_id)
        sql_question = "UPDATE Question SET \
                            question_text = :question_text, \
                            description = :description \
                        WHERE id = :question_id;"
        db.session.execute(sql_question, {"question_id": question_id, "question_text": question_text, "description": description})
        db.session.commit()
        update_options(question_id, options)
    return True

def update_options(question_id, options):
    new_options = options
    old_options = get_options(question_id)
    for option in old_options:
        if option['option_text'] in new_options:
            new_options.remove(option['option_text'])
        else:
            delete_option(option['id'])
    add_new_options(question_id, new_options)
    return True

def get_options(question_id):
    sql = "SELECT \
            id, \
            option_text \
            FROM Option \
            WHERE question_id = :question_id;"
    result = db.session.execute(sql, {"question_id":question_id}) 
    return to_dict_list(result.fetchall())

def delete_option(id):
    sql = "DELETE FROM Option WHERE id = :id;"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    return True

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
                    option_id \
                    ) VALUES ( \
                        :answer_id, \
                        :option_id \
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
            db.session.execute(sql_option, {"answer_id":answer_id, "option_id":answer['option_id']})
    db.session.commit()
    return True

def get_question_answer(registration_id, formquestion_id):
    sql =  "SELECT \
                a.answer_text AS text, \
                ARRAY( \
                    SELECT option_id \
                    FROM AnswerOption AS ao \
                    WHERE ao.answer_id = a.id \
                    ) AS options \
            FROM Answer as a \
                JOIN FormQuestion AS fq \
                    ON a.formquestion_id = fq.id \
            WHERE a.registration_id = :registration_id \
                AND fq.id = :formquestion_id;"
    result = db.session.execute(sql, {"registration_id": registration_id, "formquestion_id": formquestion_id})
    result = result.fetchone()
    if result[0] == None:
        answer = list(result[1])
    else:
        answer = result[0]
    return answer

def get_field_types():
    # Since the selector fields are not yet implemented, they are excluded for now
    sql =  "SELECT \
                id, \
                display \
            FROM FieldType \
            WHERE name != 'SelectField' \
                AND name != 'SelectMultipleField' \
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

def get_param_string(list):
    string = "(%s"
    for count in range(0,len(list)-1):
        string += ",%s"
    string += ")"
    return string