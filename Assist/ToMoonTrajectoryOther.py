import numpy as np
import matplotlib.pyplot as plt

G = 6.674 * 10 ** -11

boost_1_magnitude = 1.04
boost_2_magnitude = 1.04

angle_factor = 0.82

orbit_earth = 4000 * 10 ** 3
orbit_moon = 1000 * 10 ** 3


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
    x = Earth.r + orbit_earth
    y = 0

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
d_sat_tab = []

vx_sat_tab = []
vy_sat_tab = []

t_tab = []

t = 0

pericenter = Sat.x
apocenter = Moon.d + Moon.r + orbit_moon

axis = (apocenter + pericenter) / 2
eccentricity = (apocenter - pericenter) / (apocenter + pericenter)

axis_moon = 0
eccentricity_moon = 0

Sat.vx = 0
Sat.vy = circular_orbit(Sat.d, Earth.m)
Sat.v = np.sqrt(Sat.vx ** 2 + Sat.vy ** 2)

T_transfer = np.pi * np.sqrt(axis ** 3 / (G * Earth.m))
T_orbit = 2 * np.pi * np.sqrt((Moon.r + orbit_moon) ** 3 / (G * Moon.m))

boost_1 = True
boost_1_time = 0.25 * T_transfer

boost_2 = True
boost_2_time = 0.50 * T_transfer

Moon.v = circular_orbit(Moon.d, Earth.m)
Moon.angle = ((Moon.v * T_transfer) / Moon.d) * angle_factor

print(round(Moon.angle, 5))
print()

Moon.x = - np.cos(Moon.angle) * Moon.d
Moon.y = np.sin(Moon.angle) * Moon.d

Moon.vx = - np.sin(Moon.angle) * Moon.v
Moon.vy = - np.cos(Moon.angle) * Moon.v

delta_v = 0
delta_v_1 = transfer_orbit(Earth.m, axis, eccentricity)[0] - circular_orbit(Sat.d, Earth.m)
delta_v_2 = 0
delta_v_3 = 0

delta_v_2_burn_time = 0
delta_v_3_burn_time = 0

thruster_time = 168
thruster_time_total = 234
thruster_time_difference = thruster_time_total - thruster_time

thruster = delta_v_1 / thruster_time_difference
thruster_correction = thruster / 4

transfer_1 = True
transfer_2 = False

delta_v_2_burn = False
delta_v_3_burn = False

simulation = True

yes = True

