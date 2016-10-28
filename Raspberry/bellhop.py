from math import sin, cos, atan2
import serial


class Ping():
    def __init__(self, r, beta, gamma, arduino=None, id=None):
        self.id = id
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
    def __init__(self, x, y, alpha, arduino=None):
        self.x = x
        self.y = y
        # Bearing angle
        self.alpha = alpha
        self.arduino = arduino
        # List of attached ultrasonic sensors
        self.sensors = []

    def sensor_point(self, sensor: Ping):
        """Return x, y coordinates of a sensor with respect to
        the bellhop position"""
        x = self.x + sensor.r * sin(sensor.beta + self.alpha)
        y = self.y + sensor.r * cos(sensor.beta + self.alpha)
        return x, y

    def sensor_measurement(self, sensor: Ping):
        """Return x, y coordinates of measured point with respect to
        the bellhop position"""
        xs, ys = self.sensor_point(sensor)
        x = xs + sensor.d * sin(sensor.gamma + self.alpha)
        y = ys + sensor.d * cos(sensor.gamma + self.alpha)
        return x, y

    def update_position(self, x, y):
        '''Updates position of bellhop based on new position x, y'''
        self.x = x
        self.y = y

    def deltas(self, x, y):
        """Update position and return change in position and angle"""
        # Compute change in the position
        dx, dy = x - self.x, y - self.y

        # Compute change in the bearing angle
        # atan2() returns the angle in the correct quadrant
        theta = atan2(dy, dx)
        dalpha = theta - self.alpha

        # Update position
        self.update_position(x, y)
        return dx, dy, dalpha


class Arduino():
    def __init__(self, PORT):
#        self.serial = serial.Serial(PORT)
#        self.reading = []
        pass

    def sensor_data(self, id):
        pass

    def read_data(self):
        line = self.serial.readline.decode()
        print(line)

    def close(self):
        self.serial.close()
