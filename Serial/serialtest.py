#arduino - Rpi serial testfile
#포트 확인 명령어 - ls /dev/tty*   // dev/ttyUSB0 <- 보통 이건데 안되면 확인하기

import serial
import time
serial_port='/dev/ttyUSB0' #포트 정보
baud_rate = 9600 #arduino와 일치 시킬것

#port 열기

ser = serial.Serial(serial_port,baud_rate)

while True :
    message=input('input some text :')
    ser.write(message.encode()) #문자열을 바이트로 인코드
    
    while True :
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        print("Recieved :" ,received_data)
        if received_data=='Done':
           break
    