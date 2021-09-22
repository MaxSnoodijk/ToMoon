import numpy as np
import matplotlib.pyplot as plt

G = 6.674 * 10 ** -11

boost_1_magnitude = 1.05
boost_2_magnitude = 1.06

correction_moon_angle = 0.80
correction_transfer_2_angle = 4

orbit_earth_height = 4000 * 10 ** 3
orbit_moon_height = 1000 * 10 ** 3

t_passed = 0
count = 0


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
    x = Earth.r + orbit_earth_height
    y = 0

    d = np.sqrt(x ** 2 + y ** 2)
    d_moon = 0


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

vx_sat_tab = []
vy_sat_tab = []

orbit_d_tab = []
orbit_t_tab = []

t = 0
t_orbit_earth_elapsed = 0
t_transfer_1_elapsed = 0
t_transfer_2_elapsed = 0
t_orbit_moon_elapsed = 0

dt = 1

pericenter = Sat.x
apocenter = Moon.d + Moon.r + orbit_moon_height

axis = (apocenter + pericenter) / 2
eccentricity = (apocenter - pericenter) / (apocenter + pericenter)

axis_moon = 0
eccentricity_moon = 0

Sat.vx = 0
Sat.vy = circular_orbit(Sat.d, Earth.m)
Sat.v = np.sqrt(Sat.vx ** 2 + Sat.vy ** 2)

T_transfer_1 = np.pi * np.sqrt(axis ** 3 / (G * Earth.m))

T_orbit_earth = 2 * np.pi * np.sqrt((Earth.r + orbit_earth_height) ** 3 / (G * Earth.m))
T_orbit_moon = 2 * np.pi * np.sqrt((Moon.r + orbit_moon_height) ** 3 / (G * Moon.m))

boost_1 = True
boost_1_time = 0.25 * T_transfer_1

boost_2 = True
boost_2_time = 0.50 * T_transfer_1

Moon.v = circular_orbit(Moon.d, Earth.m)
Moon.angle = (((Moon.v * T_transfer_1) / Moon.d) * correction_moon_angle) + ((Moon.v * T_orbit_earth) / Moon.d)

Moon.x = - np.cos(Moon.angle) * Moon.d
Moon.y = np.sin(Moon.angle) * Moon.d

Moon.vx = - np.sin(Moon.angle) * Moon.v
Moon.vy = - np.cos(Moon.angle) * Moon.v

delta_v = 0
delta_v_1 = transfer_orbit(Earth.m, axis, eccentricity)[0] - circular_orbit(Sat.d, Earth.m)
delta_v_2 = 0
delta_v_3 = 0

thruster = True

orbit_earth = True
transfer_1 = False
transfer_2 = False
orbit_moon = False

phases = [orbit_earth, transfer_1, transfer_2, orbit_moon]

append_orbit_earth = True
append_transfer_1 = True
append_transfer_2 = True

rel_vx_tab = []
rel_vy_tab = []

program_position_list = []
program_time_list = []

program_position_list.append([round(Sat.x), round(Sat.y), round(Sat.vx), round(Sat.vy), round(Moon.x), round(Moon.y), round(Moon.vx), round(Moon.vy)])

