"""
The purpose of this program is to interact with the Arduino..
	:;: What this function performs..?
	::  * This program receives the car_control_commands from the Raspberry Pi(master_of_car) and sends it to the
	        Arduino to perform appropriate operation based on the command issued..
	    * To say even more clearly, this is the only program which directly acts as a mediater between a
	                Micro_Controller(Arduino) and the Micro_Processor(Raspberry pi)
"""
# Importing the Required packages
import serial  # To have a serial communication between the Arduino
import time

# Deals with arduino
class dealWithArduino(object):
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
	def __init__(self):
		self.serialPort = '/dev/ttyACM0'
		self.baudrate = 9600
		
		self.ser = dealWithArduino.ser
		self.obstacleDistance = 0
		time.sleep(5)  # For adjustment
		print("Connection established with Arduino sir, at port - " + self.serialPort + "with baudrate - " + str(self.baudrate))
	
	def controlCar(self, command, turnAngle=60):
		# Know the command  sent by the master, and sent appropriate signal that Arduino can understand..
		if command == 'FORWARD':
			print("Forward")
			self.ser.write(chr(1).encode())
		elif command == 'BACKWARD':
			print("Backward ")
			self.ser.write(chr(2).encode())
		elif command == 'LEFT':
			print("<-- Left ")
			self.ser.write(chr(3).encode())
		elif command == 'RIGHT':
			print("Right-->>")
			self.ser.write(chr(4).encode())
		elif command == "FWD_LFT":
			print("Forward-Left")
			self.ser.write(chr(5).encode())
		elif command == 'FWD_RGHT':
			print("Forward-Right")
			self.ser.write(chr(6).encode())
		elif command == 'BWD_LFT':
			print("Backward-Left")
			self.ser.write(chr(7).encode())
		elif command == 'BWD_RGHT':
			print("Backward-Right")
			self.ser.write(chr(8).encode())
		elif command == 'STOP':
			print("STOPPED..!!")
			self.ser.write(chr(9).encode())
		
		else:
			print('Unknown command received..!!!')
	
	def receiveSensorData(self):
		if self.ser.in_waiting>0:
			self.obstacleDistance = self.ser.readline() ## Getting the data from Arduino
			#print("Obstacle is at",self.obstacleDistance)
			return self.obstacleDistance  # P2N: We'll get the distance in cm (means from the equation we applied to get the distance)and we are returning in cm
	
	

# Whatever we would like to send to arduino it must be interms of bytes only
# Refer https://classes.engineering.wustl.edu/ese205/core/index.php?title=Serial_Communication_between_Raspberry_Pi_%26_Arduino for more clarity
