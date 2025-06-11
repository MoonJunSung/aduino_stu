import cv2
import numpy as np
from urllib.request import urlopen
import os

# 디렉토리 생성
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = '192.168.137.187'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''

# 속도 설정
urlopen('http://' + ip + '/action?go=speed40')

# 필요한 디렉토리 생성
if os.path.isdir('01_go') is False:
    os.mkdir('01_go')

if os.path.isdir('02_left') is False:
    os.mkdir('02_left')

if os.path.isdir('03_right') is False:
    os.mkdir('03_right')

car_state = 'stop'

while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    
    try:
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            
            # 이미지부분의 반만 자르기
            height, width, _ = img.shape
            img = img[height // 2:, :]
            
            # 크기 조정
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            
            cv2.imshow("AI CAR Streaming", img)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                urlopen('http://' + ip + '/action?go=stop')
                break
            elif key == ord('w'):
                car_state = 'go'
                print('직진')
                urlopen('http://' + ip + '/action?go=forward')
            elif key == ord('a'):
                car_state = 'left'
                print('왼쪽')
                urlopen('http://' + ip + '/action?go=left')
            elif key == ord('d'):
                car_state = 'right'
                print('오른쪽')
                urlopen('http://' + ip + '/action?go=right')
            elif key == 32:  # spacebar
                car_state = 'stop'
                print('멈춤')
                urlopen('http://' + ip + '/action?go=stop')
            
            # 이미지 저장
            if car_state == 'go':
                print("직진 이미지 저장")
                cv2.imwrite(f'01_go/go.png', img)
            elif car_state == 'left':
                print("왼쪽 이미지 저장")
                cv2.imwrite(f'02_left/left.png', img)
            elif car_state == 'right':
                print("오른쪽 이미지 저장")
                cv2.imwrite(f'03_right/right.png', img)
                
    except:
        print("에러")
        pass

urlopen('http://' + ip + '/action?go=stop')
cv2.destroyAllWindows()
