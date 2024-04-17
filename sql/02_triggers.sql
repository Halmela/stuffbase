CREATE TRIGGER trigger_relation_ownership
BEFORE INSERT OR UPDATE ON Relations
FOR EACH ROW EXECUTE FUNCTION check_relation_ownership();
