from dotenv import load_dotenv
from psycopg2 import pool
import psycopg2
import os

load_dotenv('.env')

class psql:
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
   except Exception as e:
      print('-'*30)
      print('🔴 ✧ Connection was failure')
      print('-'*30)
      print(e)
      print('-'*30)


   def init(self):
      pass

   # give connection from ready connections first from minconn and second from maxconn
   @staticmethod
   def get_conn():
      return psql.db_pool_conn.getconn()

   # Release connection
   @staticmethod
   def release_conn(c):
      psql.db_pool_conn.putconn(c)

   @staticmethod
   def db_close_conn(exception=None):
      psql.db_pool_conn.closeall()
      print('🔴 ✧ Connection Disconnected')

