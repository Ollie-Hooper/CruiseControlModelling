from math import cos, sin, pi


class Car:

    def __init__(self, mass, dimensions, drag_coefficient, power, torque, top_speed, wheel_dimensions):
        self.mass = mass
        self.height = dimensions[0]
        self.width = dimensions[1]
        self.length = dimensions[2]
        self.Cd = drag_coefficient
        self.power = power
        self.torque = torque
        self.top_speed = top_speed
        self.wheel_width = wheel_dimensions[0]
        self.wheel_radius = wheel_dimensions[1]

        self.mu = 0.25
        self.g = -9.81
        self.air_density = 1
        self.angle = 0.2

        self.speed = 0

    def cross_sectional_area(self):
        return self.height * self.width

    def friction(self):
        mu = self.mu
        M = self.mass
        g = self.g
        a = self.angle
        return mu * M * g * cos(a)

    def weight(self):
        M = self.mass
        g = self.g
        a = self.angle
        return M * g * sin(a)

    def drag(self, v):
        Cd = self.Cd
        A = self.cross_sectional_area()
        rho = self.air_density
        a = self.angle
        return 0.5 * Cd * A * rho * v ** 2

    def accelerating_force(self):
        a = self.angle
        t = self.torque
        r = self.wheel_radius
        return t/(r*sin(a))

    def resultant_acceleration(self, v):
        A = self.accelerating_force()
        F = self.friction()
        W = self.weight()
        d = self.drag(v)
        M = self.mass
        return (A + F + W + d) / M
