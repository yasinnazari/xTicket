from psql_connection.db_conn import psql_connect
from aiohttp import web
from flask import Flask, request, json
import requests
import os

app = Flask(__name__)


@app.route('/messages', methods=['POST'])
def create_message():
   conn = psql_connect.get_conn()

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
      psql_connect.release_conn(conn)


if __name__ == '__main__':
   try:
      app.run(debug=True, port=8000)
   except:
      print("[X] Unexpected error check later")
   finally:
      psql_connect.db_close_conn()
