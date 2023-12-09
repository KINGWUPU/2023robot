#arduino - Rpi serial testfile
#포트 확인 명령어 - ls /dev/tty*   // dev/ttyUSB0 <- 보통 이건데 안되면 확인하기

import serial
import time
serial_port='/dev/ttyUSB0' #포트 정보
baud_rate = 9600 #arduino와 일치 시킬것
angle1=60
angle2=60
angle3=60
angle4=60
#port 열기

flag=1
ser = serial.Serial(serial_port,baud_rate)
time.sleep(2) #시리얼 통신 연결 제대로 될때까지 대기하자
while True :
    #message=input('input some text :')
    #print(message.encode())
    if flag==1 :
        angle1=angle1-5
        if angle1<40 :
            flag=0
    if flag==0 :
        angle1=angle1+5
        if angle1>80 :
            flag=1
    
    message= str(angle1)+','+str(angle2)+','+str(angle3)+','+str(angle4)
    print(message.encode())
    ser.write(message.encode()) #문자열을 바이트로 인코드
    
    print('send')
    while True :
        print('here')
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        
        print(received_data)
        if received_data=='Done':
            break
     