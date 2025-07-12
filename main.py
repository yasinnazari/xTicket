from src.database.db_conn import psql as db # use db for use this module methods
from src.validation.validation import validate_send_msg, validate_del_msg # use validate for use this module methods
from flask import Flask, request, jsonify, json
from pydantic import ValidationError
import atexit
import requests
import os

app = Flask(__name__)

@app.route('/sendmessage', methods=['POST'])
def send_message():
   try:
      conn = db.get_conn()
   except:
      return {
         "system": "Failed to connect database"
      }

   try:
      message_data = request.get_json()
      message = validate_send_msg(**message_data) # validate send message request body data 

      with conn.cursor() as cur:
         cur.execute("SELECT EXISTS(SELECT 1 FROM tickets WHERE sender = (%s))", (message.sender_username,))
         check_username = cur.fetchone()

         if check_username[0] == False:
            cur.execute('INSERT INTO tickets (message, sender) VALUES (%s, %s)', (message.message_text, message.sender_username))
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
         else:
            return jsonify({
               "meta": {
                  'code': 422,
                  'key': 'username already exist',
                  'status': 'error',
               }
            }), 422

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
@app.route('/showmessages', methods=['POST'])
def show_messages():
   try:
      conn = db.get_conn()
   except:
      return {
         "system": "Failed to connect database"
      }

   try:
      with conn.cursor() as cur:
         response = []
         cur.execute('SELECT * FROM tickets')
         fetched_messages = cur.fetchall()

         for msg in fetched_messages:
            response.append({"id": msg[0], "name": msg[1], "username": msg[2]})
         return jsonify({"data": response, "meta": {"code": 200}})

   except:
      return jsonify({
            "meta": {
               "code": 400,
               "status": "error",
               "key": "failed to load tickets"
            }
         }), 400

   finally:
      db.release_conn(conn)


# delete message with id
@app.route('/deletemessage', methods=['DELETE'])
def delete_message():
   try:
      conn = db.get_conn()
   except:
      return jsonify({
         "system": "failed to connect database"
      }), 500

   try:
      message_data = request.get_json()
      message = validate_del_msg(**message_data) #validate delete message request body data

      with conn.cursor() as cur:
         cur.execute("SELECT EXISTS(SELECT 1 FROM tickets WHERE id = (%s))", (message.id, ))
         check_id = cur.fetchone()

         if check_id[0] == True:
            cur.execute('DELETE FROM tickets WHERE id = (%s)', (message.id,))
            conn.commit()
            return {
               "data": {
                  "system": f"message #{message.id} successfully deleted",
                  "message_id" : message.id
               },

               "meta": {
                  "code": 200,
                  "operation": "delete"
               }
            }

         else:
            return jsonify({
               "meta": {
                  "code": 400,
                  "status": "error",
                  "key": "this id does not exist"
               }
            }), 400

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


atexit.register(db.db_close_conn)
if __name__ == '__main__':
   app.run(debug=True, port=8000)
