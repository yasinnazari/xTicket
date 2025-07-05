from dotenv import load_dotenv
import os

load_dotenv('.env')

db_config = {
   'host' : os.getenv('PSQL_HOST'),
   'database' : os.getenv('PSQL_DBNAME'),
   'user' : os.getenv('PSQL_USER'),
   'password' : os.getenv('PSQL_PWD'),
   'port' : os.getenv('PSQL_PORT'),
}


t = dict(**db_config)

print(t)