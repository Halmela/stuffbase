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
    name TEXT
);

CREATE TABLE Relation_informations (
    id SERIAL PRIMARY KEY,
    description TEXT UNIQUE
);


CREATE TABLE Relations (
    info_id INTEGER REFERENCES Relation_informations ON DELETE CASCADE,
    relator INTEGER REFERENCES Stuffs ON DELETE CASCADE,
    relatee INTEGER REFERENCES Stuffs ON DELETE CASCADE,
    owner INTEGER REFERENCES Users ON DELETE CASCADE,
    converse_created BOOLEAN DEFAULT FALSE,
    UNIQUE (info_id, relator, relatee, owner)
);

CREATE TABLE Converse_relations (
    x_id INTEGER REFERENCES Relation_informations ON DELETE CASCADE,
    y_id INTEGER REFERENCES Relation_informations ON DELETE CASCADE
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
    stuff_id INTEGER REFERENCES Stuffs,
    property_id INTEGER REFERENCES Text_property_informations,
    text TEXT
);

CREATE TABLE Numeric_property_informations (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT
);

CREATE TABLE Numeric_properties (
    stuff_id INTEGER REFERENCES Stuffs,
    property_id INTEGER REFERENCES Numeric_property_informations,
    number NUMERIC
);
