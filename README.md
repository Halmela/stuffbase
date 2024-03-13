# StuffBase
Database for logging information on stuff. 

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
Where everything is located, what I have lent to whom, what have I done.
I want to be able to flexibly find and relocate my possenssions.
Types would be a good fit too, because I do not want to constantly re-invent what a book is and I want to view every book I own.

## Execution
In my mind I have sketched that there will be tables
- Stuff (id ; name ; description)
- Information (stuff.id ; stuff.id)
- Type (id ; name ; description ; template.id)
- Template (id)
- Measurement (id ; name ; value)
- Time (id ; name ; time)
- User (id ; stuff.id)
