import pickle
import socket
import struct
import cv2
import threading
import matplotlib.pyplot as plt
import imutils

from gaze_guy.display.parse import my_parse
from gaze_guy.ptgaze.server_demo import Demo

'''
1. 创建套接字，绑定套接字到本地IP与端口：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()
2. 开始监听连接：s.listen()
3. 进入循环，不断接受客户端的连接请求：s.accept()
4. 接收传来的数据，或者发送数据给对方：s.recv() , s.sendall()
5. 传输完毕后，关闭套接字：s.close()
'''

HOST = ''
PORT = 10000

config = my_parse()
demo = Demo(config)

def link_handler(conn, client): 
    data = b""
    payload_size = struct.calcsize("Q")
    print("服务器开始接收来自[%s:%s]的请求...." % (client[0], client[1]))
    while True:
        while len(data) < payload_size:
            packet = conn.recv(4*1024) 
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        
        # cv2.imshow("SERVER VIDEO",frame)
        # key = cv2.waitKey(1) & 0xFF
        # if key  == ord('q'):
        #     break
        
        demo._process_image(frame)
        processed_image = demo.visualizer.image
        a = pickle.dumps(processed_image)
        message = struct.pack("Q",len(a))+a
        conn.sendall(message)
        
    conn.close()
    cv2.destroyAllWindows()


def main():
    '''
    socket.socket()函数来创建一个socket对象，socket.socket()函数语法如下：
    family: 套接字家族，可以使AF_UNIX或者AF_INET。
    type: 套接字类型，根据是面向连接的还是非连接分为SOCK_STREAM或SOCK_DGRAM，也就是TCP和UDP的区别。
    protocol: 一般不填默认为0。
    '''
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
        print('开始新线程处理')

if __name__ == '__main__':
    main()
