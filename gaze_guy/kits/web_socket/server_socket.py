import cv2
import numpy as np
import socket
import struct
import zlib

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def process_frame(frame):
    # 对图像进行高斯模糊
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    return blurred


# 启动服务器端口
address = ('localhost', 8000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(address)

server_socket.listen(5)

print('Server started!')


while True:
    
# 等待客户端连接

    print('Waiting for connection...')

    sock, addr = server_socket.accept()

    print('Client connected:', addr)


    data = b''
    payload_size = struct.calcsize("L")

    while True:
        #视频帧的大小和数据
        while len(data) < payload_size:
            data += sock.recv(8192)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size =struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += sock.recv(8192)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # 将数据解压缩并解码成图像格式
        # frame_data = zlib.decompress(frame_data)
        frame = np.frombuffer(frame_data, dtype=np.uint8)
        # frame = frame.reshape((480, 640, 3))

        # 处理图像 
        output_frame = process_frame(frame)

        # 将处理后的图像压缩成jpg格式并发送回客户端
        result, img_encoded = cv2.imencode('.jpg', output_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = zlib.compress(img_encoded, zlib.Z_BEST_COMPRESSION)
        sock.sendall(struct.pack("L", len(data)) + data)

client_socket.close()