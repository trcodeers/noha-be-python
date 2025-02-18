from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import logging

logging.basicConfig(level=logging.DEBUG)  # Ensure logs are visible
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

guest_namespace = '/guest'

@socketio.on('connect', namespace=guest_namespace)
def handle_connect():
    logger.info(f"A guest connected: {request.sid}")

@socketio.on('audioStream', namespace=guest_namespace)
def handle_audio_stream(audio_chunk):
    print(audio_chunk)
    socketio.emit('streamBack', audio_chunk, namespace=guest_namespace)

@socketio.on('stopRecording', namespace=guest_namespace)
def handle_stop_recording():
    print(f"Stopping recording for {request.sid}")   

@socketio.on('disconnect', namespace=guest_namespace)
def handle_disconnect():
    print(f"User disconnected: {request.sid}")   

# Define a GET route
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')  # Default value is 'Guest' if no name is provided
    return f"Hello, {name}!"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2000)
