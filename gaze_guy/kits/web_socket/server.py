import pickle
import socket
import struct
import cv2
import threading
import matplotlib.pyplot as plt

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
PORT = 8090

config = my_parse()
demo = Demo(config)

def link_handler(conn, client): 
    print("服务器开始接收来自[%s:%s]的请求...." % (client[0], client[1]))
    data = b'' ### CHANGED
    payload_size = struct.calcsize("L") ### CHANGED
    ''' 
    Python3以后，socket传递的都是bytes类型的数据，字符串需要先转换一下，string.encode()即可；另一端接收到的bytes数据想转换成字符串，只要bytes.decode()一下就可以。
    '''
    while True: 
        # Retrieve message size
        while len(data) < payload_size:
            packet = conn.recv(4*1024)
            if packet:
                data += packet
            else:
                break

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Extract frame
        print('接收完成')
        frame = pickle.loads(frame_data)

        '''
        实现推理功能
        '''
        demo._process_image(frame)
        processed_image = demo.visualizer.image
        print('推理完成')
        data = pickle.dumps(processed_image)

        # Send message length first
        message_size = struct.pack("L", len(data)) ### CHANGED
        conn.sendall(message_size + data)
        '''
        下面的代码OpenCV 展示图片Display失败的原因是 OSX平台限制，只能在主线程中使用UI交互函数。
        Use UI interaction functions from the "main" thread only. This is limitation of the platform, not OpenCV.
        '''
        # cv2.imshow('frame', frame)
        # cv2.waitKey(1)

        # 这个可以成功
        print('发送完成')
    
def main():
    # socket.socket()函数来创建一个socket对象，socket.socket()函数语法如下：
    # family: 套接字家族，可以使AF_UNIX或者AF_INET。
    # type: 套接字类型，根据是面向连接的还是非连接分为SOCK_STREAM或SOCK_DGRAM，也就是TCP和UDP的区别。
    # protocol: 一般不填默认为0。
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
