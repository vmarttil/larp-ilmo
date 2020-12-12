from db import db
import utils

def get_question(formquestion_id):
    '''Get all the information for the given form instance of a question as a dictionary.'''
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
    '''Get the id of the base question based on the id of its particular form instance.'''
    sql = "SELECT question_id FROM FormQuestion WHERE id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id}) 
    return result.fetchone()[0]

def get_question_text(formquestion_id):
    '''Get the question text of a question based on the id of its particular form instance.'''
    sql =  "SELECT question_text \
            FROM Question AS q \
                JOIN FormQuestion AS fq \
                    ON q.id = fq.question_id \
            WHERE fq.id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id}) 
    return result.fetchone()[0]

def get_question_options(formquestion_id):
    '''Get the options of a particular question as a list of dictionaries, based on form instance id.'''
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
    question_options = utils.to_dict_list(result.fetchall())
    return question_options

def move_question_up(form_id, current_pos):
    '''Move the question at the given position in the selected form upwards one position.'''
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
    '''Move the question at the given position in the selected form downwards one position.'''
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
    '''Remove the selected question form instance from the form.
    
    The questions following the deleted question are moved upwards one step. If the question is 
    neither a default question nor used anywhere else, it is also deleted from the database.'''
    default = is_default(formquestion_id)
    question_id = get_question_id(formquestion_id)
    form_position = remove_question(formquestion_id)
    sql_move = "UPDATE FormQuestion SET position = position - 1 WHERE form_id = :form_id AND position > :position;"
    db.session.execute(sql_move, {"form_id": form_position[0], "position": form_position[1]})
    if default == False and count_forms_for_question(question_id) == 0:
        delete_options(question_id)
        sql_delete = "DELETE FROM Question WHERE id = :question_id;"
        db.session.execute(sql_delete, {"question_id": question_id})
    db.session.commit()
    return True

def delete_options(question_id):
    '''Delete all the options of the selected question from the database.'''
    sql = "DELETE FROM Option WHERE question_id = :question_id;"
    db.session.execute(sql, {"question_id": question_id})
    return True

def remove_question(formquestion_id):
    '''Delete the question from the database and return its previous '''
    sql = "DELETE FROM FormQuestion WHERE id = :formquestion_id RETURNING form_id, position;"
    result = db.session.execute(sql, {"formquestion_id": formquestion_id})
    form_position = result.fetchone()
    db.session.commit()
    return form_position

def add_new_question(form_id, field_type, question_text, description, options, position):
    '''Add a new question to the database and insert it to the current form.'''
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

def update_question(formquestion_id, question_text, description, options):
    '''Update the text, description and options of a question based on its form instance id.
    
    If the question is a default one or used also in some other form, a new question is created 
    with the edits and substituted for the original in the form, leaving the original unchanged.'''
    question_id = get_question_id(formquestion_id)
    if is_default(formquestion_id) or count_forms_for_question(question_id) > 1:
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
        update_options(question_id, options)
    db.session.commit()
    return True

def is_default(formquestion_id):
    '''Check whether the question is a default question.'''
    sql =  "SELECT \
                is_default \
            FROM Question AS q \
                JOIN FormQuestion AS fq \
                    ON q.id = fq.question_id \
            WHERE fq.id = :formquestion_id;"
    result = db.session.execute(sql, {"formquestion_id":formquestion_id})
    return result.fetchone()[0]

def count_forms_for_question(question_id):
    '''Count the number of forms in which the given question is used.'''
    sql = "SELECT COUNT(DISTINCT form_id) FROM FormQuestion WHERE question_id = :question_id;"
    result = db.session.execute(sql, {"question_id":question_id})
    return result.fetchone()[0]

def update_options(question_id, options):
    '''Update the options of the given question to correspond to the provided list.'''
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
    '''Get the the options (id and text) for the given question.'''
    sql = "SELECT \
            id, \
            option_text \
            FROM Option \
            WHERE question_id = :question_id;"
    result = db.session.execute(sql, {"question_id":question_id}) 
    return utils.to_dict_list(result.fetchall())

def add_new_options(question_id, options):
    '''Add a list of new options to the given question.'''
    sql_option =   "INSERT INTO Option ( \
                        question_id, \
                        option_text \
                        ) VALUES ( \
                        :question_id, \
                        :option_text \
                        );"
    for option in options:
        db.session.execute(sql_option, {"question_id": question_id, "option_text":option})
    return True

def delete_option(id):
    '''Delete the given option from the database based on its id.'''
    sql = "DELETE FROM Option WHERE id = :id;"
    db.session.execute(sql, {"id": id})
    return True