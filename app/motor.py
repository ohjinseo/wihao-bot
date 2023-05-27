import RPi.GPIO as GPIO
import time
import lidar

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 핀 번호 할당
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22
ENA = 23
ENB = 24

IN5 = 25
IN6 = 12
IN7 = 16
IN8 = 20
ENC = 21
END = 26

# 핀 초기화
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(IN5, GPIO.OUT)
GPIO.setup(IN6, GPIO.OUT)
GPIO.setup(IN7, GPIO.OUT)
GPIO.setup(IN8, GPIO.OUT)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(ENC, GPIO.OUT)
GPIO.setup(END, GPIO.OUT)
 
# PWM 초기화
pwm1 = GPIO.PWM(ENA, 50)
pwm1.start(50)
pwm2 = GPIO.PWM(ENB, 50)
pwm2.start(50)
pwm3 = GPIO.PWM(ENC, 50)
pwm3.start(50)
pwm4 = GPIO.PWM(END, 50)
pwm4.start(50)

def forward():
    # 전진
    pwm1.ChangeDutyCycle(10)    # 오른쪽 뒷바퀴
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    
    pwm2.ChangeDutyCycle(10)    # 왼쪽 뒷바퀴
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    
    pwm3.ChangeDutyCycle(20)    # 왼쪽 앞바퀴
    GPIO.output(IN5, True)
    GPIO.output(IN6, False)
    
    pwm4.ChangeDutyCycle(20)    # 오른쪽 앞바퀴
    GPIO.output(IN7, True)
    GPIO.output(IN8, False)

def backward():
    # 후진
    pwm1.ChangeDutyCycle(10)    # 오른쪽 뒷바퀴
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    
    pwm2.ChangeDutyCycle(10)    # 왼쪽 뒷바퀴
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    
    pwm3.ChangeDutyCycle(20)    # 왼쪽 앞바퀴
    GPIO.output(IN5, False)
    GPIO.output(IN6, True)
    
    pwm4.ChangeDutyCycle(20)    # 오른쪽 앞바퀴
    GPIO.output(IN7, False)
    GPIO.output(IN8, True)

def turn_left():
    # 좌회전
    pwm1.ChangeDutyCycle(0)    # 오른쪽 뒷바퀴
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    
    pwm2.ChangeDutyCycle(10)    # 왼쪽 뒷바퀴
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    
    pwm3.ChangeDutyCycle(20)    # 왼쪽 앞바퀴
    GPIO.output(IN5, False)
    GPIO.output(IN6, True)
    
    pwm4.ChangeDutyCycle(20)    # 오른쪽 앞바퀴
    GPIO.output(IN7, True)
    GPIO.output(IN8, False)

def turn_right():
    # 우회전
    pwm1.ChangeDutyCycle(10)    # 오른쪽 뒷바퀴
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    
    pwm2.ChangeDutyCycle(0)    # 왼쪽 뒷바퀴
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    
    pwm3.ChangeDutyCycle(20)    # 왼쪽 앞바퀴
    GPIO.output(IN5, True)
    GPIO.output(IN6, False)
    
    pwm4.ChangeDutyCycle(20)    # 오른쪽 앞바퀴
    GPIO.output(IN7, False)
    GPIO.output(IN8, True)

def stop():
    # 모든 모터 정지
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
    GPIO.output(IN5, False)
    GPIO.output(IN6, False)
    GPIO.output(IN7, False)
    GPIO.output(IN8, False)
        
def obstacle_avoidance():
    while True:
        distance = lidar.read_data()
        
        while distance < 30:
            stop()
            distance = lidar.read_data()
            if distance > 30:
                break
            
        forward()
        distance = lidar.read_data()
        if distance < 30:           # 장애물 감지
            print("Detected!!")            
            stop()                  # 1초 정지
            time.sleep(1)
            
            turn_left()             # 2초 동안 좌회전 (대략 45도)
            time.sleep(1)
            
            distance = lidar.read_data() # 거리값 다시 받고
            if distance > 30:       # 장애물이 없음
                forward()           # 1초동안 앞으로 전진
                time.sleep(2)
                
                turn_right()        # 2초동안 우회전 (정면)
                time.sleep(1)
                forward()
                time.sleep(3)       # 3초 앞으로 전진
                
                turn_right()        # 2초동안 우회전
                time.sleep(1)
                forward()           # 전진 (원위치)
                time.sleep(3)
                
                turn_left()         # 원위치 정면
                time.sleep(1)
            else:
                turn_right()
                time.sleep(4)
                
                distance = lidar.read_data()
                if distance > 30:       # 장애물이 없음
                    forward()           # 앞으로 1초 전진
                    time.sleep(1)
                    
                    turn_left()         # 2초동안 좌회전 (정면)
                    time.sleep(2)
                    forward()           # 3초 동안 전진
                    time.sleep(3)       
                    
                    turn_left()         # 2초동안 좌회전
                    time.sleep(2)
                    forward()           # 전진 (원위치)
                    time.sleep(1)
                    
                    turn_right()         # 원위치 정면
                    time.sleep(2)
                else:
                    distance = lidar.read_data()
                    while distance < 30:
                        stop()
                        print("Block!!")

def main():
    try:
        # 초기화 및 설정 코드

        obstacle_avoidance()

    except KeyboardInterrupt:
            stop()

    # 정리 코드

if __name__ == "__main__":
    main()

GPIO.cleanup()
