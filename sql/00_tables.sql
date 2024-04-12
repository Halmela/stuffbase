CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE Admins (
    id INTEGER REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Stuffs (
    id SERIAL PRIMARY KEY,
    owner INTEGER REFERENCES Users ON DELETE CASCADE,
    name TEXT,
    description TEXT
);

CREATE TABLE Informations (
    id SERIAL PRIMARY KEY,
    description TEXT,
    owner INTEGER REFERENCES Users ON DELETE CASCADE
);


CREATE TABLE InformationRelations (
    info_id INTEGER REFERENCES Informations ON DELETE CASCADE,
    stuff INTEGER REFERENCES Stuffs ON DELETE CASCADE,
    information INTEGER REFERENCES Stuffs ON DELETE CASCADE
);

CREATE TABLE Roots (
    owner INTEGER REFERENCES Users ON DELETE CASCADE,
    root INTEGER REFERENCES Stuffs ON DELETE CASCADE
);


CREATE TABLE Text_property_informations (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT
);

CREATE TABLE Text_properties (
    property_id INTEGER REFERENCES Text_property_informations,
    stuff_id INTEGER REFERENCES Stuffs,
    text TEXT
);

CREATE TABLE Numeric_property_informations (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT
);

CREATE TABLE Numeric_properties (
    property_id INTEGER REFERENCES Numeric_property_informations,
    stuff_id INTEGER REFERENCES Stuffs,
    number NUMERIC
);
