import socket, cv2, pickle,struct

from gaze_guy.display.parse import my_parse
from gaze_guy.ptgaze.server_demo import Demo

'''
1. 创建套接字，绑定套接字到本地IP与端口：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()
2. 开始监听连接：s.listen()
3. 进入循环，不断接受客户端的连接请求：s.accept()
4. 接收传来的数据，或者发送数据给对方：s.recv() , s.sendall()
5. 传输完毕后，关闭套接字：s.close()
'''

config = my_parse()
demo = Demo(config)

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
    client_socket,addr = server_socket.accept()
    print('GOT CONNECTION FROM:',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        
        while(vid.isOpened()):
            img,frame = vid.read()
            
            demo._process_image(frame)
            processed_image = demo.visualizer.image
        
            a = pickle.dumps(processed_image)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            
            cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_socket.close()