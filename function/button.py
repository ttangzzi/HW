# 사전에 evdev 라이브러리 설치

from evdev import InputDevice, ecodes
import select
import sys

# YOITCH Snapshot 버튼 디바이스 경로
DEVICE_PATH = "/dev/input/event3"

# 장치 열기
dev = InputDevice(DEVICE_PATH)
print(f"장치 연결됨: {dev.name} ({dev.path})")

state = False  # ON/OFF 상태

print("▶ Snapshot 버튼을 누르면 on / off 전환됨 | 'q' 입력 시 종료")

while True:
    r, _, _ = select.select([dev, sys.stdin], [], [])

    for source in r:
        # q 키 감지
        if source == sys.stdin:
            key = sys.stdin.readline().strip()
            if key.lower() == 'q':
                print("🚪 종료합니다.")
                dev.close()
                sys.exit(0)

        # Snapshot 버튼 이벤트 처리
        try:
            event = dev.read_one()
        except OSError:
            print("장치 오류. 연결이 끊겼거나 제거됨.")
            sys.exit(1)

        if event and event.type == ecodes.EV_KEY and event.code == ecodes.KEY_VOLUMEUP and event.value == 1:
            state = not state
            print("on" if state else "off")
