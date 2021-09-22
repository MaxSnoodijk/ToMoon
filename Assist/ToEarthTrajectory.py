import numpy as np
import matplotlib.pyplot as plt
import time

G = 6.674 * 10 ** -11

boost = 0.8

velocity_factor = 0.619

orbit_earth = 1.000 * 10 ** 6
orbit_moon = 5.000 * 10 ** 5

begin = time.time()


class Earth:
    x = 0
    y = 0

    m = 5.972 * 10 ** 24
    r = 6.371 * 10 ** 6


class Moon:
    d = 3.840 * 10 ** 8

    m = 7.342 * 10 ** 22
    r = 1.737 * 10 ** 6


class Sat:
    x = - (Moon.d + Moon.r + orbit_moon)
    y = 0

    d = np.sqrt(x ** 2 + y ** 2)


class Ref:
    x = Sat.x
    y = Sat.y

    d = np.sqrt(x ** 2 + y ** 2)


def gravity(d, m):
    a = (G * m) / d ** 2
    return a


def circular_orbit(d, m):
    v = np.sqrt((G * m) / d)
    return v


def transfer_orbit(m, a, e):
    v_pericenter = np.sqrt((G * m * (1 + e)) / (a * (1 - e)))
    v_apocenter = np.sqrt((G * m * (1 - e)) / (a * (1 + e)))

    return v_pericenter, v_apocenter


x_moon_tab = []
y_moon_tab = []

x_sat_tab = []
y_sat_tab = []

x_ref_tab = []
y_ref_tab = []

vx_sat_tab = []
vy_sat_tab = []

vx_ref_tab = []
vy_ref_tab = []

t = 0
dt = 1

pericenter = Earth.r + orbit_earth
apocenter = - Sat.x

axis = (apocenter + pericenter) / 2
eccentricity = (apocenter - pericenter) / (apocenter + pericenter)

v_escape = np.sqrt((2 * G * Moon.m) / (Moon.r + orbit_moon))
v_excess = transfer_orbit(Earth.m, axis, eccentricity)[1]

Sat.vx = 0
Sat.vy = velocity_factor * v_escape

T_transfer = np.pi * np.sqrt(axis ** 3 / (G * Earth.m))
T_orbit = 2 * np.pi * np.sqrt((Moon.r + orbit_moon) ** 3 / (G * Moon.m))

Ref.vx = 0
Ref.vy = transfer_orbit(Earth.m, axis, eccentricity)[1]

Moon.v = circular_orbit(Moon.d, Earth.m)

Moon.x = - Moon.d
Moon.y = 0

Sat.d_moon = Moon.x - Sat.x

Moon.vx = 0
Moon.vy = - Moon.v

delta_v = 0
delta_v_initial = Sat.vy - (Moon.v - circular_orbit((Moon.r + orbit_moon), Moon.m))

simulation = True

transfer = True

while t < 0.8 * T_transfer:

    Moon.a = gravity(Moon.d, Earth.m)
    Moon.ax = - (Moon.x / Moon.d) * Moon.a
    Moon.ay = - (Moon.y / Moon.d) * Moon.a

    Moon.vx += Moon.ax * dt
    Moon.vy += Moon.ay * dt
    Moon.v = np.sqrt(Moon.vx ** 2 + Moon.vy ** 2)

    Moon.x += Moon.vx * dt
    Moon.y += Moon.vy * dt
    Moon.d = np.sqrt(Moon.x ** 2 + Moon.y ** 2)

    Sat.dx_moon = Moon.x - Sat.x
    Sat.dy_moon = Moon.y - Sat.y
    Sat.d_moon = np.sqrt(Sat.dx_moon ** 2 + Sat.dy_moon ** 2)

    Sat.a = gravity(Sat.d, Earth.m)
    Sat.a_moon = gravity(Sat.d_moon, Moon.m)

    Sat.ax = - (Sat.x / Sat.d) * Sat.a + (Sat.dx_moon / Sat.d_moon) * Sat.a_moon
    Sat.ay = - (Sat.y / Sat.d) * Sat.a + (Sat.dy_moon / Sat.d_moon) * Sat.a_moon

    Sat.vx += Sat.ax * dt
    Sat.vy += Sat.ay * dt
    Sat.v = np.sqrt(Sat.vx ** 2 + Sat.vy ** 2)

    Sat.x += Sat.vx * dt
    Sat.y += Sat.vy * dt
    Sat.d = np.sqrt(Sat.x ** 2 + Sat.y ** 2)

    Ref.a = gravity(Ref.d, Earth.m)
    Ref.ax = - (Ref.x / Ref.d) * Ref.a
    Ref.ay = - (Ref.y / Ref.d) * Ref.a

    Ref.vx += Ref.ax * dt
    Ref.vy += Ref.ay * dt
    Ref.v = np.sqrt(Ref.vx ** 2 + Ref.vy ** 2)

    Ref.x += Ref.vx * dt
    Ref.y += Ref.vy * dt
    Ref.d = np.sqrt(Ref.x ** 2 + Ref.y ** 2)

    x_moon_tab.append(Moon.x / 10 ** 3)
    y_moon_tab.append(Moon.y / 10 ** 3)

    x_sat_tab.append(Sat.x / 10 ** 3)
    y_sat_tab.append(Sat.y / 10 ** 3)

    x_ref_tab.append(Ref.x / 10 ** 3)
    y_ref_tab.append(Ref.y / 10 ** 3)

    vx_sat_tab.append(Sat.vx)
    vy_sat_tab.append(Sat.vy)

    vx_ref_tab.append(Ref.vx)
    vy_ref_tab.append(Ref.vy)

    if t == round(0.5 * T_transfer):
        delta_v += np.sqrt((Sat.vx * boost) ** 2 + (Sat.vy * boost) ** 2) - Sat.v

        Sat.vx *= boost
        Sat.vy *= boost

    if Sat.d < 4 * Earth.r and Sat.y > Earth.y and transfer:

        Sat.vx = 0
        Sat.vy = circular_orbit(Sat.d, Earth.m)

        transfer = False

    t += dt

end = time.time()

print("Elapsed time [s]: ", round(end - begin))
print("Angle Sat [deg]: ", round(np.arctan(Sat.vx / Sat.vy) * 57.3, 2))
print("Distance [km]: ", round((Sat.d - Earth.r) / 10 ** 3))
print('Excess velocity [m/s]:', round(Sat.v - circular_orbit(Sat.d, Earth.m)))
print('Delta V correction [m/s]:', round(delta_v))
print('Total delta V:', round(delta_v_initial + abs(delta_v) + (Sat.v - circular_orbit(Sat.d, Earth.m))))

line1, = plt.plot(x_moon_tab, y_moon_tab, label='Moon')
line2, = plt.plot(x_sat_tab, y_sat_tab, label='Actual transfer')
line3, = plt.plot(x_ref_tab, y_ref_tab, label='Reference transfer')

plt.axhline(linewidth=1, color='black')
plt.axvline(linewidth=1, color='black')

plt.xlabel('X [km]')
plt.ylabel('Y [km]')
plt.title('Position trajectory')
plt.legend(handles=[line1, line2, line3])

plt.show()
