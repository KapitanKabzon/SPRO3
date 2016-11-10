from math import sin, cos
import serial
from numpy import array
from numpy.linalg import solve
import json


class Ping():
    def __init__(self, r, beta, gamma, arduino=None, id=None):
        self.id = id
        self.r = r
        self.beta = beta
        self.gamma = gamma
        self.d = 0  # reading
        self.arduino = arduino

    def point(self):
        """Return x, y coordinates with respect to own coordinate system"""
        x, y = self.r * sin(self.beta), self.r * cos(self.beta)
        return x, y

    def measurement_point(self):
        """Retrun x, y coordinates of measured point with respect to own
        coordinate system"""
        x, y = self.point()
        xm = x + self.d * sin(self.gamma)
        ym = y + self.d * cos(self.gamma)
        return xm, ym

    def update(self):
        self.d = self.arduino.measurements[self.id]

    def vect(self):
        """Return vector representation of measurement line"""
        x0, y0 = self.r * sin(self.beta), self.r * cos(self.gamma)
        xv, yv = self.d * sin(self.gamma), self.d * cos(self.gamma)
        return x0, y0, xv, yv


class Bellhop():
    def __init__(self, x, y, alpha, arduino=None, map='map.json'):
        self.x = x
        self.y = y
        # Bearing angle
        self.alpha = alpha
        self.arduino = arduino
        # List of attached ultrasonic sensors
        self.sensors = []
        self.map = Map(map)

    def measurement_vector(self, sensor: Ping):
        """Return vector representation of measurement line"""
        x0 = self.x + sensor.r * sin(self.alpha + sensor.beta)
        y0 = self.y + sensor.r * cos(self.alpha + sensor.beta)
        xv = sensor.d * sin(self.alpha + sensor.gamma)
        yv = sensor.d * cos(self.alpha + sensor.gamma)
        return x0, y0, xv, yv

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
        """Updates position of bellhop based on new position x, y"""
        self.x = x
        self.y = y

'''
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
'''


class Map():
    def __init__(self, file='map.json'):
        with open(file) as f:
            self.walls = json.load(f)

    def infront(self, line):
        """Generate walls which are in front of a line"""
        for wall in self.walls:
            wall_v = self.wall_vector(wall)
            try:
                ix, iy = self.intersection(line, wall_v)
            except:
                continue
            x, y = self.intersection(line, wall_v)
            x, y = x - line[0], y - line[1]
            vx, vy = line[2], line[3]
            max_x = max(wall[0], wall[2])
            min_x = min(wall[0], wall[2])
            max_y = max(wall[1], wall[3])
            min_y = min(wall[1], wall[3])

            if not ((x <= 0 and vx <= 0) or (x >= 0 and vx >= 0)):
                continue
            if not ((y <= 0 and vy <= 0) or (y >= 0 and vy >= 0)):
                continue
            if not ((ix >= min_x and ix <= max_x)):
                continue
            if not ((iy >= min_y and iy <= max_y)):
                continue

            yield wall

    def closest(self, line):
        """Return closest wall infront of a line"""
        distances = []
        for wall in self.infront(line):
            wall_v = self.wall_vector(wall)
            x0, y0 = line[0], line[1]
            x, y = self.intersection(line, wall_v)
            x, y = x - x0, y - y0
            d = (x**2 + y**2)**0.5
            distances.append((d, wall))
        if not distances:
            return None
        else:
            a = min(distances)
            return a[1]

    @staticmethod
    def intersection(line1, line2):
        """Return point of intersection of two lines"""
        a = array([[line2[2], -line1[2]],
                   [line2[3], -line1[3]]])
        b = array([[line1[0] - line2[0]],
                   [line1[1] - line2[1]]])
        try:
            co = solve(a, b)
        except:
            return None

        x = line2[0] + co[0][0] * line2[2]
        y = line2[1] + co[0][0] * line2[3]
        return x, y

    @staticmethod
    def length(line):
        """Return length of a line"""
        x1, y1, x2, y2 = line
        x, y = x2 - x1, y2 - y1
        len = (x**2 + y**2)**0.5
        return len

    @staticmethod
    def wall_vector(wall):
        """Return vector representation of wall line"""
        x0, y0 = wall[0], wall[1]
        xv, yv = wall[2] - wall[0], wall[3] - wall[1]
        return x0, y0, xv, yv


class Arduino():
    def __init__(self, PORT):
        self.serial = serial.Serial(PORT)
        self.measurements = []
        pass

    def sensor_data(self, id):
        pass

    def read_data(self):
        line = self.serial.readline.decode()
        print(line)

    def close(self):
        self.serial.close()
