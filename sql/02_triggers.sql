CREATE TRIGGER trigger_relation_ownership
BEFORE INSERT OR UPDATE ON Relations
FOR EACH ROW EXECUTE FUNCTION check_relation_ownership();


CREATE TRIGGER trigger_converse_creation
AFTER INSERT ON Relations
FOR EACH ROW
EXECUTE FUNCTION attach_to_converse_relation();
