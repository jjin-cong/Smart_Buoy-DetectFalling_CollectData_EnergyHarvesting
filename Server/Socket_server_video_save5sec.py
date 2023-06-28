import cv2
import socket
import struct
import numpy as np
import datetime
import keyboard

# 서버 정보
server_ip = '172.20.10.4'  # 서버 IP 주소
server_port = 50002  # 서버 포트 번호
buffer_size = 65535  # 버퍼 크기 (UDP 최대 크기로 설정)
packet_size = 40000

#영상 정보
fps = 30
output_width = 640  
output_height = 480


# UDP 소켓 생성
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((server_ip, server_port))

# 동영상 저장 생성자
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

# 화면 생성
#cv2.namedWindow('Received Video', cv2.WINDOW_NORMAL)


while True:
    break_code = 'no'
    timer = 0

    # 이미지 저장, 표시
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output_{current_time}.mp4"

    # VideoWriter 초기화
    out = cv2.VideoWriter(output_file, fourcc, fps, (output_width, output_height))

    while timer < (5 * int(fps)) : #5sec * fps
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
            #cv2.imshow('Received Video', frame)    
            # 프레임 저장
            out.write(frame)
            
            # 타이머 업데이트
            timer = timer + 1  # 5초마다 저장
            #print(timer)
        
        # 'q' 키를 누르면 종료
        if keyboard.is_pressed('q'):
            break_code = 'yes'
            break

        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break_code = 'yes'
            #break
        
    # 'q' 키를 누르면 종료
    if break_code == 'yes':
        break

# 종료 시 리소스 해제
udp_socket.close()
cv2.destroyAllWindows()