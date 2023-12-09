from adafruit_servokit import ServoKit
import time

#set channel
kit = ServoKit(channels=16)

# kit.servo[0].set_pulse_width_range(1000, 2000)
# kit.servo[3].set_pulse_width_range(1000, 2000)
# kit.servo[6].set_pulse_width_range(1000, 2000)

#코드 상에서는 0~180 -> 실제로는 0~120.
#내가 실제로 10도 돌리려면 코드 상에서는 15의 차이를 줘야함
#회전 방향은 아두이노 때랑 동일하다
a1=90
a2=120
a3=90
a4=90
kit.servo[0].angle=90
kit.servo[3].angle=120
kit.servo[6].angle=90
kit.servo[9].angle=90
while(1) :
    stst = input("Enter angles (separated by commas): ")

# 입력된 문자열을 쉼표로 분리
    angles = stst.split(',')

# 분리된 각 값을 개별 변수에 할당
    a1, a2, a3, a4 = [int(angle) for angle in angles]
    kit.servo[0].angle=a1
    kit.servo[3].angle=a2
    kit.servo[6].angle=a3
    kit.servo[9].angle=a4
    time.sleep(2)
    