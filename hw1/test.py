import socket

def download_image(save_path):
    # URL에서 호스트와 경로 추출
    host = "netapp.cs.kookmin.ac.kr"
  
    # 소켓 생성
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 서버에 연결
    s.connect((host, 80))
    
    # HTTP 요청 생성
    request = "GET /member/palladio.JPG HTTP/1.0\nHost: netapp.cs.kookmin.ac.kr\nUser-agent: HW1/1.0\nConnection: close\n"
    
    # 요청 전송
    s.send(request.encode())
    
    # 응답 받기
    response = b""
    while True:
        data = s.recv(1024)
        print(data)
        if not data:
            break
            print("아무것도없음")
        response += data
        print(response)
      
    
    # 응답 분석하여 헤더와 본문 분리
    header, body = response.split(b'\r\n\r\n', 1)
    
    # 헤더에서 Content-Length 추출
    content_length = None
    for line in header.split(b'\r\n'):
        if line.startswith(b'Content-Length'):
            content_length = int(line.split(b': ')[1])
    
    # 본문에서 이미지 데이터 추출
    image_data = body[:content_length]
    
    # 이미지 데이터 저장
    with open(save_path, 'wb') as f:
        f.write(image_data)
    
    # 소켓 연결 종료
    s.close()

# 이미지 다운로드
save_path = "palladio.jpg"
download_image(save_path)

