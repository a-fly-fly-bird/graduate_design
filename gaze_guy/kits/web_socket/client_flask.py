import cv2
import requests
import numpy as np

server_url = 'http://localhost:10000/process_video'

# 声明要使用的视频编解码器
# codec = cv2.VideoWriter_fourcc(*'MP4V')
# 定义视频帧率
frameRate = 10.0
# 设置摄像头ID
cap = cv2.VideoCapture(0)
# 获取每一帧的宽高信息
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 开始录制
# output = cv2.VideoWriter("output.mp4", codec, frameRate, (frame_width, frame_height))

while(True):
    # 读取每一帧
    ret, frame = cap.read()
    # 如果读取到了视频帧
    if ret:
        # 发送图像数据到服务器
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(server_url, img_encoded.tobytes())

        # 解析处理后的视频帧
        response_data = np.frombuffer(response.content, np.uint8)
        processed_frame = cv2.imdecode(response_data, cv2.IMREAD_COLOR)

        # 显示视频帧
        cv2.imshow('video frame', processed_frame)
        # 写入视频
        # output.write(processed_frame)

        # 如果按下了q键，就停止录制、关闭窗口并释放摄像头资源
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

#放摄像头资源、停止录制并销毁显示窗口
cap.release()
# output.release()
cv2.destroyAllWindows()
