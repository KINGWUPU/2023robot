#Final main program
import camera
import time
import math
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit


def control_motor1(yawyaw,step):
    global angle1
    if yawyaw < -10:
        if angle1>109 :
            return
        angle1=angle1+step
        kit.servo[0].angle=angle1 
        time.sleep(0.1)
    elif yawyaw > 10 :
        if angle1<11 :
            return 
        angle1=angle1-step
        kit.servo[0].angle=angle1 
        time.sleep(0.1)
           
    
        
def control_motor3(xx):
    global angle3
    if xx>340:
        if angle3>110 :
            return
        angle3=angle3+5
        kit.servo[6].angle=angle3  
        time.sleep(0.1)
    elif xx<300 :
        if angle3<10 :
            return
        angle3=angle3-5
        kit.servo[6].angle=angle3  
        time.sleep(0.1)           
      
        
def control_motor2(yy):
    global angle2
    if yy>270:
        if angle2<15 :
            return
        angle2=angle2-1
        kit.servo[3].angle=angle2 
        time.sleep(0.1)
    elif yy<210 :
        if angle2>105 :
            return
        angle2=angle2+1
        kit.servo[3].angle=angle2 
        time.sleep(0.1)        

def control_motor4(rollroll,step):
    global angle4
    if rollroll<-3 :
        if angle4<10 :
            return
        angle4=angle4-step
        kit.servo[9].angle=angle4 
        time.sleep(0.1)
    elif rollroll>3 :
        if angle4>110 :
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
   
def switch_pressed():
    #print("setting pos!") 
    global angle1,angle2,angle3,angle4, roll, pitch,yaw,x,y
    if angle1<60 :
        d1=1
    elif angle1>60 :
        d1=-1
    else :
        d1=0
    if angle2<70 :
        d2=1
    elif angle2>70 :
        d2=-1
    else :
        d2=0
    if angle3<60 :
        d3=1
    elif angle3>60 :
        d3=-1
    else :
        d3=0
    if angle4<60 :
        d4=1
    elif angle4>60 :
        d4=-1
    else :
        d4=0
    while angle1!=60 or angle2!=70 or angle3!=60 or angle4!=60 :
    
        kit.servo[0].angle=angle1
        kit.servo[3].angle=angle2
        kit.servo[6].angle=angle3
        kit.servo[9].angle=angle4
        if angle1!=60 :
            angle1=angle1+d1
        if angle2!=70 :
            angle2=angle2+d2
        if angle3!=60 :    
            angle3=angle3+d3
        if angle4!=60 :
            angle4=angle4+d4
        time.sleep(0.1)
        #fprint("setting pos")
    
    roll=0
    pitch=0
    yaw=0
    x=320
    y=240
    time.sleep(3)
    while True :
        print("wait")
        if GPIO.input(switch_pin) == False:
            break 
    time.sleep(1)
    print("terminate setting")
try :
    switch_pin = 17 
    # GPIO 핀 설정
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 내부 풀업 저항 활성화   
    
       
    #set channel
    kit = ServoKit(channels=16)
    angle1=60
    angle2=70
    angle3=60
    angle4=60
    #set initial pos
    kit.servo[0].angle=60
    kit.servo[3].angle=70
    kit.servo[6].angle=60
    kit.servo[9].angle=60
    time.sleep(0.2)
    #waiting switch
    while True :
        if GPIO.input(switch_pin) == False:
            break  
    print("Press switch")
    time.sleep(2)  
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
        
        roll_pitch_yaw = camera.capture_axis()
        setting_dir_pos(roll_pitch_yaw)
        if GPIO.input(switch_pin) == False: # 스위치가 눌렸을 때
            switch_pressed()
        if abs(yaw)>10 or abs(x-320)>20 or abs(y-240)>30 or abs(roll)>3:
            while (1) :
                if GPIO.input(switch_pin) == False: # 스위치가 눌렸을 때
                    switch_pressed()
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
    
        
                control_motor2(y)
                roll_pitch_yaw = camera.capture_axis()
                setting_dir_pos(roll_pitch_yaw)

                if abs(roll)>20 :
                    
                    control_motor4(roll,9)
                    roll_pitch_yaw = camera.capture_axis()
                    setting_dir_pos(roll_pitch_yaw)
                elif abs(roll)>10 :
                    
                    control_motor4(roll,6)
                    roll_pitch_yaw = camera.capture_axis()
                    setting_dir_pos(roll_pitch_yaw)
                else :
                    control_motor4(roll,3)
                    roll_pitch_yaw = camera.capture_axis()
                    setting_dir_pos(roll_pitch_yaw)
        
        print(roll)        
    

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()