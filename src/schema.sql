CREATE TABLE Person (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT,
    gender INTEGER,
    birth_year INTEGER,
    profile TEXT, 
    password TEXT
);
CREATE TABLE Game (
    id SERIAL PRIMARY KEY,
    name TEXT,
    start_date DATE,
    end_date DATE,
    location TEXT,
    description TEXT 
);
CREATE TABLE GameOrganiser (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Person (id),
    game_id INTEGER REFERENCES Game (id)
);
