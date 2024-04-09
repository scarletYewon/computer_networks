import socket
import select

print("Student ID : 20213047")
print("Name : Yewon Lee\n")

while (True):
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
      print("Only support http, not", serverName[0][:-1],"\r\n")
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
  cnt = 0
  tmp = 0
  while select.select([s],[],[],3)[0]:
    d = s.recv(1024)
    if not d:
      break
    # 전체값 찾기
    response+=d
    headers = response.split(b'\r\n\r\n')[0]

    # 상태코드에 따른 에러처리
    st=0
    sCode = headers.split(b'\r\n')[0].decode()
    status = sCode.split()
    if (int(status[1]) != 200):
      print(" ".join(status[1:]),"\r\n\r\n")
      st+=1
      break

    # 전체값 찾기
    if tmp < 1:
      for i in headers.split(b'\r\n'):
        if i.startswith(b'Content-Length:'):
          total = int(i.split(b':')[1])
          print("Total Size",total,"bytes")
          tmp+=1
          break

    # 10퍼마다 출력하기
    data = response[len(headers)+4:]
    progress = len(data)
    if (progress/total)*100 > cnt+10:
      print(f"Current Downloading {progress}/{total} (bytes) {(progress/total)*100:.0f}%",end="\n")
      cnt+=10
    elif (progress/total)*100 ==100:
      print(f"Current Downloading {progress}/{total} (bytes) {(progress/total)*100:.0f}%",end="\n")

  # 200이 아니면 처리
  if st==1:
    continue

  # headers =  response.split(b'\r\n\r\n')[0]
  image = response[len(headers)+4:]

  # # 상태코드에 따른 에러처리
  # sCode = headers.split(b'\r\n')[0].decode()
  # status = sCode.split()
  # if (int(status[1]) != 200):
  #   print(" ".join(status[1:]),"\r\n")
  #   continue

  # 마지막 출력
  print("Download Complete:",f"{serverName[-1]},",f"{progress}/{total}","\r\n")

  # save image
  f = open(serverName[-1], 'wb')
  f.write(image)
  f.close()
  # 소켓 연결 종료
  s.close()