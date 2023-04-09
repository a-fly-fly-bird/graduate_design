import cv2
import numpy as np
import socket
import sys
import pickle
import struct

# 1. 创建套接字，连接服务器地址：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.connect()
# 2. 连接后发送数据和接收数据：s.sendall(), s.recv()
# 3. 传输完毕后，关闭套接字：s.close()

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))

while True:
    ret,frame=cap.read()
    # Serialize frame
    data = pickle.dumps(frame)

    # Send message length first
    message_size = struct.pack("L", len(data)) ### CHANGED

    # Then data
    clientsocket.sendall(message_size + data)

    # Retrieve message size
    