import socket
import select

print("Student ID : 20213047")
print("Name : Yewon Lee")

# host = "netapp.cs.kookmin.ac.kr"
# 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 80
# 서버에 연결
# s.connect((host, port))
# 요청 전송
# s.sendall(b'GET /member/palladio.JPG HTTP/1.0\r\nHost: netapp.cs.kookmin.ac.kr\r\nUser-agent: HW1/1.0\r\nConnection: close\r\n\r\n')

while (1): 
  data = input("> ").split()
  if (data[0] == "down"):
    serverName = data[1].split("/")
    serverIp = socket.gethostbyname(serverName[2])
    if (serverName[0] != "http:"):
      print("Only Support http, not", serverName[0][:-1])
      continue
    try :
      s.connect((serverIp, port))
    except socket.gaierror :
      print("연결 ㄴㄴ")
      exit(1)

    msg = "GET /{} HTTP/1.0\r\nHost: {}\r\nUser-agent: HW1/1.0\r\nConnection: close\r\n\r\n".format("/".join(serverName[3:]), serverName[2])
    print(msg)
    s.send(msg.encode())
  elif (data[0] == "quit"):
    exit(1)

  # 응답받기
  response = b''
  while select.select([s],[],[],3)[0]:
    data = s.recv(1024)
    if not data:
      break
      print("아무것도없음")
    response += data

  headers =  response.split(b'\r\n\r\n')[0]
  image = response[len(headers)+4:]

  # save image
  f = open('palladio.JPG', 'wb')
  f.write(image)
  f.close()

# 소켓 연결 종료
  s.close()