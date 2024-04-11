CREATE TRIGGER trigger_information_ownership
BEFORE INSERT OR UPDATE ON InformationRelations
FOR EACH ROW EXECUTE FUNCTION check_information_ownership();
