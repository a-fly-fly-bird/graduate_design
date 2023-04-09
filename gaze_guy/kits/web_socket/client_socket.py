import cv2
import numpy as np
import socket
import struct
import zlib
import pickle

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: 
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# 启动客户端
server_address = ('localhost', 8000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取一帧视频并对图像进行
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    # result, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90]) # 打包图像数据和压缩级别
    # data = b''.join([img_encoded.tobytes(), struct.pack('B', zlib.Z_BEST_COMPRESSION)])

    # 发送图像数据到服务器
    try:
        # 打包数据长度和数据
        client_socket.sendall(struct.pack("L", len(data)) + data)
        payload_size = struct.calcsize("L")
        # 等待服务器返回数据并解码
        while True:
            while len(data) < payload_size:
                data += client_socket.recv(payload_size - len(data))

            msg_size = struct.unpack("L", data[:payload_size])[0]
            print(f"Received message size: {msg_size}")
            data = data[payload_size:]

            frame_data = recvall(client_socket, msg_size)
            print(f"Received frame data size: {len(frame_data)}")

            frame_data = zlib.decompress(frame_data)
            frame = np.frombuffer(frame_data, dtype=np.uint8, frame = frame((480, 640, 3)))

            # 显示图像
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(e)
        break

cap.release()
client_socket.close()
