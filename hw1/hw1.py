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
    print("serverName출력",serverName)
    try :
      s.connect((serverIp, port))
    except socket.gaierror :
      print(f"{serverName[2]}: unknown host")
      print("cannot connect to server",serverName[2],port)
      exit(1)
    serverIp = socket.gethostbyname(serverName[2])
    if (serverName[0] != "http:"):
      print("Only Support http, not", serverName[0][:-1])
      continue

    msg = "GET /{} HTTP/1.0\r\nHost: {}\r\nUser-agent: HW1/1.0\r\nConnection: close\r\n\r\n".format("/".join(serverName[3:]), serverName[2])
    print(msg)
    s.send(msg.encode())
  elif (data[0] == "quit"):
    exit(1)

  # 응답받기
  response = b''
  while select.select([s],[],[],3)[0]:
    d = s.recv(1024)
    if not d:
      break
      print("아무것도없음")
    response += d

  headers =  response.split(b'\r\n\r\n')[0]
  image = response[len(headers)+4:]

  sCode = headers.split(b'\r\n')[0].decode()
  s = sCode.split()
  if (s[1] != 200):
    print("상태"," ".join(s[1:]))
    exit(1)



  a = headers.split(b'\r\n')[6]
  b = a.split()[1]
  c = int(b.decode())
  sum = 0

  # 퍼센테이지 출력해야뎀 sum에 더해서 총 값 받아줄거임

  print("Total Size",c,"bytes")
  print("Download Complete:",f"{serverName[3:][1]},",f"{sum}/{c}")



  # save image
  f = open('palladio.JPG', 'wb')
  f.write(image)
  f.close()

# 소켓 연결 종료
  # s.close()