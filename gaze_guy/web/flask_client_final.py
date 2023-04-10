import cv2
import requests
import numpy as np

class FrontEnd:
    def __init__(self):
        self.SERVER_URL = 'http://localhost:9999/process_video'
        self.cap = cv2.VideoCapture(0)
        self.output = None

    def __del__(self):
        self.cap.release()
        if self.output:
            self.output.release()
        cv2.destroyAllWindows()

    def run(self):
        while(True):
            # 读取每一帧
            ret, frame = self.cap.read()
            # 如果读取到了视频帧
            if ret:
                response = self.send2backend(frame)
                processed_frame = self.process_response(response)
                # 显示视频帧
                cv2.imshow('video frame', processed_frame)
                # 如果按下了q键，就停止录制、关闭窗口并释放摄像头资源
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        #放摄像头资源、停止录制并销毁显示窗口
        self.cap.release()
        cv2.destroyAllWindows()

    def send2backend(self, frame):
        # 发送图像数据到服务器
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(self.SERVER_URL, img_encoded.tobytes())
        return response
    
    def process_response(self, response):
        # 解析处理后的视频帧
        response_data = np.frombuffer(response.content, np.uint8)
        processed_frame = cv2.imdecode(response_data, cv2.IMREAD_COLOR)
        return processed_frame
    
    def init_record(self):
        # 声明要使用的视频编解码器
        codec = cv2.VideoWriter_fourcc(*'MP4V')
        # 定义视频帧率
        frameRate = 10.0
        # 获取每一帧的宽高信息
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 开始录制
        output = cv2.VideoWriter("output.mp4", codec, frameRate, (frame_width, frame_height))
        return output
    
    def record(self, output, frame):
        output.write(frame)

    def init_get_image_from_url(self):
        self.url = 'http://localhost:10000/video_feed'
        # 打开摄像头并准备读取视频流
        self.web_cap = cv2.VideoCapture(self.url)
        if not self.web_cap.isOpened():
            print('无法打开视频流')
            exit(0)
        
    def get_image_from_url(self):
        self.init_get_image_from_url()
        # 读取视频流并展示图像
        while True:
            ret, frame = self.web_cap.read()
            if ret:
                cv2.imshow('Video Stream', frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
        
        # 释放摄像头资源
        self.web_cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    frontend = FrontEnd()
    frontend.run()
    # frontend.get_image_from_url()
