
#main3에 yaw의 가중치까지 두어 동작시킴
#추후에 신속성 개선, 종료조건 추가할 것
import camera
import time
import math
from adafruit_servokit import ServoKit
def control_motor1(yawyaw,step):
    global angle1
    if yawyaw < -10:
        if angle1>115 :
            return
        angle1=angle1+step
        kit.servo[0].angle=angle1 
        time.sleep(0.1)
    elif yawyaw > 10 :
        if angle1<8 :
            return
        angle1=angle1-step
        kit.servo[0].angle=angle1 
        time.sleep(0.1)
           
    
        
def control_motor3(xx):
    global angle3
    if xx>340:
        if angle3>110 :
            return
        angle3=angle3+3
        kit.servo[6].angle=angle3  
        time.sleep(0.1)
    elif xx<300 :
        if angle3<10 :
            return
        angle3=angle3-3
        kit.servo[6].angle=angle3  
        time.sleep(0.1)           
      
        
def control_motor2(pitchpitch):
    global angle2
    if pitchpitch>30:
        if angle2<15 :
            return
        angle2=angle2-3
        kit.servo[3].angle=angle2 
        time.sleep(0.1)
    elif pitchpitch<-30 :
        if angle2>105 :
            return
        angle2=angle2+3
        kit.servo[3].angle=angle2 
        time.sleep(0.1)        

def control_motor4(rollroll,step):
    global angle4
    if rollroll<-3 :
        if angle4<5 :
            return
        angle4=angle4-step
        kit.servo[9].angle=angle4 
        time.sleep(0.1)
    elif rollroll>3 :
        if angle4>115 :
            return
        angle4=angle4+step
        kit.servo[9].angle=angle4 
        time.sleep(0.1)        
def setting_dir_pos(roll_pitch_yaw) :
    global roll, pitch, yaw, x, y, img
    roll = roll_pitch_yaw[0]
    pitch = roll_pitch_yaw[1]
    yaw = roll_pitch_yaw[2]
    x=roll_pitch_yaw[3]
    y=roll_pitch_yaw[4]
   # print(roll_pitch_yaw)  
 
            
#set channel
kit = ServoKit(channels=16)
angle1=60
angle2=80
angle3=60
angle4=60
#set initial pos
kit.servo[0].angle=60
kit.servo[3].angle=80
kit.servo[6].angle=60
kit.servo[9].angle=60
time.sleep(3)
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
    
    if abs(yaw)>10 or abs(x-320)>20 or abs(y-240)>30 or abs(roll)>3:
        while (1) :
            
            if abs(yaw)>40 :
                
                control_motor1(yaw,10)
                roll_pitch_yaw = camera.capture_axis()
                setting_dir_pos(roll_pitch_yaw)
            elif abs(yaw)>20 :
                
                control_motor1(yaw,6)
                roll_pitch_yaw = camera.capture_axis()
                setting_dir_pos(roll_pitch_yaw)
            else :
                control_motor1(yaw,3)
                roll_pitch_yaw = camera.capture_axis()
                setting_dir_pos(roll_pitch_yaw)
                
            control_motor3(x)
            roll_pitch_yaw = camera.capture_axis()
            setting_dir_pos(roll_pitch_yaw)
  
       
            control_motor2(pitch)
            roll_pitch_yaw = camera.capture_axis()
            setting_dir_pos(roll_pitch_yaw)

            if abs(roll)>20 :
                
                control_motor4(roll,9)
                roll_pitch_yaw = camera.capture_axis()
                setting_dir_pos(roll_pitch_yaw)
            elif abs(roll)>10 :
                
                control_motor4(roll,5)
                roll_pitch_yaw = camera.capture_axis()
                setting_dir_pos(roll_pitch_yaw)
            else :
                control_motor4(roll,1)
                roll_pitch_yaw = camera.capture_axis()
                setting_dir_pos(roll_pitch_yaw)
    #print("hi")
    print(roll)        
# cap.release()

