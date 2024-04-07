# StuffBase
Database for logging information on stuff. 

## CURRENT STATE
### How to run
Install postgresql (I use 14.11) with your preferred method and give your user permission to create databases.

```
./init.bash
./run.bash
```

### usage
create user and then add stuff to root.
you can give stuff a description.



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
