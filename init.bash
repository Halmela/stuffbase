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

if ! sql/init_db.bash; then
  echo try initializing again when you have created the database
  exit 1
fi

echo lets create a base for .env file
echo Is psql installed with local-pg script? y/n
read -r
if [[ $REPLY = "y" ]]; then
  DATABASE_URL="postgresql+psycopg2://stuffbase"
else
  DATABASE_URL="postgresql:///stuffbase"
fi

echo "database url: $DATABASE_URL"

echo generate secret...
SECRET_KEY=$(python3 -c 'import secrets
print(secrets.token_hex(16))')  

cat << EOF > .env
DATABASE_URL="$DATABASE_URL"
SECRET_KEY="$SECRET_KEY"
EOF
