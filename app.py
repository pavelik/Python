from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    emit('response', msg)

if __name__ == '__main__':
    socketio.run(app)
