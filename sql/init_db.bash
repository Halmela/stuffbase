#!/bin/bash

DB=stuffbase

echo "Initialize database with name $DB"

if psql -l | grep -q $DB; then
  echo Old $DB found
  echo Recreate it? y/n
  read -r
  
  if [[ $REPLY = "y" ]]; then
    psql -d $DB -c "drop owned by $USER cascade;"
  else
    echo $DB left intact
    exit
  fi
else
  if ! createdb $DB; then
    echo -e "Could not create a database. This probably is because you don't have sufficient permissions. This might help:\n\nsudo -u postgres createdb -O $USER $DB\n"
    exit 1
  fi
fi

for sql in sql/*\.sql; do
  echo "$sql"
  psql -d $DB < "$sql"
done
