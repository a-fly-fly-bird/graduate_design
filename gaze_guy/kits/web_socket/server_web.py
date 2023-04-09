
from flask import Flask, request, Response
import cv2

app = Flask(__name__)

# 设置摄像头ID
camera = cv2.VideoCapture(0)

# 处理视频帧的函数
def process_frame(frame):
    # TODO: 在这里写视频处理的代码
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 返回处理后的帧
    return gray

# 生成视频流的函数
def generate_stream():
    while True:
        # 读取一帧图像
        ret, frame = camera.read()
        if not ret:
            break
 # 处理图像
        processed_frame = process_frame(frame)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
