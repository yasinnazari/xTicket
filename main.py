from psql_connection.db_conn import psql
from flask import Flask, request, json
import requests
import os

app = Flask(__name__)

@app.route('/sendmessage', methods=['POST'])
def send_message():
   conn = psql.get_conn()
   msg_text = request.form['msg_text']
   sender_name = request.form['sender_name']

   try:
      with conn.cursor() as cur:
         cur.execute('INSERT INTO messages (message, sender) VALUES (%s, %s)', (msg_text, sender_name))
         conn.commit()
         print('Message Sent!')
         return json.dumps({
                  "data" : {
                     "sender": sender_name,
                     "message": msg_text,
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
   except:
      print('Messages Not Recived!')
   finally:
      psql.release_conn(conn)


@app.route('/deletemessage', methods=['DELETE'])
def delete_message():
   conn = psql.get_conn()
   msg_id = request.form['msg_id']

   try:
      with conn.cursor() as cur:
         msg_deleted = False

         find_sender = cur.execute("SELECT sender FROM messages WHERE id = (%s)", (msg_id,))
         fetched_sender = cur.fetchone()
         if fetched_sender is not None:
            sender_name = fetched_sender[0]
         else:
            return { "system": "user not found" }

         for _ in range(0, 1, 1):
            cur.execute('DELETE FROM messages WHERE id = (%s)', (msg_id,))
            conn.commit()
            msg_deleted = True

         if msg_deleted:
            return { "system": f"message #{msg_id} from {sender_name} successfuly removed" }
         else:
            print(msg_deleted)
            return { "system": f"message #{msg_id} Not exists or already deleted" }
   except:
      return { "system": "unexpected error | message not found" }
   finally:
      psql.release_conn(conn)


if __name__ == '__main__':
   try:
      app.run(debug=True, port=8000)
   finally:
      psql.db_close_conn()