while transfer_1:

    dt = 0.5

    if t < thruster_time_difference:

        Sat.vx += (Sat.vx / Sat.v) * thruster * dt
        Sat.vy += (Sat.vy / Sat.v) * thruster * dt

    Moon.a = gravity(Moon.d, Earth.m)
    Moon.ax = - (Moon.x / Moon.d) * Moon.a
    Moon.ay = - (Moon.y / Moon.d) * Moon.a

    Moon.vx += Moon.ax * dt
    Moon.vy += Moon.ay * dt
    Moon.v = np.sqrt(Moon.vx ** 2 + Moon.vy ** 2)

    Moon.x += Moon.vx * dt
    Moon.y += Moon.vy * dt
    Moon.d = np.sqrt(Moon.x ** 2 + Moon.y ** 2)

    Sat.dx_moon = Sat.x - Moon.x
    Sat.dy_moon = Sat.y - Moon.y
    Sat.d_moon = np.sqrt(Sat.dx_moon ** 2 + Sat.dy_moon ** 2)

    Sat.a = gravity(Sat.d, Earth.m)
    Sat.a_moon = gravity(Sat.d_moon, Moon.m)

    Sat.ax = - (Sat.x / Sat.d) * Sat.a - (Sat.dx_moon / Sat.d_moon) * Sat.a_moon
    Sat.ay = - (Sat.y / Sat.d) * Sat.a - (Sat.dy_moon / Sat.d_moon) * Sat.a_moon

    Sat.vx += Sat.ax * dt
    Sat.vy += Sat.ay * dt
    Sat.v = np.sqrt(Sat.vx ** 2 + Sat.vy ** 2)

    Sat.x += Sat.vx * dt
    Sat.y += Sat.vy * dt
    Sat.d = np.sqrt(Sat.x ** 2 + Sat.y ** 2)

    x_moon_tab.append(Moon.x / 10 ** 3)
    y_moon_tab.append(Moon.y / 10 ** 3)

    x_sat_tab.append(Sat.x / 10 ** 3)
    y_sat_tab.append(Sat.y / 10 ** 3)

    vx_sat_tab.append(Sat.vx)
    vy_sat_tab.append(Sat.vy)

    Sat.angle = round(np.arctan(Sat.vx / Sat.vy) * (180 / np.pi), 1)
    Moon.angle = round(np.arctan(Moon.y / Moon.x) * (180 / np.pi), 1)

    if t >= boost_1_time and boost_1:
        delta_v += np.sqrt((Sat.vx * boost_1_magnitude) ** 2 + (Sat.vy * boost_1_magnitude) ** 2) - Sat.v

        Sat.vx *= boost_1_magnitude
        Sat.vy *= boost_1_magnitude

        boost_1 = False

    if t >= boost_2_time and boost_2:
        delta_v += np.sqrt((Sat.vx * boost_2_magnitude) ** 2 + (Sat.vy * boost_2_magnitude) ** 2) - Sat.v

        Sat.vx *= boost_2_magnitude
        Sat.vy *= boost_2_magnitude

        boost_2 = False

    if Sat.y > Moon.y and Sat.x < Moon.x and Sat.angle == abs(Moon.angle) and transfer_1:

        print('Transfer 1 \n')
        print("Elapsed time [s]: ", t)
        print("Angle Sat [deg]: ", round(np.arctan(Sat.vx / Sat.vy) * (180 / np.pi), 2))
        print("Angle Moon [deg]: ", round(np.arctan(Moon.y / Moon.x) * (180 / np.pi), 2))
        print("Distance [km]: ", round((Sat.d_moon - Moon.r) / 10 ** 3), '\n')

        pericenter_moon = Moon.r + orbit_moon
        apocenter_moon = Sat.d_moon

        axis_moon = (apocenter_moon + pericenter_moon) / 2
        eccentricity_moon = (apocenter_moon - pericenter_moon) / (apocenter_moon + pericenter_moon)

        target_v = Moon.v - transfer_orbit(Moon.m, axis_moon, eccentricity_moon)[1]

        delta_v_2 = - (target_v + Sat.v)
        delta_v_2_burn = True
        delta_v_2_burn_time = (abs(delta_v_2) / thruster_correction) + t

        transfer_1 = False
        transfer_2 = True

    if delta_v_2_burn and t < delta_v_2_burn_time:

        Sat.vx -= (abs(Sat.vx) / Sat.v) * thruster_correction * dt
        Sat.vy -= (abs(Sat.vy) / Sat.v) * thruster_correction * dt

    if Sat.y < Moon.y and Sat.x > Moon.x and Sat.angle == abs(Moon.angle) and transfer_2:

        print('Transfer 2 \n')
        print("Elapsed time [s]: ", t)
        print("Angle Sat [deg]: ", round(np.arctan(Sat.vx / Sat.vy) * (180 / np.pi), 2))
        print("Angle Moon [deg]: ", round(np.arctan(Moon.y / Moon.x) * (180 / np.pi), 2))
        print("Distance [km]: ", round((Sat.d_moon - Moon.r) / 10 ** 3), '\n')

        target_v = Moon.v + circular_orbit(Sat.d_moon, Moon.m)

        delta_v_3 = (target_v - Sat.v)
        delta_v_3_burn = True
        delta_v_3_burn_time = (abs(delta_v_3) / thruster_correction) + t

        transfer_2 = False

    if delta_v_3_burn and t < delta_v_3_burn_time:

        Sat.vx += (abs(Sat.vx) / Sat.v) * thruster_correction * dt
        Sat.vy += (abs(Sat.vy) / Sat.v) * thruster_correction * dt

    if not transfer_1 and not transfer_2:

        t_tab.append(t)
        d_sat_tab.append((Sat.d_moon - Moon.r) / 10 ** 3)

    t += dt

print(round(Moon.vx))
print(round(Moon.vy))
print(round(Moon.v))
print(round(Moon.x / 10 ** 3))
print(round(Moon.y / 10 ** 3))
print()
print(round(Sat.vx))
print(round(Sat.vy))
print(round(Sat.v))
print(round(Sat.x / 10 ** 3))
print(round(Sat.y / 10 ** 3))
print()
print(round(t))
print()

print('Delta-V 1:', round(delta_v_1))
print('Delta-V 2:', round(delta_v_2))
print('Delta-V 3:', round(delta_v_3))
print('Trajectory adjustment delta-V:', round(delta_v))
print('Total delta-V: ', round(abs(delta_v_1)) + round(abs(delta_v_2)) + round(abs(delta_v_3)) + round(abs(delta_v)))
print()
print('Total time [s]: ', round(delta_v_3_burn_time))
print('Total simulation time [s]: ', round(delta_v_3_burn_time / 50))
print('Total simulation time [h]: ', round(delta_v_3_burn_time / (50 * 3600), 2))

plt.subplot(1, 2, 1)

line1, = plt.plot(x_moon_tab, y_moon_tab, label='Moon')
line2, = plt.plot(x_sat_tab, y_sat_tab, label='Satellite')

plt.axhline(linewidth=1, color='black')
plt.axvline(linewidth=1, color='black')

plt.xlabel('X [km]')
plt.ylabel('Y [km]')
plt.title('Position trajectory')
plt.legend(handles=[line1, line2])

plt.subplot(1, 2, 2)

line1, = plt.plot(t_tab, d_sat_tab, label='Distance')

plt.axhline(linewidth=1, color='black')
plt.axvline(linewidth=1, color='black')

plt.xlabel('t [s]')
plt.ylabel('d [km]')
plt.title('Distance')

plt.show()
