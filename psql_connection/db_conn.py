from dotenv import load_dotenv
from psycopg2 import pool
import psycopg2
import os

load_dotenv('.env')

db_config = {
   'host' : os.getenv('PSQL_HOST'),
   'database' : os.getenv('PSQL_DBNAME'),
   'user' : os.getenv('PSQL_USER'),
   'password' : os.getenv('PSQL_PWD'),
   'port' : os.getenv('PSQL_PORT'),
}

try:
   # Create connection pool and give connection 
   db_pool_conn = pool.SimpleConnectionPool(7, 20, **db_config)
   print('🟢 ✧ Connection was successfuly')
except:
   print('-'*30)
   print('🔴 ✧ Connection was failure')
   print('-'*30)


class psql:
   def init(self):
      pass

   # give connection from ready connections first from minconn and second from maxconn
   def get_conn():
      return db_pool_conn.getconn()


   # Release connection 
   def release_conn(c):
      db_pool_conn.putconn(c)


   # Close Connection
   def db_close_conn():
      db_pool_conn.closeall()
      print('🔴 ✧ Connection Disconnected')
