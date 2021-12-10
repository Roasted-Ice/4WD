#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24

#RGB三色灯设置为输出模式
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

#超声波引脚定义
EchoPin = 0
TrigPin = 1

#红外避障引脚定义
AvoidSensorLeft = 12
AvoidSensorRight = 17

#速度定义
leftspeed = 60
rightspeed = 60

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化为输出模式
#按键引脚初始化为输入模式
def init():
    global pwm_ENA
    global pwm_ENB
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #红外避障引脚初始化为输入模式
    GPIO.setup(AvoidSensorLeft,GPIO.IN)
    GPIO.setup(AvoidSensorRight,GPIO.IN)
    #超声波引脚初始化
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)
    #设置pwm引脚和频率为2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

#小车前进

def run():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车后退
def back():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车左转
def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(0)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车右转
def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(0)

#小车原地左转
def spin_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车原地右转
def spin_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车停止
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

#超声波测距函数
def Distance():
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
    t1 = time.time()
    while GPIO.input(EchoPin):
        pass
    t2 = time.time()
    print ("distance is %d " % (((t2 - t1)* 340 / 2) * 100))
    time.sleep(0.01)
    return ((t2 - t1)* 340 / 2) * 100

#try/except语句用来检测try语句块中的错误，
#从而让except语句捕获异常信息并处理。
try:
    init()
    while True:
        #遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
        #未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
        LeftSensorValue  = GPIO.input(AvoidSensorLeft);
        RightSensorValue = GPIO.input(AvoidSensorRight);

        if LeftSensorValue == True and RightSensorValue == True :
            run()         #当两侧均未检测到障碍物时调用前进函数
        elif LeftSensorValue == True and RightSensorValue == False :
            spin_left()   #右边探测到有障碍物，有信号返回，原地向左转
            time.sleep(0.002)
        elif RightSensorValue == True and LeftSensorValue == False:
            spin_right()  #左边探测到有障碍物，有信号返回，原地向右转
            time.sleep(0.002)
        elif RightSensorValue == False and LeftSensorValue == False :
            spin_right()  #当两侧均检测到障碍物时调用固定方向的避障(原地右转)
            time.sleep(0.002)
        while True:
            distance = Distance()
            if distance > 50:
                    run()
            elif 30 <= distance <= 50:
                run()      #当快靠近障碍物时慢速前进
            elif distance < 30:
                spin_right()
                time.sleep()  #当靠近障碍物时原地右转大约90度
                brake()
                time.sleep(0.001)
                distance = Distance()  #再次测试判断前方距离
            if distance >= 30:
                run()         #转弯后当前方距离大于25cm时前进
            elif distance < 30:
                spin_left()
                time.sleep(0.6)    #转弯后前方距离小于25cm时向左原地转弯180度
                brake()
                time.sleep(0.001)
                distance = Distance() #再次测试判断前方距离
                if distance >= 30:
                    run()            #转弯后当前方距离大于25cm时前进
                elif distance < 30:
                    spin_left()    #转弯后前方距离小于25cm时向左原地转弯90度
                    time.sleep(0.3)
                    brake()
                    time.sleep(0.001)

except KeyboardInterrupt:
    pass
pwm_ENA.stop()

pwm_ENB.stop()

GPIO.cleanup()
