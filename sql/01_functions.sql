CREATE OR REPLACE FUNCTION check_relation_ownership() RETURNS TRIGGER AS $$
DECLARE
    relation_owner INTEGER;
    relator_owner INTEGER;
    relatee_owner INTEGER;
BEGIN
    SELECT owner INTO relator_owner FROM Stuffs WHERE id = NEW.relator;
    SELECT owner INTO relatee_owner FROM Stuffs WHERE id = NEW.relatee;

    IF NOT (relator_owner = relatee_owner AND relator_owner = NEW.owner) THEN
        RAISE EXCEPTION 'Ownerships do not match.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION attach_to_converse_relation()
RETURNS TRIGGER AS $$
DECLARE
    converse_exists BOOLEAN;
    converse_possible BOOLEAN;
    converse_id INTEGER;
BEGIN
    SELECT EXISTS(
        SELECT 1 FROM Relations
        WHERE info_id = NEW.info_id AND relator = NEW.relator AND relatee = NEW.relatee
            AND NEW.converse_created = true
    ) INTO converse_exists;

    IF converse_exists THEN
        RETURN NULL;
    END IF;
  
    SELECT EXISTS(
        SELECT 1 FROM Converse_relations
        WHERE x_id = NEW.info_id OR y_id = NEW.info_id
    ) INTO converse_possible;

    IF converse_possible THEN
        SELECT y_id INTO converse_id FROM Converse_relations WHERE x_id = NEW.info_id;
        IF converse_id IS NULL THEN
            SELECT x_id INTO converse_id FROM Converse_relations WHERE y_id = NEW.info_id;
        END IF;
        INSERT INTO Relations (info_id, relator, relatee, converse_created)
        VALUES (converse_id, NEW.relatee, NEW.relator, true);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_converse_relations(
    x_description TEXT,
    y_description TEXT
)
RETURNS void AS $$
DECLARE
    x_id INTEGER;
    y_id INTEGER;
BEGIN
    INSERT INTO Relation_informations (description) VALUES (x_description)
    RETURNING id INTO x_id;

    INSERT INTO Relation_informations (description) VALUES (y_description)
    RETURNING id INTO y_id;

    INSERT INTO Converse_relations (x_id, y_id) VALUES (x_id, y_id);
END;
$$ LANGUAGE plpgsql;

