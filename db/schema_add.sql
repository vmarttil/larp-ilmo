CREATE TABLE Form (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES Game (id)
);

CREATE TABLE Question (
    id SERIAL PRIMARY KEY,
    field_type INTEGER REFERENCES FieldType (id),
    question_text TEXT NOT NULL,
    description TEXT,
    is_default BOOLEAN NOT NULL
);

CREATE TABLE FormQuestion (
    id SERIAL PRIMARY KEY,
    form_id INTEGER REFERENCES Form (id),
    question_id INTEGER REFERENCES Question (id)
);

CREATE TABLE Option (
    id SERIAL PRIMARY KEY,
    option_text TEXT NOT NULL
);

CREATE TABLE QuestionOption (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES Question (id),
    option_id INTEGER REFERENCES Option (id)
);

CREATE TABLE FieldType (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE Answer (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES Person (id),
    question_id INTEGER REFERENCES Question (id),
    questionoption_id INTEGER REFERENCES QuestionOption (id),
    answer_text TEXT
);


