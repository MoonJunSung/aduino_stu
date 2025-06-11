import cv2
import numpy as np
from urllib.request import urlopen
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = '192.168.137.187'
stream = urlopen('http://' + ip +':81/stream')
buffer = b''
urlopen('http://' + ip + "/action?go=speed40")

if os.path.isdir('01_go') is False:
    os.mkdir("01_go")

if os.path.isdir('02_left') is False:
    os.mkdir("02_left")

if os.path.isdir('03_right') is False:
    os.mkdir("03_right")

go_cnt = 0
left_cnt = 0
right_cnt = 0
car_state = 'stop'
while True:
    buffer += stream.read(4096)
    #print(buffer)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    
    try: #가끔 비어있는 버퍼를 받아 오류가 발생함. 이를 위한 try문
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            # 아래부분의 반만 자르기
            height, width, _ = img.shape
            img = img[height // 2:, :]

            # 크기 조절
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

            cv2.imshow("AI CAR Streaming", img)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('w'):
                car_state = 'go'
                print('전진')
                urlopen('http://' + ip + "/action?go=backward")
            elif key == ord('a'):
                car_state = 'left'
                print('왼쪽')
                urlopen('http://' + ip + "/action?go=left")
            elif key == ord('d'):
                car_state = 'right'
                print('오른쪽')
                urlopen('http://' + ip + "/action?go=right")
            elif key == 32: #space key
                car_state = 'stop'
                print('멈춤')
                urlopen('http://' + ip + "/action?go=stop")

            if car_state == 'go':
                print("직진 저장")
                cv2.imwrite(f'01_go/go_{go_cnt}.png',img)
                go_cnt = go_cnt + 1
            elif car_state == 'left':
                print("왼쪽 저장")
                cv2.imwrite(f'02_left/left_{left_cnt}.png',img)
                left_cnt = left_cnt + 1
            elif car_state == 'right':
                print("오른쪽 저장")
                cv2.imwrite(f'03_right/right_{right_cnt}.png',img)
                right_cnt = right_cnt + 1

    except:
        print("에러")
        pass

urlopen('http://' + ip + "/action?go=stop")
cv2.destroyAllWindows()

# main4-1-2.py
# 주행이미지 저장하기