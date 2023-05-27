import time
import serial

# ser = serial.Serial("/dev/ttyUSB1", 115200)

ser = serial.Serial("/dev/serial0", 115200) # serialAmm0(구버전) -> serial0(4B)으로 해야됨
# ser = serial.Serial("COM12", 115200)



def read_data():
    start_time = time.time()  # 시작 시간 기록
    while True:
        elapsed_time = time.time() - start_time  # 경과 시간 계산
        
        if elapsed_time >= 1:  # 1초 동안만 실행
            break
        
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                #print("Printing python3 portion")            
                distance = bytes_serial[2] + bytes_serial[3]*256
                strength = bytes_serial[4] + bytes_serial[5]*256
                temperature = bytes_serial[6] + bytes_serial[7]*256
                temperature = (temperature/8) - 256
                #print("Distance:"+ str(distance))
                #print("Strength:" + str(strength))
                #if temperature != 0:
                #    print("Temperature:" + str(temperature))
                ser.reset_input_buffer()
    return distance
                

if __name__ == "__main__":
    try:
        if ser.isOpen() == False:
            ser.open()
        read_data()
    except KeyboardInterrupt: # ctrl + c 누르면 종료
        if ser != None:
            ser.close()
            print("program interrupted by the user")
