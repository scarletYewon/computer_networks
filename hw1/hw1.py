import socket
import select

print("Student ID : 20213047")
print("Name : Yewon Lee")

while (1): 
  # 소켓생성
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = 80
  # 입력 받는곳
  data = input("> ").split()
  # down이면
  if (data[0] == "down"):
    serverName = data[1].split("/")

    # 숫자처리
    numSN = serverName[2]
    for i in numSN:
      if (i.isnumeric()):
        numSN = ''.join(char for char in numSN if not char.isnumeric())
        numSN = numSN[:-1]
        break
    
    serverName[2] = numSN

    print(numSN)

    # 소켓연결
    try :
      serverIp = socket.gethostbyname(serverName[2])
      s.connect((serverIp, port))
  
    # 에러처리
    except socket.gaierror :
      print(f"{serverName[2]}: unknown host")
      print("cannot connect to server",serverName[2],port,"\r\n")
      continue

    if (serverName[0] != "http:"):
      print("Only Support http, not", serverName[0][:-1],"\r\n")
      continue

    # 요청보내기
    msg = "GET /{} HTTP/1.0\r\nHost: {}\r\nUser-agent: HW1/1.0\r\nConnection: close\r\n\r\n".format("/".join(serverName[3:]), serverName[2])
    print(msg)
    s.send(msg.encode())

  # quit이면
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

  # 상태코드에 따른 에러처리
  sCode = headers.split(b'\r\n')[0].decode()
  status = sCode.split()
  if (int(status[1]) != 200):
    print(" ".join(status[1:]),"\r\n")
    continue



  a = headers.split(b'\r\n')[6]
  b = a.split()[1]
  total = int(b.decode())
  sum = 0

  # 퍼센테이지 출력해야뎀 sum에 더해서 총 값 받아줄거임


  # 마지막 출력
  print("Total Size",total,"bytes")
  print("Download Complete:",f"{serverName[3:][1]},",f"{sum}/{total}","\r\n")

  # save image
  f = open('palladio.JPG', 'wb')
  f.write(image)
  f.close()

# 소켓 연결 종료
  s.close()