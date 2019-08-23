from flask import Flask, render_template, url_for, request, session, redirect
from flask_socketio import SocketIO, send, emit
from flask_pymongo  import PyMongo
import bcrypt

app = Flask(__name__,template_folder='./templates')

app.config['SECRET_KEY'] = 'mysecret'
app.config['MONGO_DBNAME'] = 'accountsDB'
app.config['MONGO_URI'] = 'mongodb+srv://admin:badpassword@cluster0-eapoj.mongodb.net/accountsDB'
mongo = PyMongo(app)

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('publicMessage')
def handleMessage(msg):
	emit('publicMessage', msg, broadcast=True)

@socketio.on('init')
def handleInit(username):
    emit('init', username, broadcast=True)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('chat.html', user=session['username'])
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    existing_user = users.find_one({'name' : request.form['username']})

    if existing_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), existing_user['password']) == existing_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Error: Bad login credentials'
    

    

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user= users.find_one({'name' : request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'Error: An account with that username already exists'
    return render_template('register.html')

if __name__ == '__main__':
	socketio.run(app)