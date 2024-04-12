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
sql/init.bash

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

echo generate admin credientials
echo the account will be created first time you go to /admin without logging in
ADMIN_USERNAME=$(python3 -c 'import secrets
print(secrets.token_hex(16))')  
ADMIN_PASSWORD=$(python3 -c 'import secrets
print(secrets.token_hex(16))')  

cat << EOF > .env
DATABASE_URL="$DATABASE_URL"
SECRET_KEY="$SECRET_KEY"
ADMIN_USERNAME="$ADMIN_USERNAME"
ADMIN_PASSWORD="$ADMIN_PASSWORD"
EOF
