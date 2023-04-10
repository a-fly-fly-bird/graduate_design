from flask import Flask, render_template, request, Response
from flask import Flask
import cv2
import numpy as np

from gaze_guy.display.parse import my_parse
from gaze_guy.ptgaze.server_demo import Demo

config = my_parse()
demo = Demo(config)
app = Flask(__name__)
processed_frame = None

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

    global processed_frame
    processed_frame = processed_image

    # 将处理后的图像转换成jpg格式
    _, processed_img_encoded = cv2.imencode('.jpg', processed_image)
    # 将jpg格式的帧转换成byte数组
    processed_img_bytes = processed_img_encoded.tobytes()
    # 返回byte数组
    return processed_img_bytes

# 生成视频流的函数
def generate_stream():
    while True:
        # 将处理后的帧转换成jpg格式
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        # 将jpg格式的帧转换成byte数组
        frame_bytes = buffer.tobytes()
        # 返回byte数组，作为视频流的一帧
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# 定义一个路由，用于打开摄像头并启动视频流
@app.route('/video_feed')
def video_feed():
    return Response(generate_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 定义可以接收POST请求的路由
@app.route('/process_video', methods=['POST'])
def process_video():
    # 接收客户端发来的图像数据
    img_data = request.get_data()
    # 对图像进行处理
    processed_img_bytes = process_image(img_data)
    # 返回处理后的图像
    return Response(response=processed_img_bytes, status=200, mimetype="image/jpeg")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
