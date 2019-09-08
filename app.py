from flask import Flask, render_template, url_for, request, session, redirect, Response
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_pymongo  import PyMongo
from camera_effects import Camera_effects
from camera import Camera
import bcrypt

app = Flask(__name__,template_folder='./templates')

app.config['SECRET_KEY'] = 'mysecret'
app.config['MONGO_DBNAME'] = 'accountsDB'
app.config['MONGO_URI'] = 'mongodb+srv://admin:badpassword@cluster0-eapoj.mongodb.net/accountsDB'
mongo = PyMongo(app)
camera = {}
socketio = SocketIO(app, cors_allowed_origins="*")
queue = []

@socketio.on('publicMessage')
def handleMessage(data):
	emit('publicMessage', data, room=data['room'])

@socketio.on('init')
def handleInit(data):
    join_room(data['room'])
    emit('init', data['username'], room=data['room'])

@socketio.on('initiateMatch')
def handleMatch(userdata):
    if len(queue) > 0 :
        if userdata in queue :
            return
        existing_data = queue.pop()
        newroom = userdata + ":" + existing_data
        emit('roomFound', newroom)
        emit('roomFound', newroom, room=existing_data.split(":")[1])
    else:
        queue.append(userdata)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('match.html', user=session['username'])
    return render_template('index.html')

@app.route('/matched/<room_id>', methods=['POST'])
def matched(room_id):
    if 'username' in session:
        return render_template('chat.html', user=session['username'], room=room_id)
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

@socketio.on('input_frame')
def test_message(payload):
    input = payload['dataURL']
    myStreamID = payload['streamID']
    input = input.split(",")[1]
    try: 
        camera[myStreamID].enqueue_input(input)
    except: 
        camera[myStreamID] = Camera(Camera_effects())
        camera[myStreamID].enqueue_input(input)
        #camera.enqueue_input(base64_to_pil_image(input))

def gen(streamID):
    '''Video streaming generator function.'''
    app.logger.info("starting to generate frames!")
    while True:
        try: 
            frame = camera[streamID].get_frame() #pil_image_to_base64(camera.get_frame())
        except: 
            camera[streamID] = Camera(Camera_effects())
            frame = camera[streamID].get_frame() #pil_image_to_base64(camera.get_frame())
        try: 
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')

@app.route('/get_stream/<streamID>')
def get_stream(streamID):
    '''This route will iterate through the video frames of stream. Putting this
        in the source of an img tag will simulate video stream'''
    return Response(gen(streamID), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	socketio.run(app)