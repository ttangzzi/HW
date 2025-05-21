# import RPi.GPIO as GPIO
# import time
# from evdev import InputDevice, ecodes
# import select
# import sys

# # ==== GPIO 핀 설정 ====
# IN1 = 17
# IN2 = 18
# ENA = 22  # PWM 핀

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(IN1, GPIO.OUT)
# GPIO.setup(IN2, GPIO.OUT)
# GPIO.setup(ENA, GPIO.OUT)

# pwm = GPIO.PWM(ENA, 1000)  # 1kHz
# pwm.start(0)  # 초기 정지 상태

# def motor_control(on: bool):
#     if on:
#         GPIO.output(IN1, GPIO.HIGH)
#         GPIO.output(IN2, GPIO.LOW)
#         pwm.ChangeDutyCycle(50)  # 50% 속도로 전진
#         print("모터 ON (25%)")
#     else:
#         GPIO.output(IN1, GPIO.LOW)
#         GPIO.output(IN2, GPIO.LOW)
#         pwm.ChangeDutyCycle(0)
#         print("모터 OFF")


# # ==== evdev로 버튼 입력 받기 ====
# DEVICE_PATH = "/dev/input/event2"
# dev = InputDevice(DEVICE_PATH)
# print("장치 연결 완료")

# state = False  # 모터 상태 on/off

# print("버튼을 누르면 on/off 전환됨 | 'q' 입력 시 종료")

# try:
#     while True:
#         r, _, _ = select.select([dev, sys.stdin], [], [])

#         for source in r:
#             if source == sys.stdin:
#                 key = sys.stdin.readline().strip()
#                 if key.lower() == 'q':
#                     print("종료")
#                     raise KeyboardInterrupt

#             try:
#                 event = dev.read_one()
#             except OSError:
#                 print("장치 오류: 연결이 끊김 또는 제거됨")
#                 raise KeyboardInterrupt

#             if event and event.type == ecodes.EV_KEY and event.code == ecodes.KEY_VOLUMEUP and event.value == 1:
#                 state = not state
#                 print("on" if state else "off")
#                 motor_control(state)

# except KeyboardInterrupt:
#     print("종료 처리 중...")
#     pwm.stop()
#     GPIO.cleanup()
#     dev.close()
#     sys.exit(0)


import RPi.GPIO as GPIO
import time
from evdev import InputDevice, ecodes
import select
import sys

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

# 블루투스 버튼 장치 경로
DEVICE_PATH = "/dev/input/event2"  # 실제 연결된 장치 번호로 확인
dev = InputDevice(DEVICE_PATH)
print("장치 연결 완료")

state = False  # 모터 상태
last_event_time = 0
debounce_delay = 0.3  # 0.3초 내 중복 입력 무시

print("버튼 누르면 ON/OFF 전환 | 'q' 입력 시 종료")

try:
    while True:
        r, _, _ = select.select([dev, sys.stdin], [], [])

        for source in r:
            if source == sys.stdin:
                key = sys.stdin.readline().strip()
                if key.lower() == 'q':
                    raise KeyboardInterrupt

            elif source == dev:
                events = dev.read()
                for event in events:
                    if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_VOLUMEUP and event.value == 1:
                        now = time.time()
                        if now - last_event_time < debounce_delay:
                            continue
                        last_event_time = now

                        state = not state
                        motor_control(state)

except KeyboardInterrupt:
    print("종료 처리 중...")
    pwm.stop()
    GPIO.cleanup()
    dev.close()
    sys.exit(0)
