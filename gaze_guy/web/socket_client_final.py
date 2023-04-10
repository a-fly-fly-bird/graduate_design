import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import imutils


def main():
    '''
    1. 创建套接字，连接服务器地址：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.connect()
    2. 连接后发送数据和接收数据：s.sendall(), s.recv()
    3. 传输完毕后，关闭套接字：s.close()
    '''

    cap = cv2.VideoCapture(0)
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8090))

    # Socket Accept
    while(cap.isOpened() and clientsocket):
        _,frame = cap.read()
        frame = imutils.resize(frame,width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        clientsocket.sendall(message)

        cv2.imshow('TRANSMITTING VIDEO',frame)
        key = cv2.waitKey(1) & 0xFF
        if key ==ord('q'):
            clientsocket.close()
            break
        
    clientsocket.close()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
