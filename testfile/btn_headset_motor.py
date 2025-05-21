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

# 블루투스 버튼 장치 경로
DEVICE_PATH = "/dev/input/event2"  # 실제 연결된 장치 번호로 확인
dev = InputDevice(DEVICE_PATH)
print("장치 연결 완료")

# 중복입력 무시처리
last_event_time = 0
delay = 0.5 # 0.5초 이내 중복 입력 무시하기

recording = None  # 녹음 상태 저장용

print("버튼을 누르면 on / off 전환됨 | 'p' 입력 시 재생 | 'q' 입력 시 종료")

while True:
    r, _, _ = select.select([dev, sys.stdin], [], [])

    for source in r:
        if source == sys.stdin:
            key = sys.stdin.readline().strip()
            # 대소문자 상관없이 q 키 감지 -> 종료
            if key.lower() == 'q':
                print("종료")
                dev.close()
                sys.exit(0)

            # 대소문자 상관없이 p 키 감지 -> 재생
            if key.lower() == 'p':
                print("파일 재생 중...")
                # plughw : 장치 번호 만약에 바뀌면 수정해줘야함
                subprocess.run(["aplay", "-D", "plughw:1,0", "out.wav"])

        try:
            # 이벤트를 읽어옴
            events = dev.read()
        except OSError:
            print("장치 오류 : 연결이 끊김 혹은 제거")
            sys.exit(1)
        
        for event in events:
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_VOLUMEUP and event.value == 1:
                state = not state
                current_time = time.time()
                if current_time - last_event_time < delay:
                    continue # delay 초 내 중복 입력은 무시
                last_event_time = current_time
            
                if recording is None or recording.poll() is not None:
                        print("녹음 시작")
                        try:
                            recording = subprocess.Popen([
                                # plughw : 장치 번호 만약에 바뀌면 수정해줘야함
                                "arecord", "-D", "plughw:1,0", "-f", "S16_LE", "-r", "16000", "-c", "1", "out.wav"
                            ])
                            motor_control(state)
                        except Exception as e:
                            print("녹음 시작 실패:", e)
                # None 상태가 아닌 경우 녹음 중지 -> recoding이 다시 None이 됨
                else:
                    print("녹음 중지")
                    recording.terminate()
                    recording = None
                    motor_control(state)