while any(phases):

    if phases[0]:
        if t_orbit_earth_elapsed > T_orbit_earth:

            phases[0] = False
            phases[1] = True

        t_orbit_earth_elapsed += dt

    elif phases[1]:

        if thruster:

            # Small deviation after orbit causes larger oscillation at Moon

            Sat.x = 10371 * 10 ** 3
            Sat.y = 0
            Sat.vx = 0
            Sat.vy = 6199.3
            Sat.v = np.sqrt(Sat.vx ** 2 + Sat.vy ** 2)

            Sat.vx += (Sat.vx / Sat.v) * delta_v_1
            Sat.vy += (Sat.vy / Sat.v) * delta_v_1

            thruster = False

        if t_transfer_1_elapsed > boost_1_time and boost_1:
            delta_v += np.sqrt((Sat.vx * boost_1_magnitude) ** 2 + (Sat.vy * boost_1_magnitude) ** 2) - Sat.v

            Sat.vx *= boost_1_magnitude
            Sat.vy *= boost_1_magnitude

            boost_1 = False

        if t_transfer_1_elapsed > boost_2_time and boost_2:
            delta_v += np.sqrt((Sat.vx * boost_2_magnitude) ** 2 + (Sat.vy * boost_2_magnitude) ** 2) - Sat.v

            Sat.vx *= boost_2_magnitude
            Sat.vy *= boost_2_magnitude

            boost_2 = False

        if Sat.y > Moon.y and Sat.x < Moon.x and Sat.angle > (abs(Moon.angle) + correction_transfer_2_angle):

            print('Transfer 1 \n')
            print("Elapsed time [s]: ", t)
            print("Angle Sat [deg]: ", round(np.arctan(Sat.vx / Sat.vy) * (180 / np.pi), 2))
            print("Angle Moon [deg]: ", round(np.arctan(Moon.y / Moon.x) * (180 / np.pi), 2))
            print("Distance [km]: ", round((Sat.d_moon - Moon.r) / 10 ** 3), '\n')

            pericenter_moon = Moon.r + orbit_moon_height
            apocenter_moon = Sat.d_moon

            axis_moon = (apocenter_moon + pericenter_moon) / 2
            eccentricity_moon = (apocenter_moon - pericenter_moon) / (apocenter_moon + pericenter_moon)

            target_v = Moon.v - transfer_orbit(Moon.m, axis_moon, eccentricity_moon)[1]

            delta_v_2 = - (target_v + Sat.v)

            phases[1] = False
            phases[2] = True

            thruster = True

        t_transfer_1_elapsed += dt

    elif phases[2]:

        if thruster:

            Sat.vx += (Sat.vx / Sat.v) * delta_v_2
            Sat.vy += (Sat.vy / Sat.v) * delta_v_2

            thruster = False

        if Sat.y < Moon.y and Sat.x > Moon.x and Sat.d_d_moon > 0:

            print('Transfer 2 \n')
            print("Elapsed time [s]: ", t)
            print("Angle Sat [deg]: ", round(np.arctan(Sat.vx / Sat.vy) * (180 / np.pi), 2))
            print("Angle Moon [deg]: ", round(np.arctan(Moon.y / Moon.x) * (180 / np.pi), 2))
            print("Distance [km]: ", round((Sat.d_moon - Moon.r) / 10 ** 3), '\n')

            target_v = Moon.v + circular_orbit(Sat.d_moon, Moon.m)

            delta_v_3 = target_v - Sat.v

            phases[2] = False
            phases[3] = True

            thruster = True

        t_transfer_2_elapsed += dt

    elif phases[3]:

        if thruster:

            Sat.vx += (Sat.vx / Sat.v) * delta_v_3
            Sat.vy += (Sat.vy / Sat.v) * delta_v_3

            thruster = False

        if t_orbit_moon_elapsed > 2 * T_orbit_moon:
            phases[3] = False

        orbit_t_tab.append(t_orbit_moon_elapsed)
        orbit_d_tab.append(round((Sat.d_moon - Moon.r) / 10 ** 3, 2))

        t_orbit_moon_elapsed += dt

    Moon.a = gravity(Moon.d, Earth.m)
    Moon.ax = - (Moon.x / Moon.d) * Moon.a
    Moon.ay = - (Moon.y / Moon.d) * Moon.a

    Moon.vx += Moon.ax * dt
    Moon.vy += Moon.ay * dt
    Moon.v = np.sqrt(Moon.vx ** 2 + Moon.vy ** 2)

    Moon.x += Moon.vx * dt
    Moon.y += Moon.vy * dt
    Moon.d = np.sqrt(Moon.x ** 2 + Moon.y ** 2)

    Sat.d_moon_old = Sat.d_moon

    Sat.dx_moon = Sat.x - Moon.x
    Sat.dy_moon = Sat.y - Moon.y
    Sat.d_moon = np.sqrt(Sat.dx_moon ** 2 + Sat.dy_moon ** 2)

    Sat.d_d_moon = (Sat.d_moon - Sat.d_moon_old) / dt

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

    Sat.rel_vx = Sat.vx - Moon.vx
    Sat.rel_vy = Sat.vy - Moon.vy

    x_moon_tab.append(Moon.x / 10 ** 3)
    y_moon_tab.append(Moon.y / 10 ** 3)

    x_sat_tab.append(Sat.x / 10 ** 3)
    y_sat_tab.append(Sat.y / 10 ** 3)

    vx_sat_tab.append(Sat.vx)
    vy_sat_tab.append(Sat.vy)

    if t > 318000:

        rel_vx_tab.append(Sat.rel_vx)
        rel_vy_tab.append(Sat.rel_vy)

    Sat.angle = round(np.arctan(Sat.vx / Sat.vy) * (180 / np.pi), 1)
    Moon.angle = round(np.arctan(Moon.y / Moon.x) * (180 / np.pi), 1)

    if t % 25 == 0:

        program_position_list.append([round(Sat.x), round(Sat.y), round(Sat.vx), round(Sat.vy), round(Moon.x), round(Moon.y), round(Moon.vx), round(Moon.vy)])

        if phases[1] and append_orbit_earth:
            program_time_list.append(round(t))

            append_orbit_earth = False

        if phases[2] and append_transfer_1:
            program_time_list.append(round(t))

            append_transfer_1 = False

        if phases[3] and append_transfer_2:
            program_time_list.append(round(t))

            append_transfer_2 = False

    t += dt

program_time_list.append(round(boost_1_time))
program_time_list.append(round(boost_2_time))

program_position_array = np.array(program_position_list)
program_time_array = np.array(program_time_list)

np.savetxt("position_data.txt", program_position_array, fmt='%i')
np.savetxt("time_data.txt", program_time_array, fmt='%i')

print('Delta-V 1:', round(delta_v_1))
print('Delta-V 2:', round(delta_v_2))
print('Delta-V 3:', round(delta_v_3))
print('Trajectory adjustment delta-V:', round(delta_v))
print('Total delta-V: ', round(abs(delta_v_1)) + round(abs(delta_v_2)) + round(abs(delta_v_3)) + round(abs(delta_v)))

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

line1, = plt.plot(orbit_t_tab, orbit_d_tab, label='Distance')

plt.axhline(linewidth=1, color='black')
plt.axvline(linewidth=1, color='black')

plt.xlabel('t [s]')
plt.ylabel('d [km]')
plt.title('Distance')

plt.show()
