import cv2
import numpy as np 
from urllib.request import urlopen

ip = "192.168.137.190"
stream = urlopen('http://'+ ip + ':81/stream')
Buffer = b''

while True:
  Buffer += stream.read(4096)
  print(Buffer)