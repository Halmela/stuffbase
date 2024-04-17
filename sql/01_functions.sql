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
