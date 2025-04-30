# HW
하드웨어팀

만약 JSON 요청으로 데이터를 받는 게 아닌, Python 코드에서 값을 넘겨준다면 API 호출을 위한 서버는 필요없고 그냥 모듈 형태로 정리해놓기만 하면 됨

소프트웨어팀이 우리의 코드를 라이브러리처럼 import 해서 호출 하고 
ex) from display_emotion import show_expression
emotion_result = "happy" #GPT 결과값 넣기
show_expression(emotion_result)
-> 이렇게 하면 된다네...?
