CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);


CREATE TABLE Stuffs (
    id SERIAL PRIMARY KEY,
    owner INTEGER REFERENCES Users,
    name TEXT,
    description TEXT
);

CREATE TABLE Informations (
    id SERIAL PRIMARY KEY,
    stuff INTEGER REFERENCES Stuffs,
    information INTEGER REFERENCES Stuffs,
    description TEXT,
    owner INTEGER REFERENCES Users
);

CREATE TABLE Roots (
    root INTEGER REFERENCES Stuffs,
    owner INTEGER REFERENCES Users
);
