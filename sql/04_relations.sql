INSERT INTO Relation_informations (description) VALUES ('→');
INSERT INTO Relation_informations (description) VALUES ('←');
SELECT create_converse_relations('⇄', '⇆'); 
SELECT create_converse_relations('is right of', 'is left of'); 
SELECT create_converse_relations('is above', 'is below'); 
SELECT create_converse_relations('authored', 'authored by'); 
SELECT create_converse_relations('contains', 'is inside'); 

