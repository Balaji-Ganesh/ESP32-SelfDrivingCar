#!/usr/bin/python3.7
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        ser.write('Hello from RPi..!!'.encode('utf-8'))  # send data
        line = ser.readline().decode('utf-8').rstrip()		# take ACK
        print(line)
        time.sleep(1)
