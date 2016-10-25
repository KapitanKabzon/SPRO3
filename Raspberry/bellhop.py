from math import sin, cos
import serial


class Ping():
    def __init__(self, r, beta, gamma, arduino=None, id=None):
        self.r = r
        self.beta = beta
        self.gamma = gamma
        self.d = 0  # reading

    def point(self):
        """Return x, y coordinates with respect to own coordinate system"""
        x, y = self.r * cos(self.beta), self.r * sin(self.beta)
        return x, y

    def measurement_point(self):
        """Retrun x, y coordinates of measured point with respect to own
        coordinate system"""
        x, y = self.point()
        xm = x + self.d * cos(self.gamma)
        ym = y + self.d * sin(self.gamma)
        return xm, ym


class Bellhop():
    def __init__(self, x, y, alpha):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.arduino = Arduino()


class Arduino():
    def __init__(self, PORT):
        self.serial = serial.Serial(PORT)
        self.reading = []

    def sensor_data(self, id):
        pass

    def read_data(self):
        line = self.serial.readline.decode()
        print(line)

    def close(self):
        self.serial.close()


if False:
    arduino = Arduino('/dev/ttyUSB0')
    arduino.close()
