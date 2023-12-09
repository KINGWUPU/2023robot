#arduino - Rpi serial testfile
#포트 확인 명령어 - ls /dev/tty*   // dev/ttyUSB0 <- 보통 이건데 안되면 확인하기

import serial
import time
serial_port='/dev/ttyUSB0' #포트 정보
baud_rate = 9600 #arduino와 일치 시킬것

#port 열기

ser = serial.Serial(serial_port,baud_rate)
angles=80
while True :
    
    message=str(angles)

    message=message+'\n'
    print(message)
    ser.write(message.encode()) #문자열을 바이트로 인코드
   # time.sleep(0.1)
   # print("g")
    received_data=ser.readline().decode().strip() 
    print("dd")
    angles=angles+1
    if angles<120 :
        angles=60