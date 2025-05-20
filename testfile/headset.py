import subprocess

recording = None  # 녹음 상태 저장용

# 무한 반복
while True:
		# 키 입력 받기
    cmd = input("Enter: 녹음 시작/중지 | p: 재생 | q: 종료\n입력: ")

	# quit -----------------------
    if cmd == 'q':
		    # 만약에 녹음 중에 enter가 아닌 q를 눌렀어도 중지하고 종료하도록
        if recording:
            print("녹음 중지")
            recording.terminate()
            recording = None
        print("프로그램 종료")
        break

	# play -----------------------
    elif cmd == 'p':
        print("파일 재생 중...")
        subprocess.run([
            "aplay", "out.wav"
        ])  # 기본 재생 명령어, ALSA 기반

	# Enter를 눌렀을 때 ------------
		# None 상태인 경우엔 녹음 시작 -> recoding이 Popen 상태 됨
    elif recording is None:
        print("녹음 시작")
        recording = subprocess.Popen([
            "arecord", "-D", "plughw:2,0", "-f", "S16_LE", "-r", "16000", "-c", "1", "out.wav"
        ])
    # None 상태가 아닌 경우 녹음 중지 -> recoding이 다시 None이 됨
    else:
        print("녹음 중지")
        recording.terminate()
        recording = None