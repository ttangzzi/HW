import os #파일 경로 처리
import time #재생 사이에 잠시 기다릴 때 사용
import subprocess #외부 프로그램 (여기서 omxplayer 실행)

EXPRESSIONS_FOLDER = "expressions" #동영상 파일이 들어있는 폴더 이름


EXPRESSIONS = {
    "neutral": "neutral.mp4",
    "anxious": "anxious.mp4",
    "happy": "happy.mp4"
} #감정 키워드에 대응되는 동영상 파일 이름을 매핑한 딕셔너리
#근데 데이터를 보낼 때 표정(동영상 파일)로 보낸다면 필요 없지 않나... 그러면 아래 코드 수정해야할 듯

def show_expression(emotion): #감정 이름을 받아서 그에 맞는 동영상 파일을 찾아 재생
    if emotion not in EXPRESSIONS:
        print(f"[오류] '{emotion}' 감정은 정의되어 있지 않습니다.")
        return
    
    video_path = os.path.join(EXPRESSIONS_FOLDER, EXPRESSIONS[emotion]) #실제 동영상 파일 경로 생성
    
    if not os.path.exists(video_path):
        print(f"[오류] 동영상 파일이 존재하지 않습니다: {video_path}")
        return
    
    print(f"[표정 재생] 감정: {emotion} → 파일: {video_path}") #테스트용 실행 로그 
    
    subprocess.run(["omxplayer", "--no-osd", video_path]) #라즈베리파이에 omxplayer는 설치되어 있음 
    #라즈베리파이에서 동영상을 실제로 재생하는 명령
    #omxplayer: 라즈베리파이 기본 동영상 플레이어
    #--no-osd: 영상 재생 시 화면에 타이틀 표시 안 함

# 테스트
if __name__ == "__main__":
    show_expression("happy")
    time.sleep(2)
    show_expression("anxious")
    time.sleep(2)
    show_expression("neutral")
