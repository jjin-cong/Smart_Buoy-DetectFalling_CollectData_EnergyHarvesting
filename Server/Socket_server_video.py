import cv2
import socket
import struct
import numpy as np
import datetime

# 서버 정보
server_ip = '10.1.0.8'  # 서버 IP 주소
server_port = 50001  # 서버 포트 번호
buffer_size = 65535  # 버퍼 크기 (UDP 최대 크기로 설정)
packet_size = 40000

# UDP 소켓 생성
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((server_ip, server_port))

# 동영상 저장 생성자
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output_v4.avi',fourcc,20.0,(640,480))

# 화면 생성
cv2.namedWindow('Received Video', cv2.WINDOW_NORMAL)

while True:
    # 데이터 수신
    data, addr = udp_socket.recvfrom(buffer_size)

    # 수신된 데이터에서 프레임 크기 얻기
    length = struct.unpack('>L', data[:4])[0]

    # 데이터에서 프레임 추출
    frame_data = data[4:]

    # 데이터 재조립
    while len(frame_data) == packet_size:
        data, _ = udp_socket.recvfrom(buffer_size)
        frame_data += data[4:] #갱신이 되어야 함

    # 프레임 디코딩
    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    # 프레임이 유효한지 확인
    if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
        # 이미지 저장, 표시
        out.write(frame)
        cv2.imshow('Received Video', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 시 리소스 해제
udp_socket.close()
cv2.destroyAllWindows()
