#!/bin/bash

echo -e "StuffBase initialization skript\n"

echo "You should have postgresql installed and your current user should have rights to use it"
echo "Continue y/n?"
read -r 
if [[ $REPLY = "y" ]]; then
  echo -e "\ngreat! let us begin!\n"
else
  echo "come back later then"
  exit
fi 

echo Create virtual environment and enter it
python -m venv venv
source venv/bin/activate

echo Install dependencies
pip install -r ./requirements.txt

echo Initialize database with name "stuffbase"
psql -d stuffbase < schema.sql
