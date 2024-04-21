# StuffBase
Database for logging information on stuff. 

## CURRENT STATE
### installation
Install postgresql (I use 14.11) with your preferred method and give your user permission to create databases.
If your user doesn't have permissions to create a database, do so with command

```
sudo -u postgres createdb -O [user] stuffbase
```

`sql/init_db.bash` will ask if you want to recreate database. Answer y to that.


#### Automated
```
./init.bash
```

#### Manual
Check how `init.bash` and `sql/init_db.bash` works.
`init.bash` will create a virtual environment, install dependencies, run `sql/init_db.bash` and create a environment file.
`sql/init_db.bash` will run every sql-command found in sql-directory.
You can achieve this manually with command `psql -d stuffbase < [sql-file]`
 
Running 03_properties.sql and 04_relations.sql are optional, but these will define few standard properties and relations.


### usage
```
# Activate virtual environment
source venv/bin/activate
# start server
flask run
```

`./run.bash` will do the same



You can add stuff to root and give them names.
If you want to add properties, you can do so in stuff's page.
There you can also add new relations to it.
If you want to add a relation between two existing stuffs, you can use the other stuff's #id instead of a new name.
If for a relation xRy exists a converse relation, a relation yCx will also be created.

#### admin

First user that goes to /admin page becomes an admin.
Admins can create describe new properties and relations.



## INITIAL THOUGHTS
## Definitions

### Stuff
Stuff is anything.
It can be material, such as books, clothes, shelves, people and text.
It can be immaterial, such as memories, concepts, types and time.
Pretty much anything that can be given a name.

### Information
Information is stuff related to stuff.
It can be a permanent or temporary owner of stuff.
It can be a descriptive text of stuff.
It can be a current or ideal location of stuff.
It can be the size of stuff.

## Motivation
I want to be able to organize my stuff.
Where everything is located, what I have lent to whom, what have I done, when stuff has changed.
I want to be able to flexibly find and relocate my possessions.
Types would be a good fit too, because I do not want to constantly re-invent what a book is and I want to view every book I own.

## Execution
In my mind I have sketched that there will be tables
- Stuff (id ; name ; description)
- Information (stuff.id ; stuff.id)
- Type (id ; name ; description ; stuff.id (some stuff with default values))
- Measurement (id ; name ; value)
- Measurement relation(?) (stuff.id ; measurement.id)
- Time (id ; name ; time)
- Time relation(?) (stuff.id ; time.id)
- User (id ; stuff.id)
