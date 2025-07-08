from src.database.db_conn import psql as db # use db for use this module methods
from src.validation.validation import data_validation as validate # use validate for use this module methods
from flask import Flask, request, jsonify, json
from pydantic import ValidationError
import atexit
import requests
import os

app = Flask(__name__)
atexit.register(db.db_close_conn)


@app.route('/sendmessage', methods=['POST'])
def send_message():
   conn = db.get_conn()

   try:
      message_data = request.get_json()
      message = validate(**message_data) # validate request body data 

      with conn.cursor() as cur:
         cur.execute('INSERT INTO messages (message, sender) VALUES (%s, %s)', (message.message_text, message.sender_username))
         conn.commit()

         print('Message Sent!')
      return {
         "data": {
            "message_text": message.message_text,
            "sender_username": message.sender_username
         },
         "meta": {
            "code": "200",
            "operation": "send"
         }
      }

   except ValidationError as err:
      error_list = [
         {
            'field': e['loc'][0],
            'reason': e['msg']
         }
         for e in err.errors()
      ]

      return jsonify({
         'code': 422,
         'errors': error_list,
         'message': 'validation failed',
         'status': 'error',
      }), 422

   finally:
      db.release_conn(conn)


# Show all messages in database
@app.route('/messages', methods=['POST'])
def show_messages():
   conn = db.get_conn()

   try:
      with conn.cursor() as cur:
         response = []
         cur.execute('SELECT * FROM messages')
         fetched_messages = cur.fetchall()

         for msg in fetched_messages:
            response.append({"id": msg[0], "name": msg[1], "username": msg[2]})
         return jsonify({"data": response, "meta": {"code": 200}})

   except Exception as e:
      return { 
         "system": "messages not recived", "err": e 
      }
   finally:
      db.release_conn(conn)


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------


# @app.route('/deletemessage', methods=['DELETE'])
# def delete_message():
#    conn = psql.get_conn()
#    msg_data = request.form

#    try:
#       with conn.cursor() as cur:
#          msg_deleted = False

#          find_sender = cur.execute("SELECT sender FROM messages WHERE id = (%s)", (msg_data.get('msg_id'),))
#          fetch_sender_info = cur.fetchone()

#          if fetch_sender_info != None:
#             sender_name = fetch_sender_info[0]
#          else:
#             return { "data": { "system": f"message #{msg_data.get('msg_id')} not exists or already deleted" } }

#          cur.execute('DELETE FROM messages WHERE id = (%s)', (msg_data.get('msg_id'),))
#          conn.commit()
#          msg_deleted = True

#          if msg_deleted:
#             return { 
#                "data": {
#                   "system": f"message #{msg_data.get('msg_id')} from {sender_name} successfuly removed" 
#                },
#                "meta": {
#                      "code": 200,
#                      "operation": "delete"
#                }
#             }

#    except Exception as e:
#       return { "system": "message not found for delete", "err": e }

#    finally:
#       psql.release_conn(conn)


if __name__ == '__main__':
   app.run(debug=True, port=8000)
