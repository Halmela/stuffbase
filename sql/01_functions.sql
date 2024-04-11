CREATE OR REPLACE FUNCTION check_information_ownership() RETURNS TRIGGER AS $$
DECLARE
    info_owner INTEGER;
    stuff1_owner INTEGER;
    stuff2_owner INTEGER;
BEGIN
    SELECT owner INTO info_owner FROM Informations WHERE id = NEW.info_id;
    SELECT owner INTO stuff1_owner FROM Stuffs WHERE id = NEW.stuff;
    SELECT owner INTO stuff2_owner FROM Stuffs WHERE id = NEW.information;

    IF NOT (stuff1_owner = stuff2_owner AND stuff1_owner = info_owner) THEN
        RAISE EXCEPTION 'Ownerships do not match.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
