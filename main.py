from flask import Flask, render_template, url_for, request, session, redirect
from flask_socketio import SocketIO, send
from flask_pymongo  import PyMongo
import bcrypt

app = Flask(__name__,template_folder='.')

app.config['SECRET_KEY'] = 'mysecret'
app.config['MONGO_DBNAME'] = 'accountsDB'
app.config['MONGO_URI'] = 'mongodb+srv://admin:<badpassword>@cluster0-eapoj.mongodb.net/accountsDB'
mongo = PyMongo(app)

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return render_template('index.html')

@app.route('/login')
def login():
    return ''

@app.rout('/register')
def register():
    return ''

if __name__ == '__main__':
	socketio.run(app)