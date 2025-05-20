# pip3 install yeelight 사전 설치후 실행

from yeelight import Bulb

# 아이피를 적어줌으로써 연동 가능함
bulb = Bulb("")

# 전구 켜기
bulb.turn_on()

# 전구 끄기
bulb.turn_off()

# 50% 밝기로 조절하기
bulb.set_brightness(50)

# RGB 값을 직접 제어하기
bulb.set_rgb(255, 0, 0)

# 색 온도 제어하기
bulb.set_color_temp(4700)

# 지금까지 세팅을 디폴트 값으로 설정하기
bulb.set_default()