import math
import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[0].angle=130
kit.servo[3].angle=80
kit.servo[6].angle=60
kit.servo[9].angle=60
time.sleep(3)