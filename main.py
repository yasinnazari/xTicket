from psql_connection.db_conn import psql
from psycopg2.errors import NotNullViolation
from flask import Flask, request, json
import atexit
import requests
import os

app = Flask(__name__)
atexit.register(psql.db_close_conn)

@app.route('/sendmessage', methods=['POST'])
def send_message():
   conn = psql.get_conn()
   msg_data = request.form

   try:
      with conn.cursor() as cur:
         cur.execute('INSERT INTO messages (message, sender) VALUES (%s, %s)', (msg_data.get('msg_text'), msg_data.get('sender_name')))
         conn.commit()

         print('Message Sent!')
         return json.dumps({
                  "data" : {
                     "sender": msg_data.get('sender_name'),
                     "message": msg_data.get('msg_text'),
                  },
                  "meta": {
                     "code": 200,
                     "operation": "send"
                  }
               }
            )

   except Exception as e:
      return { "system": "message sent is failure", "err": e }

   finally:
      psql.release_conn(conn)


# Show all messages in database
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
  
   except Exception as e:
      return { "system": "messages not recived", "err": e }
   finally:
      psql.release_conn(conn)


@app.route('/deletemessage', methods=['DELETE'])
def delete_message():
   conn = psql.get_conn()
   msg_data = request.form

   try:
      with conn.cursor() as cur:
         msg_deleted = False

         find_sender = cur.execute("SELECT sender FROM messages WHERE id = (%s)", (msg_data.get('msg_id'),))
         fetch_sender_info = cur.fetchone()

         if fetch_sender_info != None:
            sender_name = fetch_sender_info[0]
         else:
            return { "data": { "system": f"message #{msg_data.get('msg_id')} not exists or already deleted" } }

         cur.execute('DELETE FROM messages WHERE id = (%s)', (msg_data.get('msg_id'),))
         conn.commit()
         msg_deleted = True

         if msg_deleted:
            return { 
               "data": {
                  "system": f"message #{msg_data.get('msg_id')} from {sender_name} successfuly removed" 
               },
               "meta": {
                     "code": 200,
                     "operation": "delete"
               }
            }

   except Exception as e:
      return { "system": "message not found for delete", "err": e }
  
   finally:
      psql.release_conn(conn)


if __name__ == '__main__':
   app.run(debug=True, port=8000)
