# 사전에 evdev 라이브러리 설치

from evdev import InputDevice, ecodes
import subprocess
import select
import sys
import time

# YOITCH Snapshot 버튼 디바이스 경로
# 실제로 블루투스 버튼 연결 시 event3 라는것이 생기는것 확인인
DEVICE_PATH = "/dev/input/event3"

# 장치 열기
dev = InputDevice(DEVICE_PATH)
print("장치 연결 완료")

recording = None  # 녹음 상태 저장용

# 중복입력 무시처리
last_event_time = 0
delay = 0.5 # 0.5초 이내 중복 입력 무시하기

print("버튼을 누르면 on / off 전환됨 | 'p' 입력 시 재생 | 'q' 입력 시 종료")

while True:
    # 굳이 select.select() 함수 사용하는 이유 : 입력 실제 발생할 때까지 기다리는 함수라서
    # input도 가능은 하지만 그건 "키보드 입력"일때만. 우리는 "이벤트 입력"을 기다림
    # select.select() 함수는 무조건 3가지 인자를 요구함
    # 따라서 2,3번째 리스트는 빈 리스트라도 줘야함
    # 즉, r = select.select([dev, sys.stdin]) 으로 생각해도 됨
    r, _, _ = select.select([dev, sys.stdin], [], [])

    for source in r:
        # sys.stdin : 콘솔에서 키보드 입력 받을 때 연결되는 표준 입력 스트림
        # readline().strip() : 줄바꿈 포함해서 sys.stdin을 읽어오는 함수
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
                subprocess.run(["aplay", "out.wav"])

        # dev는 evdev를 통해 연 입력장치 (블루투스) 의미
        # Snapshot 버튼 이벤트 처리
        try:
            # 하나의 이벤트를 읽어옴 = 볼륨 업
            event = dev.read_one()
        except OSError:
            print("장치 오류 : 연결이 끊김 혹은 제거")
            sys.exit(1)

        # 이벤트가 비어있지(None) 않고, 타입이 EV_KEY, 코드가 KEY_VOLUMEUP(볼륨업)이며
        # 이벤트 값이 1 = 버튼이 눌림을 나타냄
        if event and event.type == ecodes.EV_KEY and event.code == ecodes.KEY_VOLUMEUP and event.value == 1:
            # 토글 기능 : on 상태면 off로, off 상태면 on으로

            current_time = time.time()
            if current_time - last_event_time < delay:
                continue # delay 초 내 중복 입력은 무시
            last_event_time = current_time
            
            if recording is None or recording.poll() is not None:
                    print("녹음 시작")
                    try:
                        recording = subprocess.Popen([
                            "arecord", "-D", "plughw:1,0", "-f", "S16_LE", "-r", "16000", "-c", "1", "out.wav"
                        ])
                    except Exception as e:
                        print("녹음 시작 실패:", e)
            # None 상태가 아닌 경우 녹음 중지 -> recoding이 다시 None이 됨
            else:
                print("녹음 중지")
                recording.terminate()
                recording = None
