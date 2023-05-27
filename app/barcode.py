import evdev

# 바코드 스캐너의 장치 파일 경로 지정
scanner = evdev.InputDevice('/dev/input/by-id/usb-0581_011c-event-kbd')

# 이벤트 루프 시작
barcode = ""
for event in scanner.read_loop():
    # 바코드 스캔 이벤트(42번 키 다운) 발생 시
    if event.type == evdev.ecodes.EV_KEY and event.code == evdev.ecodes.KEY_0:
        # 바코드 값 가져오기
        if event.value == 1:
            key_lookup = evdev.ecodes.KEY[event.code]
            # 숫자와 대문자 알파벳만 바코드로 인식
            if len(key_lookup) == 1:
                barcode += key_lookup

        # 바코드 값 출력
        if event.value == 0 and len(barcode) > 1:
            print(barcode[:-1])
            barcode = "" 
            #barcode 변수에 바코드 정보(바코드 고유 번호) 들어있음
