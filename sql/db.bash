#!/bin/bash

DB=stuffbase

echo Initialize database

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
fi

for sql in ./*\.sql; do
  echo "$sql"
  psql -d $DB < "$sql"
done
