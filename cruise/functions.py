from math import cos, sin


def friction(mu, M, a, g=-9.81):
    return mu*M*g*cos(a)


def weight(M, a, g=-9.81):
    return M*g*sin(a)


def drag(Cd, A, rho, v):
    return 0.5*Cd*A*rho*v**2


def acceleration(t, r, a):
    return t/(r*sin(a))

