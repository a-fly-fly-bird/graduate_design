from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")


def process_image(img_data):
    img_np = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    # Add your image processing logic here
    _, processed_img_encoded = cv2.imencode('.jpg', img)
    processed_img_bytes = processed_img_encoded.tobytes()
    return processed_img_bytes


@app.route('/')
def index():
    return render_template('gpt.html')


@socketio.on('send_frame')
def handle_frame(data):
    img_data = data['image']
    processed_img_bytes = process_image(img_data)
    emit('receive_frame', {'image': processed_img_bytes}, broadcast=False)


if __name__ == '__main__':
    socketio.run(app)
