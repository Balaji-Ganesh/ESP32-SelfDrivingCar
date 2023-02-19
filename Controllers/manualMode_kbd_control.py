'''
The purpose of this program is to interact with the car with in manual mode
    * For this purpose we are using "pygame" to for sensing keyboard keys
    * After sensing the appropriate key with the help of pygame we send it as a command to the Arduino to control the
        wheels for appropriate direction in which it is directed by the Controller(Administrator of the car)
    * We use "serial" library for serial communication with the Arduino
'''
# importing required libraries
import serial  # for serial communication with the Arduino
import pygame  # For sensing the keyboard keys which serves as a joystick or a remote to contorl the car
from utils.dealWithArduino import ArduinoHandler
import socket


class ManualControl(object):
    def __init__(self):
        pygame.init()  # calling the pygame's init function to work with all the pygame related functions, if we don't write this stmt, we can't use our pgm won't work properly
        # Creating the screen
        # Creating a pygame window of size 50 X 50
        self.screen = pygame.display.set_mode((561, 358))
        # Changing the window name
        pygame.display.set_caption("Car control in Manual Mode")
        # Background
        self.backgroundImg = pygame.image.load('../assets/greenBoard.jpg')
        # Changing the window icon
        pygameIcon = pygame.image.load('../assets/car.png')
        pygame.display.set_icon(pygameIcon)

        # taking the font to display direction in which the car is moving..
        self.directionFont = pygame.font.Font('../assets/comicSans.ttf', 32)
        # Where the font should display..(ie., Co-ordinates)
        self.textX, self.textY = 200, 130

        self.controlText = ""  # Updated while key stroke is recorded..

        # Taking the font to display the obstacle distance
        self.obstacleDistanceFont = pygame.font.Font('../assets/arial.ttf', 20)

        # To run the car_control_loop (while loop in steerTheCar)infinitely till the user quits..
        self.runTheCar = True
        # Creating the object of ArduinoHandler to contact with the hardware..
        # to interface with the Arduino control program
        self.arduinoControl = ArduinoHandler()
        self.steerTheCar()  # Start steering after setup.

    def steerTheCar(self):
        # car_control_loop
        while self.runTheCar:
            # Every control that should affect on our pygame screen/action should be in this infinte loop..
            # Filling the screen
            self.screen.fill((30, 30, 30))  # RGB values
            # Placing the background image
            self.screen.blit(self.backgroundImg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Will return the list of all the keys pressed
                    # key_pressed = pygame.key.get_pressed() -- needed for complex controls, not for normal.
                    print("Sensed the keydown action of keyboard")

                    # Normal Controls...
                    if event.key == pygame.K_LEFT:
                        self.controlText = "LEFT"
                        self.arduinoControl.controlCar('LEFT')

                    elif event.key == pygame.K_RIGHT:
                        self.controlText = "RIGHT"
                        self.arduinoControl.controlCar('RIGHT')

                    elif event.key == pygame.K_UP:
                        self.controlText = "FORWARD"
                        self.arduinoControl.controlCar('FORWARD')

                    elif event.key == pygame.K_DOWN:
                        self.controlText = "BACKWARD"
                        self.arduinoControl.controlCar('BACKWARD')

                    elif event.key == pygame.K_SPACE:
                        self.controlText = "Stopped"
                        self.arduinoControl.controlCar('STOP')

                    elif event.type == pygame.QUIT:
                        self.controlText = "Manual control - QUIT.!!"
                        break

                    # A bit complex controls -- for car design of model_1: like actual car.
                    # For this model_2: Not required.
                    # elif key_pressed[pygame.K_UP] and key_pressed[pygame.K_RIGHT]:
                    #     self.controlText = "Right Forward"
                    #     # self.arduinoControl.controlCar('FWD_RGHT')
                    #     self.conn.send('FWD_RGHT'.encode())

                    # elif key_pressed[pygame.K_UP] and key_pressed[pygame.K_LEFT]:
                    #     self.controlText = "Left Forward"
                    #     # self.arduinoControl.controlCar('FWD_LEFT')
                    #     self.conn.send('FWD_LEFT'.encode())

                    # elif key_pressed[pygame.K_DOWN] and key_pressed[pygame.K_RIGHT]:
                    #     self.controlText = "Right Backward"
                    #     # self.arduinoControl.controlCar('BWD_RGHT')
                    #     self.conn.send('BWD_RGHT'.encode())

                    # elif key_pressed[pygame.K_DOWN] and key_pressed[pygame.K_LEFT]:
                    #     self.controlText = "Left Backward"
                    #     # self.arduinoControl.controlCar('BWD_LEFT')
                    #     self.conn.send('BWD_LEFT'.encode())

            # print on console..
            print(self.controlText)
            # Displaying the direction on the window
            self.displayControlDirection(
                controlText=self.controlText, ordinates=(self.textX, self.textY))

            # Displaying the obstacle distance data on the screen
            # distance = self.arduinoControl.receiveSensorData()

            # Some times we may get None value, so to avoid that...
            # if distance is not None:
            # self.displayObstacleDistance(distance=str(distance, 'UTF-8'))# Decoding the received data and sending for display...

            # Make sure to update the screen after each and every change in screen
            # if this stmt doesn't exist, we can't see our changes which we've made on screen
            pygame.display.update()

    def displayControlDirection(self, controlText, ordinates):
        # For the font we first need to render and then blit it on image
        direction = self.directionFont.render(
            controlText, True, (255, 255, 255))
        self.screen.blit(direction, ordinates)

    def displayObstacleDistance(self, distance):
        # First Rendering text in order to blit on the image..
        distnce = "Obstacle in front at :" + str(distance) + "cm"
        dist = self.obstacleDistanceFont.render(distnce, True, (200, 200, 200))
        self.screen.blit(dist, (300, 10))


# Only if we run this program solely, execute this, else not...
if __name__ == '__main__':
    ManualControl()
