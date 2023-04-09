import base64
import io
from flask import Flask, request, Response
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
from PIL import Image

from gaze_guy.display.parse import my_parse
from gaze_guy.ptgaze.server_demo import Demo


config = my_parse()
demo = Demo(config)
app = Flask(__name__)
socketio = SocketIO(app)

# 处理接收到的图像
def process_image(img_data):
    # 将二进制数据转换为numpy数组
    img_np = np.frombuffer(img_data, np.uint8)
    # 解码图像数据
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    # 在这里写实现视频帧处理的代码
    demo._process_image(img)
    processed_image = demo.visualizer.image
    print('处理完成')
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将处理后的图像转换成jpg格式
    _, processed_img_encoded = cv2.imencode('.jpg', processed_image)
    # 将jpg格式的帧转换成byte数组
    processed_img_bytes = processed_img_encoded.tobytes()
    # 返回byte数组
    return processed_img_bytes

@socketio.on('image')
def image(data_image):
    sbuf = io.StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2GRAY)

    # Process the image frame
    frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

# 定义可以接收POST请求的路由
@app.route('/process_video', methods=['POST'])
def process_video():
    # 接收客户端发来的图像数据
    img_data = request.get_data()
    # 对图像进行处理
    processed_img_bytes = process_image(img_data)
    # 返回处理后的图像
    return Response(response=processed_img_bytes, status=200, mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
