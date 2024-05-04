import sys
import os
import socket

serverPort = int(sys.argv[1]) # 테스트시 입력한 포트로
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Student ID : 20213047")
print("Name : Yewon Lee")

CONTENT_BODY =\
"""HTTP/1.0 200 OK
Connection: close
Content-Length: {length}
Content-Type: {type}

"""
ERROR_BODY =\
"""HTTP/1.0 404 NOT FOUND
Connection: close
Content-Length: 0
Content-Type: text/html

"""

def FileConverter(type, data): # 변환
    print(f"finish {len(data)}, {len(data)}", flush=True)
    return CONTENT_BODY.replace("{type}", type).replace("{length}", str(len(data))).encode('ascii')+data

try:
    while True:
        clientSocket, addr = serverSocket.accept() # 클라이언트

        print(f"Connection : Host IP {addr[0]}, Port {addr[1]}, socket 4", flush=True)

        request = clientSocket.recv(1024).strip() # 요청

        headers = request.split(b'\r\n\r\n')[0] # 나눠서 헤더 분리
        header_lines = headers.split(b'\r\n')[1:]  # 요청 라인을 제외하고 헤더만 추출
        cnt = len(header_lines) # 헤더 라인의 수

        for i in headers.split(b'\r\n'):
            if i.startswith(b'GET'):
                print(i.decode(), flush=True)
            elif i.startswith(b'User-Agent:'):
                print(i.split(b'(')[0][:-1].decode(), flush=True)

        print(f"{cnt} headers", flush=True)

        if request.startswith(b'GET '):
            filename = '.'+request.split()[1].decode()
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, 'rb') as f:
                    file_data = f.read()
                if filename.split('.')[2] == "html": # html
                    clientSocket.sendall(FileConverter('text/html', file_data))
                elif filename.split('.')[2] == "jpg": # jpg
                    clientSocket.sendall(FileConverter('image/jpeg', file_data))
            else:
                print(f"Server Error : No such file {filename}!", flush=True)
                clientSocket.sendall(ERROR_BODY.encode('ascii'))

        clientSocket.close() # 클라이언트 소켓 종료
finally:
    serverSocket.close() # 서버 소켓 종료