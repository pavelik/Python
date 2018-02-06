from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

socketio = SocketIO(app)
db = SQLAlchemy(app)

from models import *

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages = messages)

@socketio.on('message')
def handleMessage(msg):
    message = Message(msg['nickname'], msg['message'], msg['date'])
    db.session.add(message)
    db.session.commit()
    
    emit('response', msg)

if __name__ == '__main__':
    socketio.run(app)
