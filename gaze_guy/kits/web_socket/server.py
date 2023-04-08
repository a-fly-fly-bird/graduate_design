import pickle
import socket
import struct
import cv2
import threading
import matplotlib.pyplot as plt

# 1. 创建套接字，绑定套接字到本地IP与端口：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()
# 2. 开始监听连接：s.listen()
# 3. 进入循环，不断接受客户端的连接请求：s.accept()
# 4. 接收传来的数据，或者发送数据给对方：s.recv() , s.sendall()
# 5. 传输完毕后，关闭套接字：s.close()

def link_handler(conn, client): 
    print("服务器开始接收来自[%s:%s]的请求...." % (client[0], client[1]))
    data = b'' ### CHANGED
    payload_size = struct.calcsize("L") ### CHANGED
    while True: 
        # Retrieve message size
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)

        # 下面的代码OpenCV 展示图片Display失败的原因是 OSX平台限制，只能在主线程中使用UI交互函数
        # Use UI interaction functions from the "main" thread only. This is limitation of the platform, not OpenCV.
        
        # Display
        # cv2.imshow('frame', frame)
        # cv2.waitKey(1)

        # 这个可以成功
        print(frame)


HOST = ''
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(4)
print('Socket now listening')

while True:
    conn, addr = s.accept()
    t = threading.Thread(target=link_handler, args=(conn, addr))
    t.start()

    
