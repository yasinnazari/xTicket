from aiohttp import web
from flask import Flask, request, json
from dotenv import load_dotenv
from psycopg2 import pool
import psycopg2
import requests
import os

load_dotenv('.env')
app = Flask(__name__)

db_config = {
      'host' : os.getenv('PSQL_HOST'),
      'database' : os.getenv('PSQL_DBNAME'),
      'user' : os.getenv('PSQL_USER'),
      'password' : os.getenv('PSQL_PWD'),
      'port' : os.getenv('PSQL_PORT'),
   }

try:
   # Create connection pool and give connection 
   db_pool_conn = pool.SimpleConnectionPool(4, 10, **db_config)
   print('🟢 ✧ Connection was successfuly')
except:
   print('🔴 ✧ Connection was failure')


# give connection from ready connections first from minconn and second from maxconn
def get_conn():
   return db_pool_conn.getconn()


# release connection 
def release_conn(c):
   db_pool_conn.putconn(c)


def db_close_conn():
   db_pool_conn.closeall()
   print('🔴 ✧ Connection Disconnected')

@app.route('/messages', methods=['POST'])
def show_messages():
   conn = get_conn()

   try:
      with conn.cursor() as cur:
         response = []
         cur.execute('SELECT * FROM messages')
         fetched_messages = cur.fetchall()

         for msg in fetched_messages:
            response.append({"id": msg[0], "name": msg[1], "username": msg[2]})
         return json.dumps({"data": response, "meta": {"code": 200}})
   except:
      print('Message Not Sent!')
   finally:
      release_conn(conn)


if __name__ == '__main__':
   try:
      app.run(debug=True, port=8000)
   except:
      print("[X] Unexpected error check later")
   finally:
      db_close_conn()
