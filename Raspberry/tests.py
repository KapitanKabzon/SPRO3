import unittest
from math import pi
from bellhop import Ping, Bellhop, Map


class PingTest(unittest.TestCase):
    def setUp(self):
        self.ping = Ping(1, (5*pi)/4, pi/2, None, id=4)
        self.ping.d = 5

    def test_point_x(self):
        x, y = self.ping.point()
        self.assertAlmostEqual(x, -1*(2**-0.5))

    def test_point_y(self):
        x, y = self.ping.point()
        self.assertAlmostEqual(y, -1*(2**-0.5))

    def test_measurement_x(self):
        x, y = self.ping.measurement_point()
        correct_x = -1*(2**-0.5) + 5
        self.assertAlmostEqual(x, correct_x)

    def test_measurement_y(self):
        x, y = self.ping.measurement_point()
        correct_y = -1*(2**-0.5)
        self.assertAlmostEqual(y, correct_y)


class BellhopTest(unittest.TestCase):
    def setUp(self):
        ping = Ping(1, pi/4, pi/2, None, id=4)
        ping.d = 10
        self.bellhop = Bellhop(5, 5, pi/6)
        self.bellhop.sensors.append(ping)

    def test_measurement_vector_x(self):
        x, y, vx, vy = self.bellhop.measurement_vector(self.bellhop.sensors[0])
        correct_x = 5.965925826289068
        self.assertAlmostEqual(x, correct_x)

    def test_measurement_vector_y(self):
        x, y, vx, vy = self.bellhop.measurement_vector(self.bellhop.sensors[0])
        correct_y = 5.258819045102521
        self.assertAlmostEqual(y, correct_y)

    def test_measurement_vector_vx(self):
        x, y, vx, vy = self.bellhop.measurement_vector(self.bellhop.sensors[0])
        correct_vx = 8.660254037844387
        self.assertAlmostEqual(vx, correct_vx)

    def test_measurement_vector_vy(self):
        x, y, vx, vy = self.bellhop.measurement_vector(self.bellhop.sensors[0])
        correct_vy = -5.0
        self.assertAlmostEqual(vy, correct_vy)

    def test_sensor_point_x(self):
        x, y = self.bellhop.sensor_point(self.bellhop.sensors[0])
        correct_x = 5.965925826289068
        self.assertAlmostEqual(x, correct_x)

    def test_sensor_point_y(self):
        x, y = self.bellhop.sensor_point(self.bellhop.sensors[0])
        correct_y = 5.258819045102521
        self.assertAlmostEqual(y, correct_y)

    def test_sensor_measurement_x(self):
        x, y = self.bellhop.sensor_measurement(self.bellhop.sensors[0])
        correct_x = 14.626179864133455
        self.assertAlmostEqual(x, correct_x)

    def test_sensor_measurement_y(self):
        x, y = self.bellhop.sensor_measurement(self.bellhop.sensors[0])
        correct_y = 0.2588190451025225
        self.assertAlmostEqual(y, correct_y)

    def test_update_position_x(self):
        self.bellhop.update_position(2, 3)
        self.assertEqual(self.bellhop.x, 2)

    def test_update_position_y(self):
        self.bellhop.update_position(2, 3)
        self.assertEqual(self.bellhop.y, 3)


class MapTest(unittest.TestCase):
    def setUp(self):
        self.map = Map('testMap.json')
        self.line = (8, 8, 3, 2)

    def test_infront(self):
        walls = []
        for wall in self.map.infront(self.line):
            walls.append(wall)
        correct_walls = [[10, 16, 16, 10], [12, 16, 16, 12]]
        self.assertEqual(walls, correct_walls)

    def test_closest(self):
        wall = self.map.closest(self.line)
        correct_wall = [10, 16, 16, 10]
        self.assertEqual(wall, correct_wall)
        pass

    def test_intersection_x(self):
        line2 = (12, 8, -1, 2)
        x, y = self.map.intersection(self.line, line2)
        correct_x = 11
        self.assertEqual(x, correct_x)

    def test_intersection_y(self):
        line2 = (12, 8, -1, 2)
        x, y = self.map.intersection(self.line, line2)
        correct_y = 10
        self.assertEqual(y, correct_y)

    def test_wall_vector_x0(self):
        wall = [16, 10, 10, 16]
        x0, y0, vx, vy = Map.wall_vector(wall)
        correct_x0 = 16
        self.assertEqual(x0, correct_x0)

    def test_wall_vector_y0(self):
        wall = [16, 10, 10, 16]
        x0, y0, vx, vy = Map.wall_vector(wall)
        correct_y0 = 10
        self.assertEqual(y0, correct_y0)

    def test_wall_vector_xv(self):
        wall = [16, 10, 10, 16]
        x0, y0, vx, vy = Map.wall_vector(wall)
        correct_vx = -6
        self.assertEqual(vx, correct_vx)

    def test_wall_vector_yv(self):
        wall = [16, 10, 10, 16]
        x0, y0, vx, vy = Map.wall_vector(wall)
        correct_vy = 6
        self.assertEqual(vy, correct_vy)


class ArduinoTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_sensor_data(self):
        pass

    def test_read_data(self):
        pass

    def test_close(self):
        pass
