import cv2
import numpy as np
import socket
import sys
import pickle
import struct


def main():
    '''
    1. 创建套接字，连接服务器地址：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.connect()
    2. 连接后发送数据和接收数据：s.sendall(), s.recv()
    3. 传输完毕后，关闭套接字：s.close()
    '''

    cap = cv2.VideoCapture(0)
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8090))

    data_re = b''  # CHANGED
    payload_size = struct.calcsize("L")  # CHANGED

    while True:
        ret, frame = cap.read()
        # Serialize frame
        data = pickle.dumps(frame)
        # Send message length first
        message_size = struct.pack("L", len(data))  # CHANGED
        # Then data
        clientsocket.sendall(message_size + data)
        print('client 发送完成')

        # Retrieve message size
        while len(data_re) < payload_size:
            packet = clientsocket.recv(4*1024)
            print('why?')
            if packet:
                data_re += packet
            else:
                break

        packed_msg_size = data_re[:payload_size]
        data_re = data_re[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]  # CHANGED
        # Retrieve all data based on message size
        while len(data_re) < msg_size:
            data_re += clientsocket.recv(4096)
        frame_data = data_re[:msg_size]
        data_re = data_re[msg_size:]
        # Extract frame
        frame = pickle.loads(frame_data)
        print('client 接收完成')
        cv2.imshow('frame', frame)
        key = cv2.waitKey(10)
        if key == 13:
            break
    
    clientsocket.close()


if __name__ == '__main__':
    main()
