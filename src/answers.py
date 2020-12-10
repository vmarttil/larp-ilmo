from db import db

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