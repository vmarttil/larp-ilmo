CREATE TABLE Person (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    nickname TEXT,
    phone TEXT UNIQUE,
    birth_date DATE NOT NULL,
    profile TEXT, 
    password TEXT NOT NULL
);
CREATE TABLE Game (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    location TEXT,
    price INT,
    description TEXT 
);
CREATE TABLE GameOrganiser (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES Person (id),
    game_id INTEGER REFERENCES Game (id)
);

CREATE TABLE Form (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES Game (id),
    name TEXT,
    published BOOLEAN NOT NULL
);

CREATE TABLE FieldType (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    display TEXT NOT NULL
);

CREATE TABLE Question (
    id SERIAL PRIMARY KEY,
    field_type INTEGER REFERENCES FieldType (id),
    question_text TEXT NOT NULL,
    description TEXT,
    is_default BOOLEAN NOT NULL,
    is_optional BOOLEAN NOT NULL,
    prefill_tag TEXT
);

CREATE TABLE FormQuestion (
    id SERIAL PRIMARY KEY,
    form_id INTEGER REFERENCES Form (id),
    question_id INTEGER REFERENCES Question (id),
    position INTEGER NOT NULL
);

CREATE TABLE Option (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES Question (id),
    option_text TEXT NOT NULL
);

CREATE TABLE Registration (
    id SERIAL PRIMARY KEY,
    submitted TIMESTAMP,
    person_id INTEGER REFERENCES Person (id),
    game_id INTEGER REFERENCES Game (id)
);

CREATE TABLE Answer (
    id SERIAL PRIMARY KEY,
    registration_id INTEGER REFERENCES Registration (id),
    formquestion_id INTEGER REFERENCES FormQuestion (id),
    answer_text TEXT
);

CREATE TABLE AnswerOption (
    id SERIAL PRIMARY KEY,
    answer_id INTEGER REFERENCES Answer (id),
    option_id INTEGER REFERENCES Option (id)
);
