import RPi.GPIO as GPIO

# GPIO 핀 설정
IN1 = 17
IN2 = 18
ENA = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)

def motor_control(on: bool):
    if on:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(50)
        print("모터 ON (50%)")
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(0)
        print("모터 OFF")