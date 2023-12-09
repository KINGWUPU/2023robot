import camera
import serial
import time
import math

def control_motor1(yawyaw):
    global angle1,angle2,angle3,angle4
    if yawyaw > 10:
        if angle1>115 :
            return
        angle1=angle1-5
    elif yawyaw < -10 :
        if angle1<5 :
            return
        angle1=angle1+5
            
    message= str(angle1)+','+str(angle2)+','+str(angle3)+','+str(angle4)
    print(message.encode())
    ser.write(message.encode())
    while(1) :
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        
        print(received_data)
        if received_data=='Done':
            break
        
def control_motor3(xx):
    global angle1,angle2,angle3,angle4
    if xx>340:
        if angle3>110 :
            return
        angle3=angle3+5
    elif xx<300 :
        if angle3<10 :
            return
        angle3=angle3-5
            
    message= str(angle1)+','+str(angle2)+','+str(angle3)+','+str(angle4)
    print(message.encode())
    ser.write(message.encode())
    while(1) :
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        
        print(received_data)
        if received_data=='Done':
            break    
        
def control_motor2(pitchpitch):
    global angle1,angle2,angle3,angle4
    if pitchpitch>20:
        if angle2<10 :
            return
        angle2=angle2-5
    elif pitchpitch<-20 :
        if angle2>110 :
            return
        angle2=angle2+5
            
    message= str(angle1)+','+str(angle2)+','+str(angle3)+','+str(angle4)
    print(message.encode())
    ser.write(message.encode())
    while(1) :
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        
        print(received_data)
        if received_data=='Done':
            break 
 
def setting_dir_pos(roll_pitch_yaw) :
    global roll, pitch, yaw, x, y, img
    roll = roll_pitch_yaw[0]
    pitch = roll_pitch_yaw[1]
    yaw = roll_pitch_yaw[2]
    x=roll_pitch_yaw[3]
    y=roll_pitch_yaw[4]
    print(roll_pitch_yaw)  
    # gogoimg()
             
def gogoimg() :
    from camera import img
        
    while True:
        # 전역 이미지가 있을 경우에만 imshow()를 통해 보여줌
        if img is not None:
            camera.cv2.imshow('img', img)
            # camera.cv2.imwrite('img', img)
            img=None
        # q 키를 누르면 종료
        k = camera.cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
        if camera.cv2.waitKey(1) & 0xFF == ord('q'):
            camera.cv2.destroyAllWindows()
            break
    
    return 0


# serial setting
serial_port='/dev/ttyUSB0' #포트 정보
baud_rate = 9600 #arduino와 일치 시킬것
ser = serial.Serial(serial_port,baud_rate)

angle1=60
angle2=80
angle3=60
angle4=60

global img
img=None

roll_pitch_yaw = camera.capture_axis()

roll = roll_pitch_yaw[0]
pitch = roll_pitch_yaw[1]
yaw = roll_pitch_yaw[2]
x=roll_pitch_yaw[3]
y=roll_pitch_yaw[4]

print(roll_pitch_yaw)

while(1) :
    # jj=input("cap?")
    roll_pitch_yaw = camera.capture_axis()
    # camera.cv2.imshow('img', image)
    setting_dir_pos(roll_pitch_yaw)
    
    if abs(yaw)>15 :
        while (1) :
            # jj=input("before 1")
            control_motor1(yaw)
            roll_pitch_yaw = camera.capture_axis()
            
            setting_dir_pos(roll_pitch_yaw)
            # jj=input("before 3")
            control_motor3(x)
            roll_pitch_yaw = camera.capture_axis()
            
            setting_dir_pos(roll_pitch_yaw)
            if abs(yaw)<20 and abs(x-320)<40 :
                print('1,3 terminate')
                break
            
            # face tracking fail
            if abs(yaw)==0 and abs(x)==0:
                print('1,3 terminate')
                break
            
        if abs(y-240)>30 : 
            while (1):
                 jj=input("before 2")
                 control_motor2(pitch)
                 roll_pitch_yaw = camera.capture_axis()
                 #ㅇ
                 setting_dir_pos(roll_pitch_yaw)
                 if abs(pitch)<20 :
                     print('2 terminate')
                     break
    print("hi")
            
# cap.release()

