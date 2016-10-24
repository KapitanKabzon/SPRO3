import math
import serial
import random
import time


class Ping():
    def __init__(self, id, r, gamma, beta):
        self.id = id
        self.r = r
        self.gamma = gamma
        self.beta = beta
        self.d = 0  # reading

    def sensor_point(self, hop):
        xs = hop.x + hop.r * math.cos(self.gamma + hop.alpha)
        ys = hop.y + hop.r * math.sin(self.gamma + hop.alpha)
        return xs, ys


class Bellhopp():
    def __init__(self, x, y, alpha):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.arduino = Arduino()

    def get_data():


class Arduino():
    def __init__(self, PORT):
#        self.serial = serial.Serial(PORT)
        self.reading = []

    def read_data(self):
        # line = self.serial.readline().decode().strip('\r\n')
        # self.reading = line.split(sep=',')
        a = random.randrange(0, 5)
        time.sleep(1)
        return a

    def close(self):
        self.serial.close()

# test
arduino = Arduino('/dev/ttyUSB0')

while True:
    data = arduino.read_data()
    print(data)
