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

echo lets create a base for .env file
echo Is psql installed with local-pg script? y/n
read -r
if [[ $REPLY = "y" ]]; then
  url="postgresql+psycopg2://stuffbase"
else
  url="postgresql:///stuffbase"
fi

echo "database URL: $url"

echo generate secret...
secret=$(python3 -c 'import secrets
print(secrets.token_hex(16))')  

cat << EOF > .env
DATABASE_URL="$url"
SECRET_KEY="$secret"
EOF
