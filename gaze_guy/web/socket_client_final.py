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
    clientsocket.connect(('localhost', 10000))

    # Socket Accept
    while(cap.isOpened() and clientsocket):
        _,frame = cap.read()
        frame = imutils.resize(frame,width=800)
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        clientsocket.sendall(message)

        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            packet = clientsocket.recv(4*1024) 
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += clientsocket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("CLIENT VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
    clientsocket.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
