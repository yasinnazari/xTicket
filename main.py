from psql_connection.db_conn import psql
from flask import Flask, request, json
import requests
import os

app = Flask(__name__)

@app.route('/sendmessage', methods=['POST'])
def send_message():
   conn = psql.get_conn()

   try:
      with conn.cursor() as cur:
         cur.execute('INSERT INTO messages (message, sender) VALUES (%s, %s)', ('Where are you ?', 'Lwis'))
         conn.commit()
         print('Message Sent!')
         return json.dumps(
               {
                  "data" : {
                     "sender": request.form['sender_name'], "message": request.form['msg_text']
                  },

                  "meta": {
                     "code": 200,
                     "operation": "send"
                  }

               }
            )
   except:
      print('Message send is failed !')
   finally:
      psql.release_conn(conn)


@app.route('/messages', methods=['POST'])
def show_messages():
   conn = psql.get_conn()

   try:
      with conn.cursor() as cur:
         response = []
         cur.execute('SELECT * FROM messages')
         fetched_messages = cur.fetchall()

         for msg in fetched_messages:
            response.append({"id": msg[0], "name": msg[1], "username": msg[2]})
         return json.dumps({"data": response, "meta": {"code": 200}})
   except:
      print('Messages Not Recived!')
   finally:
      psql.release_conn(conn)


if __name__ == '__main__':
   try:
      app.run(debug=True, port=8000)
   except:
      print("[X] Unexpected error check later")
   finally:
      psql.db_close_conn()
