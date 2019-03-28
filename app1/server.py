from flask import Flask, jsonify, session, request, abort, make_response, render_template
import base64
import os, binascii
import sqlalchemy as sqa
from sqlalchemy.orm import sessionmaker
from db_models import User, Message
from datetime import datetime, timedelta
from uuid import uuid1
import sqlite3
old_connection =  sqlite3.connect('./p2.db')
cursor = old_connection.cursor()
connection = sqa.create_engine('sqlite+pysqlite:///p2.db', echo=True)
Session = sessionmaker(bind=connection)()
app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False #Need to do this so I can check if the session cookie is set on login I wonder if this could cause issues.
app.secret_key = binascii.b2a_base64(os.urandom(16))

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login():
    creds = request.get_json()
    if not creds.get('email') or not creds.get('password'):
        abort(401, 'No creds.')
    #The last dev left this raw sql here we've already updated the rest of the app to use sqlalchemy's managed orm but still need to do this one
    cursor.execute(f"SELECT * FROM users WHERE email='{creds.get('email')}' AND password='{creds.get('password')}'")
    user = cursor.fetchone()
    print(user)
    if not user:
        abort(401, 'User not found.')
    else:
        token = str(uuid1())
        email = creds.get('email').split("'")[0]
        connection.execute(f"UPDATE users SET sessionToken='{token}' WHERE email='{email}'")
        return jsonify({'token': token, 'expiry': (datetime.now() + timedelta(hours=24))})

@app.route('/register', methods=['POST'])
def register():
    creds = request.get_json()
    user = Session.query(User).filter_by(email=creds.get('email'), password=creds.get('password')).first()
    if user:
        abort(409, 'User exists.')
    try:
        new_user = User(email=creds.get('email'), password=creds.get('password'))
        Session.add(new_user)
        Session.commit()
        return 'Success!'
    except Exception as e:
        print(e)
        Session.rollback()
        abort(500)

@app.route('/message/new', methods=['POST'])
def new_message():
    token = request.headers.get('token')
    print(token)
    user = Session.query(User).filter_by(sessionToken=token).first()
    if not user:
        abort(401, 'No user.')
    data = request.get_json()
    print(request.get_json())
    if not data or not data.get('text'):
        abort(409, 'No message.')
    try:
        message = Message(user_id=user.id, content=data.get('text'))
        Session.add(message)
        Session.commit()
    except Exception as e:
        print(e)
        Session.rollback()
    return 'Success!'

@app.route('/message/get', methods=['GET'])
def read_messages():
    token = request.headers.get('token')
    user = Session.query(User).filter_by(sessionToken=token)
    if not user:
        abort(403, 'Not logged in.')
    messages = Session.query(Message).join(User, Message.user_id == User.id).add_columns(User.email).all()
    messages = list(map(lambda msg: { 'content': msg[0].content, 'author': msg[1] }, messages))
    return jsonify(messages)

@app.after_request
def after_request(response):
    header = response.headers
    return response

if __name__ == '__main__':
    app.run()
