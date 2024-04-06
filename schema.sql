CREATE TABLE Stuffs (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE Informations (
    id SERIAL PRIMARY KEY,
    stuff INTEGER REFERENCES Stuffs,
    information INTEGER REFERENCES Stuffs,
    description TEXT
);

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
