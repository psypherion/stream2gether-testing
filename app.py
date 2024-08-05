from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
import os
import uuid
import shutil
import json
import ngrok_handler
import auth_token_creator
import eventlet

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'assets'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'webm', 'avi', 'mov', 'vid'}

rooms = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_assets_folder():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route('/')
def index():
    room_key = str(uuid.uuid4())
    rooms[room_key] = {'video': None, 'user_names': []}
    session['room_key'] = room_key
    return render_template('index.html', room_key=room_key)

@app.route('/host', methods=['GET', 'POST'])
def host():
    if request.method == 'POST':
        room_key = session.get('room_key')
        if not room_key or room_key not in rooms:
            room_key = str(uuid.uuid4())
            rooms[room_key] = {'video': None, 'user_names': []}

        movie_name = request.form.get('going_to_watch', 'Untitled')
        user_name = request.form.get('name', 'anon')
        
        rooms[room_key]['movie_name'] = movie_name
        if user_name not in rooms[room_key]['user_names']:
            rooms[room_key]['user_names'].append(user_name)

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                clear_assets_folder()
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sample.mp4')
                file.save(file_path)
                rooms[room_key]['video'] = 'sample.mp4'
                return redirect(url_for('watch_video', room_key=room_key))

    return render_template('room.html')

@app.route('/guest', methods=['GET', 'POST'])
def guest():
    if request.method == 'POST':
        room_key = request.form['room_key']
        user_name = request.form.get('name', 'anon')
        if room_key in rooms:
            session['room_key'] = room_key
            session['user_name'] = user_name
            if user_name not in rooms[room_key]['user_names']:
                rooms[room_key]['user_names'].append(user_name)
            return redirect(url_for('watch_video', room_key=room_key))
    return render_template('guest.html')

@app.route('/watch/<room_key>')
def watch_video(room_key):
    room = rooms.get(room_key, {})
    video_filename = room.get('video')
    movie_name = room.get('movie_name', 'Untitled Movie')
    user_names = room.get('user_names', [])
    
    if video_filename:
        ngrok_urls = ngrok_handler.get_ngrok_urls()
        if ngrok_urls:
            video_url = f'{ngrok_urls[0]}/video'
            print(f"Share the link: {ngrok_urls[1]}/{room_key}")
        else:
            video_url = f'http://127.0.0.1:3000/video'
            print(f"Share the link: {video_url}/{room_key}")

        return render_template('glassmorphism.html', room_key=room_key, video_url=video_url, movie_name=movie_name, user_names=user_names)
    return 'Room or video not found', 404

@app.route('/set_name', methods=['POST'])
def set_name():
    data = request.get_json()
    session['user_name'] = data.get('name', 'anon')
    return '', 200

@socketio.on('send_message')
def handle_message(message):
    user_name = session.get('user_name', 'anon')
    formatted_message = f"{user_name} : {message}"
    emit('receive_message', formatted_message, broadcast=True)

@socketio.on('offer')
def handle_offer(data):
    room_key = data['room_key']
    emit('offer', data, to=room_key)

@socketio.on('answer')
def handle_answer(data):
    room_key = data['room_key']
    emit('answer', data, to=room_key)

@socketio.on('candidate')
def handle_candidate(data):
    room_key = data['room_key']
    emit('candidate', data, to=room_key)

if __name__ == '__main__':
    auth_token_creator.main()
    try:
        ngrok_handler.save_ngrok_urls()
    except Exception as e:
        print(f"Error starting ngrok: {e}")
    socketio.run(app, debug=True)
