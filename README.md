# Python

Open-source python-based projects.

## Flask Chat Application

Basic application that emulates communication between different endpoints.

![Flask Chat APp](./images/flask-chat-app.png)

Back-end: Flask (Python), Socket.IO, PostgreSQL  
Front-end: Bootstrap 4, custom CSS

## Installation

1. [Configuration](#configuration)
2. [Local setup](#local-setup)
3. [Deployment to Heroku](#deployment-to-heroku)

----------

## Configuration

Before you go any further, make sure you have Python and that it’s available from your command line. You can check this by simply running:

```bash
python --version
```

Otherwise install python:

```bash
sudo apt-get install python3.6
```

Additionally, you’ll need to make sure you have pip available. It is a package manager for Python. You can check this by running:

```bash
pip --version
```

Otherwise install pip:

```bash
sudo apt-get install python-pip
```

Install virtualenv via pip:

```bash
pip install virtualenv
```

1. Create a virtual environment for a project:

```bash
sudo mkdir flask-chat-app
cd flask-chat-app
virtualenv env
```

2. To begin using the virtual environment, it needs to be activated:

```bash
source flask-chat-app/bin/activate
```

3. Add project folder under the source control:

```bash
git init
```

4. Create .gitignore file. This file is used to unstage ceratin folders / files from version control (mostly because of security or capcaity reasons).

```bash
touch .gitignore
```

add those folders / files:  
env/  
*.pyc


5. Install necessary dependencies by running:

```bash
pip install flask flask-socketio eventlet flask-sqlalchemy psycopg2 gunicorn
```
6. Save those packages into a special text file called 'requirements'. This step allows other developers to install those dependencies directly from a text file instead of copying a whole environment.

```bash
pip freeze > requirements.txt
```

**!!! IMPORTANT FOR LINUX USERS !!!**  
When we will be ready for deployment, Heroku does not understand this package:

`pkg-resources==0.0.0`

So just remove it from the file and save changes.

7. Choose your favourite text editor or IDE. I will be using [Visual Studio Code](https://code.visualstudio.com/).

----------

## Local setup

1. First of all, we need to think about a folder / file structure of the application. In our simple example I would like to keep it as simple as possible by following common conventions:

```bash
app.py
config.py
db_create.py
models.py
Procfile
requirements.txt
static/
templates/
env/
```

**Description:**

----------

[app.py](./app.py) - This is the file that is invoked to start up a development server. It gets a copy of the app from your package and runs it. This won’t be used in production, but it will see a lot of mileage in development.

[config.py](./config.py) - This file contains most of the configuration variables that your app needs.

[db_create.py](./db_create.py) - This file creates a database schema.

[models.py](./models.py) - This is where you define the domain models of your application.

[static/](./static/) - This directory contains the public CSS, JavaScript, images and other files that you want to make public via your app.

[templates/](./templates/) - This is where you’ll put the Jinja2 templates for your app.

We will discuss [Procfile](./Procfile) in the deployment section.

3. Let's write some boilerplate code for spinning up the default server:

[app.py](./app.py)

```python
from flask import Flask, render_template

app = Flask(__name__) 
 
@app.route('/') 
def index(): 
    return 'Hello, World!' 
 
if __name__ == '__main__': 
    app.run(debug = True) 
```
Launch the app from the terminal:

```bash
python app.py
```

4. Let's add some front-end. Create those files into templates/ folder.

[layout.html](./templates/layout.html)  
[index.html](./templates/index.html)

5. Add custom css and favicon:

[style.css](./static/style.css)
[chat-icon](./static/chat-icon.png)

Now we can render a template that we have created:

[app.py](./app.py)

```python
@app.route('/') 
def index(): 
    return render_template('index.html')
```
6. Adding bidirectional real-time communication between different endpoints.

First, we need to reference socket.io library in our ``layout.html`` template. Optionally you can add separate .js file for better maintanance:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.js"></script>
<script src="../static/socket.js"></script> 
```

Then, we also need to reference websocket on the server side:

[app.py](./app.py)

```python 
from flask_socketio import SocketIO, emit 
   
@socketio.on('message') 
# When message is posted handle the JSON object from the client.
# This data should be persisted in a database. We will take a look on that later.
def handleMessage(msg): 
    emit('response', msg) 
 
if __name__ == '__main__': 
    socketio.run(app) 
``` 

[socket.js](./static/socket.js)

```javascript
// Make a connection to the specific domain.
const socket = io.connect('https://flask-chat-app.herokuapp.com/');

// Get values from input fields.
// Send a JSON object to the server.
socket.emit('message', { 
        nickname: nickname, 
        message: message, 
        date: dateString 
    }); 

// On successfull response add bubble to the chatroom.
socket.on('response', (msg) => { 
    $('#messages').append( 
        `<label class="author">${msg.nickname}</label> 
            <div class="alert alert-dark" role="alert"> 
                ${msg.message} 
                <div class="text-muted text-right"> 
                    <small>${msg.date}</small> 
                </div> 
            </div>` 
    });
```

Websockets work based on event system. If we want to send some information to the server or client we use ``emit()`` method. If we want to trigger some action we use ``on()`` method.

7. Now it is time to slightly modify our application and start implementing an abstraction layer.

[config.py](./config.py)

```python
import os 
 
class BaseConfig(object): 
    DEBUG = False 
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' 
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] 
 
class DevelopmentConfig(BaseConfig): 
    DEBUG = True 
 
class ProductionConfig(BaseConfig): 
    DEBUG = False 
```

Notice that we are taking database connection string from environment variables which you can define yourself. Open terminal in a root folder of your project and type:

```bash
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://admin:01eamqnj@localhost/flask-chat-app"
```

This file is used as a 'settings' for our project.  
**Note: You should exclude this file from source control due to sensitive information.**

8. Now let's create our first domain class aka 'model':

[models.py](./models.py)

```python
from app import db 
from datetime import datetime 
 
class Message(db.Model): 
    __tablename__ = 'messages' 
    id = db.Column(db.Integer, primary_key = True) 
    nickname = db.Column(db.String(50), nullable = False) 
    body = db.Column(db.Text, nullable = False) 
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
 
    def __init__(self, nickname, body, created_at): 
        self.nickname = nickname 
        self.body = body 
        self.created_at = created_at 
```

9. Register database in entry point of the application:

[app.py](./app.py)

```python
from flask_sqlalchemy import SQLAlchemy 

# SQLAlchemy is ORM (Object Relational Mapper). Basically, it allows us to write plain python code without worring about SQL part which generates behind the scene.

db = SQLAlchemy(app) 
 
from models import *

@app.route('/') 
def index(): 
    # Get data from a database.
    messages = Message.query.all()

    # Pass recieved data to a view. 
    return render_template('index.html', messages = messages) 

# Now we are persisting data to the PostgreSQL database.
@socketio.on('message') 
def handleMessage(msg): 
    message = Message(msg['nickname'], msg['message'], msg['date']) 
    db.session.add(message) 
    db.session.commit() 
```

Also we want to display messages (if any) to the user:

[index.html](./templates/index.html)

```html
{% for message in messages %} 
        <label class="author">{{message.nickname}}</label> 
        <div class="alert alert-dark" role="alert"> 
            {{message.body}} 
            <div class="text-muted text-right"> 
                <small>{{message.created_at.strftime('%d.%m.%Y %H:%M:%S')}}</small> 
            </div> 
        </div> 
        {% endfor %} 
```

Here we are using Jinja view engine to loop through all messages which were passed from index controller.

10. Finally, we need to create schema by invoking db_create file:

[db_create.py](./db_create.py)

```python
from app import db 
from models import Message 
 
db.create_all() 
```

Terminal part:

```bash
python db_create.py
```

If you get this warning:  
``'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and... '``

Just ignore it.

Well, now your application is running localy! You can always test it by launching from terminal:

```bash
python app.py
```

Next, we will take a look on deployment part.

----------

## Deployment to Heroku

We need to make a little changes in application configuration. The good news is that the most of the work is already done.

1. Create a Procfile in the root folder of project.

[Procfile](./Procfile)

``web: gunicorn -k eventlet app:app``

**Note: This file does not have extension! This is special kind of file for Heroku. Here we are basically saying that we want to use gunicorn web server instead of built-in Flask server.**

By doing that, we can now remove those lines from our main [app.py](./app.py):

```python
if __name__ == '__main__': 
    socketio.run(app)
```

2. Create [runtime.txt](./runtime.txt) file. Again, all in the root folder.

``python-3.6.4 ``

**This file specifies the version of Python interpreter so Heroku knows which tools to use.**

It is all we need to do from Python's side.

Now let's take a look on Heroku.

3. You will need to setup Heroku CLI and account. You have to do this on your own. So please take a look on heroku website. 

4. When you finish installing Heroku CLI, you can log in to your account via terminal:

```bash
heroku login
```

5. Enter your credentials.

6. Then, create your application by running command:

```bash
heroku create flask-chat-app
```

_If you ommit the name, Heroku will choose a random for you._

7. We need to reference PostgreSQL by adding addon:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

8. Point connection string to the remote database:

```bash
heroku config:set APP_SETTINGS=config.ProductionConfig --remote heroku
```

9. Since we have initialized our project in the beginning we can now use git commands to push our repository to heroku:

```bash 
git add --all
```

```bash 
git commit -m "Deployment to Heroku."
```

```bash 
git push heroku master
```

10. Now we are live! But you will get 500 Internal Server Error. Because we have not moved our database. Heroku did not know anything about [db_create.py](./db_create.py) file before pushing.

```bash
heroku run python db_create.py
```

### WE ARE DONE!!

----------

## Known issues / tips

As I said in the beginning it was very simple demonstration of websocket and flask framework. We have not talked about security and Socket.IO API that much. So, if you want to take this application to the next level you should handle this types of security problems:

**CSSA / CSFI / SQL Injection**

You may also consider to add those features:

- Infinite scroll
- User session difference
- Private chat
- User connection state
