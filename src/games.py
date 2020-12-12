from db import db
import utils

def get_list():
    '''Return a list of all games in the database as a list of dictionaries.'''
    sql =  "SELECT \
                g.id, \
                g.name, \
                g.start_date, \
                g.end_date, \
                g.location, \
                g.price, \
                go.person_id AS organiser_id, \
                f.published, \
                COUNT(r.person_id) AS num_registrations \
            FROM Game AS g \
                JOIN GameOrganiser AS go \
                    ON g.id = go.game_id \
                LEFT JOIN Form AS f \
                    ON g.id = f.game_id \
                LEFT JOIN Registration as r \
                    ON g.id = r.game_id \
            GROUP BY g.id, g.name, g.start_date, g.end_date, g.location, g.price, go.person_id, f.published \
            ORDER BY start_date"
    result = db.session.execute(sql)
    game_list = utils.to_dict_list(result.fetchall())
    return game_list

def get_details(id):
    '''Return all the information about the given game as a dictionary.'''
    sql_game = "SELECT \
                    g.id, \
                    g.name, \
                    g.start_date, \
                    g.end_date, \
                    g.location, \
                    g.price, \
                    g.description, \
                    f.published \
                    FROM Game AS g\
                        LEFT JOIN Form AS f \
                            ON g.id = f.game_id \
                    WHERE g.id = :id"
    result_game = db.session.execute(sql_game, {"id":id})
    game = result_game.fetchone()
    organisers = get_organisers(id)
    game = dict(game.items())
    game['organisers'] = organisers
    return game

def get_organisers(game_id):
    '''Return the id, name components and email of the organisers for the given game as a list of dictionaries.'''
    sql_orgs =  "SELECT \
                    p.id, \
                    p.first_name, \
                    p.last_name, \
                    p.nickname, \
                    p.email \
                FROM Person AS p \
                    JOIN GameOrganiser AS go \
                        ON p.id = go.person_id \
                WHERE go.game_id = :id \
                ORDER BY p.last_name"
    result_orgs = db.session.execute(sql_orgs, {"id":game_id})
    organisers = utils.to_dict_list(result_orgs.fetchall())
    return organisers

def get_registrations(game_id):
    '''Return all registrations for the given game as a list of dictionaries.'''
    sql_regs =  "SELECT \
                    ROW_NUMBER() OVER (ORDER BY r.submitted ASC) AS number, \
                    r.id, \
                    a.answer_text AS name, \
                    r.submitted \
                FROM Registration AS r \
                    JOIN Answer AS a \
                        ON r.id = a.registration_id \
                    JOIN FormQuestion AS fq \
                        ON a.formquestion_id = fq.id \
                    JOIN Question AS q \
                        ON fq.question_id = q.id \
                WHERE r.game_id = :id \
                    AND q.prefill_tag = 'name'\
                ORDER BY r.submitted ASC"
    result_regs = db.session.execute(sql_regs, {"id":game_id})
    registrations = utils.to_dict_list(result_regs.fetchall())
    return registrations

def get_registration_game(registration_id):
    '''Return the id of the game the registration is linked to.'''
    sql =  "SELECT \
                game_id \
            FROM Registration \
            WHERE id = :registration_id"
    result = db.session.execute(sql, {"registration_id": registration_id})
    game_id = result.fetchone()[0]
    return game_id

def send(person_id, id, name, start_date, end_date, location, price, description):
    '''Insert the information for a game, either new or existing, into the database.'''
    if id is None:
        sql =  "INSERT INTO Game (\
                    name, \
                    start_date, \
                    end_date, \
                    location, \
                    price, \
                    description \
                ) \
                VALUES ( \
                    :name, \
                    :start_date, \
                    :end_date, \
                    :location, \
                    :price, \
                    :description \
                )"
        db.session.execute(sql, {"name":name, "start_date":start_date, "end_date":end_date, "location":location, "price":price, "description":description})
        sql = "SELECT CURRVAL(pg_get_serial_sequence('Game','id'))"
        result = db.session.execute(sql)
        game_id = result.fetchone()[0]
        sql =  "INSERT INTO GameOrganiser ( \
                    person_id, \
                    game_id \
                ) \
                VALUES ( \
                    :person_id, \
                    :game_id \
                );"
        db.session.execute(sql, {"person_id":person_id, "game_id":game_id})
    else: 
        sql =  "UPDATE Game SET \
                    name=:name, \
                    start_date=:start_date, \
                    end_date=:end_date, \
                    location=:location, \
                    price=:price, \
                    description=:description \
                WHERE id=:id"
        db.session.execute(sql, {"name":name, "start_date":start_date, "end_date":end_date, "location":location, "price":price, "description":description, "id":id})
    db.session.commit()
    return True
