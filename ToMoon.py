from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.particles.ParticleEffect import ParticleEffect
from pathlib import Path

import numpy as np
import panda3d.core as pc
import sys
import pickle

pc.loadPrcFile('Configurations/Config.prc')

configuration = 'n'

# todo: no music overlap after first skip
# todo: general warnings
# todo: rewrite last time variable to orbit
# todo: tweak lunar orbit
# todo: general light fix
# todo: better Module textures / model complexity
# todo: slightly more interactive
# todo: maybe summary at end
# todo: check graphics Moon at start

# todo: fix position particles

# todo: final rewrite


class ToMoon:

    angle = 0.95782

    transfer_time_1 = 326577
    transfer_time_1_elapsed = 0.98 * transfer_time_1

    transfer_time_2 = 14021
    transfer_time_2_elapsed = 0.70 * transfer_time_2

    T_2_delta_v = - 814
    O_M_delta_v = - 257

    # Skip 1

    S_1_moon_vx = - 110
    S_1_moon_vy = - 1013
    S_1_moon_vz = 0

    S_1_moon_x = - 381744636
    S_1_moon_y = 41555818
    S_1_moon_z = 0

    S_1_satellite_vx = - 394
    S_1_satellite_vy = 225
    S_1_satellite_vz = 0

    S_1_satellite_x = - 387638137
    S_1_satellite_y = 32806250
    S_1_satellite_z = 0

    # Skip 2

    S_2_moon_vx = - 65
    S_2_moon_vy = - 1017
    S_2_moon_vz = 0

    S_2_moon_x = - 383223376
    S_2_moon_y = 24406795
    S_2_moon_z = 0

    S_2_satellite_vx = 1093
    S_2_satellite_vy = - 1476
    S_2_satellite_vz = 0

    S_2_satellite_x = - 383297694
    S_2_satellite_y = 28183730
    S_2_satellite_z = 0


class Initial_Physics():

    folder = Path('Load')
    file = folder / 'Physics.txt'

    def gravity(self, r, body):
        a = (self.G * body.m) / r ** 2

        return a

    def load(self):
        f = open(self.file, 'rb')
        return pickle.load(f)

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Physics, f)

    def __init__(self):

        if configuration == 'n':

            self.G = 6.674 * 10 ** -11
            self.time = 0

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Physics = Initial_Physics()


class Initial_Earth():

    folder = Path('Load')
    file = folder / 'Earth.txt'

    def load(self):
        f = open(self.file, 'rb')
        return pickle.load(f)

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Earth, f)

    def __init__(self):

        if configuration == 'n':

            self.m = 5.972 * 10 ** 24
            self.r = 6371 * 10 ** 3
            self.h = 0

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Earth = Initial_Earth()


class Initial_Moon():

    folder = Path('Load')
    file = folder / 'Moon.txt'

    def load(self):
        f = open(self.file, 'rb')
        return pickle.load(f)

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Moon, f)

    def __init__(self):

        if configuration == 'n':

            self.m = 7.342 * 10 ** 22
            self.r = 1727 * 10 ** 3
            self.d = 384000 * 10 ** 3
            self.v = np.sqrt((Physics.G * Earth.m) / self.d)
            self.angle = ToMoon.angle

            self.x = - np.cos(self.angle) * self.d
            self.y = np.sin(self.angle) * self.d
            self.z = 0

            self.vx = - np.sin(self.angle) * self.v
            self.vy = - np.cos(self.angle) * self.v
            self.vz = 0

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Moon = Initial_Moon()


class Initial_Satellite():

    folder = Path('Load')
    file = folder / 'Satellite.txt'

    def load(self):
        f = open(self.file, 'rb')
        return pickle.load(f)

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Satellite, f)

    def __init__(self):

        if configuration == 'n':

            self.earth_angle_1 = np.pi / 2
            self.earth_angle_2 = (3 * np.pi) / 32
            self.earth_angle = self.earth_angle_1 + self.earth_angle_2

            self.orbit_earth = 4000 * 10 ** 3
            self.orbit_moon = 1000 * 10 ** 3

            self.d = Earth.r + self.orbit_earth
            self.x = np.cos(self.earth_angle) * self.d
            self.y = - np.sin(self.earth_angle) * self.d
            self.z = 0

            self.v = np.sqrt((Physics.G * Earth.m) / self.d)
            self.vx = - (self.y / self.d) * self.v
            self.vy = (self.x / self.d) * self.v
            self.vz = 0

            self.angle_yaw = (np.arctan(self.vy / self.vx)) * (180 / np.pi)

            self.h_earth_dot = self.v / self.d
            self.h_moon_dot = 0

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Satellite = Initial_Satellite()


class Initial_Trajectory():

    folder = Path('Load')
    file = folder / 'Trajectory.txt'

    def load(self):
        f = open(self.file, 'rb')
        return pickle.load(f)

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Trajectory, f)

    def __init__(self):

        if configuration == 'n':

            # Transfer 1

            self.T_1_pericenter = Satellite.d
            self.T_1_apocenter = Moon.d + Moon.r + Satellite.orbit_moon
            self.T_1_axis = (self.T_1_apocenter + self.T_1_pericenter) / 2
            self.T_1_eccentricity = (self.T_1_apocenter - self.T_1_pericenter) / \
                                    (self.T_1_apocenter + self.T_1_pericenter)

            self.T_1_v_pericenter = np.sqrt((Physics.G * Earth.m * (1 + self.T_1_eccentricity)) /
                                            (self.T_1_axis * (1 - self.T_1_eccentricity)))
            self.T_1_v_apocenter = np.sqrt((Physics.G * Earth.m * (1 - self.T_1_eccentricity)) /
                                           (self.T_1_axis * (1 + self.T_1_eccentricity)))

            self.T_1_delta_v = self.T_1_v_pericenter - Satellite.v

            self.T_1_time = np.pi * np.sqrt(self.T_1_axis ** 3 / (Physics.G * Earth.m))

            # Transfer 2

            self.T_2_pericenter = 0
            self.T_2_apocenter = 0
            self.T_2_axis = 0
            self.T_2_eccentricity = 0
            self.T_2_v_pericenter = 0
            self.T_2_v_apocenter = 0
            self.T_2_delta_v = ToMoon.T_2_delta_v
            self.T_2_time = 0

            # Lunar orbit

            self.O_M_delta_v = ToMoon.O_M_delta_v
            self.O_M_time = 2 * np.pi * np.sqrt((Moon.r + Satellite.orbit_moon) ** 3 / (Physics.G * Moon.m))

            # Time

            self.transfer_1_time = ToMoon.transfer_time_1
            self.transfer_1_time_elapsed = 0

            self.transfer_2_time = ToMoon.transfer_time_2
            self.transfer_2_time_elapsed = 0

            self.time_factor = 10

            # Thruster

            self.thruster_x = 0
            self.thruster_y = 0
            self.thruster_z = 0

            # Launch 1

            self.launch_1_time = (Satellite.earth_angle / Satellite.h_earth_dot) / self.time_factor
            self.launch_1_time_sound_start = 168
            self.launch_1_time_sound_stop = 234
            self.launch_1_time_difference = self.launch_1_time_sound_stop - self.launch_1_time_sound_start

            self.launch_1_thruster = self.T_1_delta_v / self.launch_1_time_difference

            # Launch 2

            self.launch_2_time = ToMoon.transfer_time_1 / self.time_factor
            self.launch_2_time_sound_start = 155
            self.launch_2_time_sound_stop = 218
            self.launch_2_time_difference = self.launch_2_time_sound_stop - self.launch_2_time_sound_start

            self.launch_2_thruster = self.T_2_delta_v / self.launch_2_time_difference

            # Launch 3

            self.launch_3_time = ToMoon.transfer_time_2 / self.time_factor
            self.launch_3_time_sound_start = 287
            self.launch_3_time_sound_stop = 317
            self.launch_3_time_difference = self.launch_3_time_sound_stop - self.launch_3_time_sound_start

            self.launch_3_thruster = self.O_M_delta_v / self.launch_3_time_difference

            # Alignment

            self.turn_speed = 0
            self.turn_angle = 0

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Trajectory = Initial_Trajectory()


class Initial_Triggers():

    folder = Path('Load')
    file = folder / 'Triggers.txt'

    def load(self):
        f = open(self.file, 'rb')
        return pickle.load(f)

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Triggers, f)

    def __init__(self):

        if configuration == 'n':

            self.task_1 = False
            self.task_2 = False

            self.text = True
            self.text_dash = True

            self.sound = True
            self.sound_launch = False

            self.phase = True
            self.phase_sub = True
            self.phases = [True, False, False, False, False, False, False, False, False, False]

            self.phase_0 = True
            self.phase_1 = True
            self.phase_2 = None
            self.phase_3 = None
            self.phase_4 = None
            self.phase_5 = True
            self.phase_6 = None
            self.phase_7 = None
            self.phase_8 = True
            self.phase_9 = True

            self.transfer_1 = False
            self.transfer_2 = False

            self.reverse = False

            self.skip = True

            self.alignment = True
            self.alignment_auto = True
            self.reverse = False
            self.flip = True

            self.launch = True
            self.thruster = False

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Triggers = Initial_Triggers()


class Main(ShowBase):

    def update_physics(self, task):

        dt = globalClock.getDt() * Trajectory.time_factor

        Physics.time += globalClock.getDt()

        if Triggers.transfer_1:
            Trajectory.transfer_1_time_elapsed += dt

        if Triggers.transfer_2:
            Trajectory.transfer_2_time_elapsed += dt

        Moon.d_x = Satellite.x - Moon.x
        Moon.d_y = Satellite.y - Moon.y
        Moon.d_z = Satellite.z - Moon.z
        Moon.d_sat = np.sqrt(Moon.d_x ** 2 + Moon.d_y ** 2 + Moon.d_z ** 2)

        self.moon.setX(-Moon.d_x / self.scale)
        self.moon.setY(-Moon.d_y / self.scale)
        self.moon.setZ(-Moon.d_z / self.scale)

        self.earth.setX(-Satellite.x / self.scale)
        self.earth.setY(-Satellite.y / self.scale)
        self.earth.setZ(-Satellite.z / self.scale)

        self.earth.setH(Earth.h)

        if Triggers.alignment_auto:

            if Triggers.reverse and not Triggers.alignment:
                Satellite.angle_yaw = (np.arctan(Satellite.vy / Satellite.vx)) * (180 / np.pi) - 180

            elif Triggers.reverse and Triggers.alignment:

                if Trajectory.turn_angle > - 91:
                    Trajectory.turn_speed -= 0.001
                elif Trajectory.turn_angle > - 180:
                    Trajectory.turn_speed += 0.001
                else:
                    Trajectory.turn_speed = 0
                    Trajectory.turn_angle = - 180

                Satellite.angle_yaw = (np.arctan(Satellite.vy / Satellite.vx)) * (180 / np.pi) + Trajectory.turn_angle

                Trajectory.turn_angle += Trajectory.turn_speed

            else:
                Satellite.angle_yaw = (np.arctan(Satellite.vy / Satellite.vx)) * (180 / np.pi)

            if Satellite.vx > 0:
                self.satellite.setH(Satellite.angle_yaw)
            else:
                self.satellite.setH(180 + Satellite.angle_yaw)

        Moon.a = Physics.gravity(Moon.d, Earth)
        Moon.ax = (Moon.x / Moon.d) * Moon.a
        Moon.ay = (Moon.y / Moon.d) * Moon.a
        Moon.az = (Moon.z / Moon.d) * Moon.a

        Moon.vx -= Moon.ax * dt
        Moon.vy -= Moon.ay * dt
        Moon.vz -= Moon.az * dt
        Moon.v = np.sqrt(Moon.vx ** 2 + Moon.vy ** 2 + Moon.vz ** 2)

        Moon.x += Moon.vx * dt
        Moon.y += Moon.vy * dt
        Moon.z += Moon.vz * dt
        Moon.d = np.sqrt(Moon.x ** 2 + Moon.y ** 2 + Moon.z ** 2)

        Satellite.a = Physics.gravity(Satellite.d, Earth)
        Satellite.ax = (-Satellite.x / Satellite.d) * Satellite.a
        Satellite.ay = (-Satellite.y / Satellite.d) * Satellite.a
        Satellite.az = (-Satellite.z / Satellite.d) * Satellite.a

        Satellite.a = Physics.gravity(Moon.d_sat, Moon)
        Satellite.ax += (-Moon.d_x / Moon.d_sat) * Satellite.a
        Satellite.ay += (-Moon.d_y / Moon.d_sat) * Satellite.a
        Satellite.az += (-Moon.d_z / Moon.d_sat) * Satellite.a

        Satellite.vx += Satellite.ax * dt
        Satellite.vy += Satellite.ay * dt
        Satellite.vz += Satellite.az * dt
        Satellite.v = np.sqrt(Satellite.vx ** 2 + Satellite.vy ** 2 + Satellite.vz ** 2)

        if Triggers.thruster and Triggers.transfer_1:

            Satellite.vx += Trajectory.thruster_x * Trajectory.launch_1_thruster * (dt / Trajectory.time_factor)
            Satellite.vy += Trajectory.thruster_y * Trajectory.launch_1_thruster * (dt / Trajectory.time_factor)
            Satellite.vz += Trajectory.thruster_z * Trajectory.launch_1_thruster * (dt / Trajectory.time_factor)

        if Triggers.thruster and Triggers.transfer_2:

            Satellite.vx += Trajectory.thruster_x * Trajectory.launch_2_thruster * (dt / Trajectory.time_factor)
            Satellite.vy += Trajectory.thruster_y * Trajectory.launch_2_thruster * (dt / Trajectory.time_factor)
            Satellite.vz += Trajectory.thruster_z * Trajectory.launch_2_thruster * (dt / Trajectory.time_factor)

        Satellite.x += Satellite.vx * dt
        Satellite.y += Satellite.vy * dt
        Satellite.z += Satellite.vz * dt
        Satellite.d = np.sqrt(Satellite.x ** 2 + Satellite.y ** 2 + Satellite.z ** 2)

        Earth.h += (360 * dt) / (24 * 3600)

        Satellite.earth_angle = np.arctan(Satellite.y / Satellite.x)
        Moon.earth_angle = np.arctan(Moon.y / Moon.x)

        return task.cont

    def update_light(self, task):

        if Satellite.d < 4 * Earth.r or Moon.d_sat < 4 * Moon.r:

            fade_angle = np.pi / 6

            if Satellite.x <= 0:

                self.directionalLightSat.setColor((0.7, 0.7, 0.7, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif abs(Satellite.earth_angle) <= fade_angle:

                self.directionalLightSat.setColor((0, 0, 0, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif Satellite.earth_angle > fade_angle:

                intensity = (Satellite.earth_angle - fade_angle) / (4 * fade_angle)

                self.directionalLightSat.setColor((intensity, intensity, intensity, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif Satellite.earth_angle < - fade_angle:

                intensity = - (Satellite.earth_angle + fade_angle) / (4 * fade_angle)

                self.directionalLightSat.setColor((intensity, intensity, intensity, 1))
                self.satellite.setLight(self.directionalLightSatNP)

        else:

            self.directionalLightSat.setColor((0.5, 0.5, 0.5, 1))
            self.satellite.setLight(self.directionalLightSatNP)

        return task.cont

    def update_text(self, text, text_list, text_entry, text_time, task):

        if Triggers.text:

            self.time_symbol_reference = Physics.time
            self.time_dash_reference = self.time_symbol_reference + (len(text) * self.symbol_speed)
            self.time_total = self.time_symbol_reference + text_time

            self.sound_typing.play()

        Triggers.text = False

        if Physics.time >= self.time_total:
            self.text.setText('')
            self.text_NP.reparentTo(base.a2dTopLeft)

            Triggers.text = True

            self.symbol_counter = 0

            text_list[text_entry] = True

            return task.done

        if Physics.time >= self.time_symbol_reference:
            self.time_symbol_reference += self.symbol_speed
            self.symbol_counter += 1

        if Physics.time >= self.time_dash_reference:
            self.time_dash_reference += self.dash_speed

            if Triggers.text_dash:
                Triggers.text_dash = False
            else:
                Triggers.text_dash = True

        if self.symbol_counter < (len(text) - 1):

            self.text.setText(''.join(text[:self.symbol_counter]))
            self.text_NP.reparentTo(base.a2dTopLeft)

        else:
            self.sound_typing.stop()

            if Triggers.text_dash:

                self.text.setText(''.join(text))
                self.text_NP.reparentTo(base.a2dTopLeft)

            else:

                self.text.setText(''.join(text[:-2]))
                self.text_NP.reparentTo(base.a2dTopLeft)

        return task.cont

    def update_menu_triggers(self, menu):

        if menu == 'controls':
            if self.text2_trigger:
                self.text2_trigger = False
            else:
                self.text2_trigger = True

        if menu == 'trajectory':
            if self.text4_trigger:
                self.text4_trigger = False
            else:
                self.text4_trigger = True

        return

    def update_menus(self, menu, trigger):

        if menu == 'controls':

            self.text2_trigger = trigger

            if self.text2_trigger:
                self.text2.setText(("Camera controls" + "\n" + "\n" + "W:  rotate up" + "\n" + "S:  rotate down" + "\n"
                                    + "A:  rotate left" + "\n" + "D:  rotate right" + "\n" + "Scroll:  zoom" + "\n" +
                                    "X:  reset view" + "\n" + "Esc:  exit"))

            else:
                self.text2.setText("")

            self.text2_NP.reparentTo(base.a2dBottomRight)

        if menu == 'trajectory':

            self.text4_trigger = trigger

            if self.text4_trigger:

                if Triggers.transfer_1:

                    self.text4.setText("Trajectory information" + "\n" + "\n" + "Velocity  (m/s):  "
                                       + str(round(Satellite.v)) + "\n" + 'Distance to Earth  (km):  '
                                       + str(round((Satellite.d - Earth.r) / 10 ** 3)) + "\n"
                                       + 'Distance to Moon  (km):  ' + str(round((Moon.d_sat - Moon.r) / 10 ** 3))
                                       + "\n" + 'Transfer 1  (%):  '
                                       + str(round((Trajectory.transfer_1_time_elapsed /
                                                    Trajectory.transfer_1_time) * 100)))

                elif Triggers.transfer_2:

                    self.text4.setText("Trajectory information" + "\n" + "\n" + "Velocity  (m/s):  "
                                       + str(round(Satellite.v)) + "\n" + 'Distance to Earth  (km):  '
                                       + str(round((Satellite.d - Earth.r) / 10 ** 3)) + "\n"
                                       + 'Distance to Moon  (km):  ' + str(round((Moon.d_sat - Moon.r) / 10 ** 3))
                                       + "\n" + 'Transfer 2  (%):  '
                                       + str(round((Trajectory.transfer_2_time_elapsed /
                                                    Trajectory.transfer_2_time) * 100)))

                else:

                    self.text4.setText("Trajectory information" + "\n" + "\n" + "Velocity  (m/s):  "
                                       + str(round(Satellite.v)) + "\n" + 'Distance to Earth  (km):  '
                                       + str(round((Satellite.d - Earth.r) / 10 ** 3)) + "\n"
                                       + 'Distance to Moon  (km):  ' + str(round((Moon.d_sat - Moon.r) / 10 ** 3)))

            else:
                self.text4.setText("")

            self.text4_NP.reparentTo(base.a2dBottomLeft)

        return

    def update_phase_1(self):

        if self.failure_trigger:
            sys.exit()

        if Triggers.phase_sub:
            self.text3.setText('')
            self.text3_NP.reparentTo(self.aspect2d)

            Triggers.phase_sub = False

            self.minor_trigger = True
            self.major_trigger = True

        if Triggers.phase or Triggers.task_2:
            phase = np.where(Triggers.phases)[0][0]
            Triggers.phase = False
            Triggers.task_2 = False

            taskMgr.add(self.update_phase_2, 'Phase task', extraArgs=[phase], appendTask=True)

        return

    def update_phase_2(self, phase, task):

        if phase == 0:

            if self.text_counter < len(self.phase_0_list):

                # List has to be in update_text function otherwise sub-phase starts at same time as last message

                text_list = self.phase_0_text[self.text_counter]
                text_delay = self.phase_0_delay[self.text_counter]
                text_time = self.phase_0_text_time[self.text_counter]

                taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                      extraArgs=[text_list, self.phase_0_list, self.text_counter, text_time],
                                      appendTask=True)

                self.text_counter += 1

            elif all(self.phase_0_list):

                self.update_phase_3(phase)

                self.text3.setText("Press 'i' to arm the thruster")
                self.text3_NP.reparentTo(self.aspect2d)

                self.text_counter = 0

                Triggers.phase_sub = True
                Triggers.task_1 = False

                return task.done

        if phase == 1:

            if Triggers.phase_1:

                text_list = list("Thruster armed, it will start in ")

                start_time_stringer = str(round(Trajectory.launch_1_time - Physics.time))

                time_stringer = start_time_stringer + ' seconds _'
                time_stringer_list = list(time_stringer)

                for i in range(len(time_stringer_list)):
                    text_list.append(time_stringer_list[i])

                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.phase_1 = False

            if Physics.time < (Trajectory.launch_1_time - Trajectory.launch_1_time_sound_start):
                Triggers.sound_launch = True

            if Physics.time >= (Trajectory.launch_1_time - Trajectory.launch_1_time_sound_start) and \
                    Triggers.sound_launch:
                self.sound_launch_1.play()

                Triggers.sound_launch = False

            if Physics.time >= (Trajectory.launch_1_time - self.phase_1_total_text_time):

                if self.text_counter < len(self.phase_1_list):
                    text_list = self.phase_1_text[self.text_counter]
                    text_delay = self.phase_1_delay[self.text_counter]
                    text_time = self.phase_1_text_time[self.text_counter]

                    taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                          extraArgs=[text_list, self.phase_1_list, self.text_counter, text_time],
                                          appendTask=True)

                    self.text_counter += 1

            if Triggers.launch:
                if Physics.time >= Trajectory.launch_1_time:

                    self.update_particles('fire', True, (0, 0, 0), (0, 0, 90))

                    Trajectory.thruster_x = Satellite.vx / Satellite.v
                    Trajectory.thruster_y = Satellite.vy / Satellite.v
                    Trajectory.thruster_z = Satellite.vz / Satellite.v

                    Triggers.alignment_auto = False
                    Triggers.thruster = True
                    Triggers.launch = False
                    Triggers.transfer_1 = True

            if Physics.time >= (Trajectory.launch_1_time + Trajectory.launch_1_time_difference):

                self.update_particles('fire', False, (0, 0, 0), (0, 0, 0))
                self.update_phase_3(phase)

                Triggers.thruster = False
                Triggers.launch = True

                self.text_counter = 0

                self.update_phase_1()

                return task.done

        if phase == 2:

            if self.text_counter < len(self.phase_2_list):

                # List has to be in update_text function otherwise sub-phase starts at same time as last message

                text_list = self.phase_2_text[self.text_counter]
                text_delay = self.phase_2_delay[self.text_counter]
                text_time = self.phase_2_text_time[self.text_counter]

                taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                      extraArgs=[text_list, self.phase_2_list, self.text_counter, text_time],
                                      appendTask=True)

                self.text_counter += 1

            elif all(self.phase_2_list):

                self.sound_background_1.play()

                self.update_phase_3(phase)

                self.text3.setText("Press 'i' to initialize the transfer skip")
                self.text3_NP.reparentTo(self.aspect2d)

                self.text_counter = 0

                Triggers.phase_sub = True
                Triggers.task_1 = False

                return task.done

        if phase == 3:

            if Triggers.skip:

                Triggers.skip = False
                Triggers.alignment_auto = True

                self.update_skip_1()

                self.parentNodeCam.setHpr(-90, 40, -90)

            if self.text_counter < len(self.phase_3_list):

                # List has to be in update_text function otherwise sub-phase starts at same time as last message

                text_list = self.phase_3_text[self.text_counter]
                text_delay = self.phase_3_delay[self.text_counter]
                text_time = self.phase_3_text_time[self.text_counter]

                taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                      extraArgs=[text_list, self.phase_3_list, self.text_counter, text_time],
                                      appendTask=True)

                self.text_counter += 1

            elif all(self.phase_3_list):

                self.update_phase_3(phase)

                self.text3.setText("Press 'i' to initialize the alignment")
                self.text3_NP.reparentTo(self.aspect2d)

                self.text_counter = 0

                Triggers.phase_sub = True
                Triggers.task_1 = False
                Triggers.alignment = True
                Triggers.skip = True

                return task.done

        if phase == 4:

            if Triggers.alignment:

                if not Triggers.reverse:
                    Triggers.reverse = True

                    # Turn right

                    self.update_particles('air', True, (0.82, 0, 1.25), (0, 0, 90))

                if Trajectory.turn_angle < - 90 and Triggers.flip:
                    # Turn left / stop turn

                    self.update_particles('air', True, (0.82, 0, 1.75), (0, 0, - 90))

                    Triggers.flip = False

                if Trajectory.turn_angle == - 180:
                    Triggers.alignment = False

                    self.update_particles('air', False, (0, 0, 0), (0, 0, 0))

            if not Triggers.alignment:

                if self.text_counter < len(self.phase_4_list):

                    # List has to be in update_text function otherwise sub-phase starts at same time as last message

                    text_list = self.phase_4_text[self.text_counter]
                    text_delay = self.phase_4_delay[self.text_counter]
                    text_time = self.phase_4_text_time[self.text_counter]

                    taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                          extraArgs=[text_list, self.phase_4_list, self.text_counter, text_time],
                                          appendTask=True)

                    self.text_counter += 1

                elif all(self.phase_4_list):

                    self.update_phase_3(phase)

                    self.text3.setText("Press 'i' to re-arm the thruster")
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.text_counter = 0

                    Triggers.phase_sub = True
                    Triggers.task_1 = False

                    return task.done

        if phase == 5:

            if Triggers.phase_5:

                text_list = list("Thruster re-armed, it will start in ")

                start_time_stringer = str(round(Trajectory.launch_2_time -
                                                (Trajectory.transfer_1_time_elapsed / Trajectory.time_factor)))

                time_stringer = start_time_stringer + ' seconds _'
                time_stringer_list = list(time_stringer)

                for i in range(len(time_stringer_list)):
                    text_list.append(time_stringer_list[i])

                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.phase_5 = False

            if Trajectory.transfer_1_time_elapsed > (ToMoon.transfer_time_1_elapsed +
                                                     (1.2 * Trajectory.time_factor * self.sound_background_1_length)) \
                    and Triggers.sound:
                self.sound_background_2.play()

                Triggers.sound = False

            if (Trajectory.transfer_1_time_elapsed / Trajectory.time_factor) < \
                    (Trajectory.launch_2_time - Trajectory.launch_2_time_sound_start):
                Triggers.sound_launch = True

            if (Trajectory.transfer_1_time_elapsed / Trajectory.time_factor) >= \
                    (Trajectory.launch_2_time - Trajectory.launch_2_time_sound_start) and Triggers.sound_launch:
                self.sound_launch_2.play()

                Triggers.sound_launch = False

            if (Trajectory.transfer_1_time_elapsed / Trajectory.time_factor) >= \
                    (Trajectory.launch_2_time - self.phase_5_total_text_time):

                if self.text_counter < len(self.phase_5_list):
                    text_list = self.phase_5_text[self.text_counter]
                    text_delay = self.phase_5_delay[self.text_counter]
                    text_time = self.phase_5_text_time[self.text_counter]

                    taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                          extraArgs=[text_list, self.phase_5_list, self.text_counter, text_time],
                                          appendTask=True)

                    self.text_counter += 1

            if Triggers.launch:
                if (Trajectory.transfer_1_time_elapsed / Trajectory.time_factor) >= Trajectory.launch_2_time:

                    self.update_particles('fire', True, (0, 0, 0), (0, 0, 90))

                    Trajectory.thruster_x = Satellite.vx / Satellite.v
                    Trajectory.thruster_y = Satellite.vy / Satellite.v
                    Trajectory.thruster_z = Satellite.vz / Satellite.v

                    Triggers.alignment_auto = False
                    Triggers.thruster = True
                    Triggers.launch = False
                    Triggers.transfer_1 = False
                    Triggers.transfer_2 = True

            if (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor) >= Trajectory.launch_2_time_difference:

                self.update_particles('fire', False, (0, 0, 0), (0, 0, 0))
                self.update_phase_3(phase)

                Triggers.thruster = False
                Triggers.launch = True
                Triggers.sound_launch = True

                self.text_counter = 0

                self.update_phase_1()

                return task.done

        if phase == 6:

            if self.text_counter < len(self.phase_6_list):

                # List has to be in update_text function otherwise sub-phase starts at same time as last message

                text_list = self.phase_6_text[self.text_counter]
                text_delay = self.phase_6_delay[self.text_counter]
                text_time = self.phase_6_text_time[self.text_counter]

                taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                      extraArgs=[text_list, self.phase_6_list, self.text_counter, text_time],
                                      appendTask=True)

                self.text_counter += 1

            elif all(self.phase_6_list):

                self.update_phase_3(phase)

                self.text3.setText("Press 'i' to initialize the second transfer skip")
                self.text3_NP.reparentTo(self.aspect2d)

                self.text_counter = 0

                Triggers.phase_sub = True
                Triggers.task_1 = False

                return task.done

        if phase == 7:

            if Triggers.skip:

                Triggers.alignment_auto = True
                Triggers.skip = False

                self.update_skip_2()

                self.parentNodeCam.setHpr(-90, -30, -90)

            if self.text_counter < len(self.phase_7_list):

                # List has to be in update_text function otherwise sub-phase starts at same time as last message

                text_list = self.phase_7_text[self.text_counter]
                text_delay = self.phase_7_delay[self.text_counter]
                text_time = self.phase_7_text_time[self.text_counter]

                taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                      extraArgs=[text_list, self.phase_7_list, self.text_counter, text_time],
                                      appendTask=True)

                self.text_counter += 1

            elif all(self.phase_7_list):

                self.update_phase_3(phase)

                self.text3.setText("Press 'i' to re-arm the thruster")
                self.text3_NP.reparentTo(self.aspect2d)

                self.text_counter = 0

                Triggers.phase_sub = True
                Triggers.task_1 = False

                return task.done

        if phase == 8:

            if Triggers.phase_8:

                text_list = list("Thruster re-armed, it will start in ")

                start_time_stringer = str(round(Trajectory.launch_3_time -
                                                (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor)))

                time_stringer = start_time_stringer + ' seconds _'
                time_stringer_list = list(time_stringer)

                for i in range(len(time_stringer_list)):
                    text_list.append(time_stringer_list[i])

                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.phase_8 = False

            if (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor) < \
                    (Trajectory.launch_3_time - Trajectory.launch_3_time_sound_start):
                Triggers.sound_launch = True

            if (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor) >= \
                    (Trajectory.launch_3_time - Trajectory.launch_3_time_sound_start) and Triggers.sound_launch:
                self.sound_launch_3.play()

                Triggers.sound_launch = False

            if (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor) >= \
                    (Trajectory.launch_3_time - self.phase_8_total_text_time):

                if self.text_counter < len(self.phase_8_list):
                    text_list = self.phase_8_text[self.text_counter]
                    text_delay = self.phase_8_delay[self.text_counter]
                    text_time = self.phase_8_text_time[self.text_counter]

                    taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                          extraArgs=[text_list, self.phase_8_list, self.text_counter, text_time],
                                          appendTask=True)

                    self.text_counter += 1

            if Triggers.launch:
                if (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor) >= Trajectory.launch_3_time:

                    self.update_particles('fire', True, (0, 0, 0), (0, 0, 90))

                    Trajectory.thruster_x = Satellite.vx / Satellite.v
                    Trajectory.thruster_y = Satellite.vy / Satellite.v
                    Trajectory.thruster_z = Satellite.vz / Satellite.v

                    Triggers.thruster = True
                    Triggers.launch = False

            if (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor) >= Trajectory.launch_3_time + \
                    Trajectory.launch_3_time_difference:

                self.update_particles('fire', False, (0, 0, 0), (0, 0, 0))
                self.update_phase_3(phase)

                Triggers.thruster = False
                Triggers.launch = True
                Triggers.sound_launch = True
                Triggers.sound = True

                self.text_counter = 0

                self.update_phase_1()

                return task.done

        if phase == 9:

            if self.text_counter < len(self.phase_9_list):

                # List has to be in update_text function otherwise sub-phase starts at same time as last message

                text_list = self.phase_9_text[self.text_counter]
                text_delay = self.phase_9_delay[self.text_counter]
                text_time = self.phase_9_text_time[self.text_counter]

                taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                      extraArgs=[text_list, self.phase_9_list, self.text_counter, text_time],
                                      appendTask=True)

                self.text_counter += 1

            if self.phase_9_list[0] and Triggers.sound:
                self.sound_background_3.play()

                Triggers.sound = False

            if (Trajectory.transfer_2_time_elapsed / Trajectory.time_factor) >= Trajectory.launch_3_time + \
                    Trajectory.launch_3_time_difference + self.sound_background_3_length + 10:

                text_list = list("Thank you for using the program, I hope you enjoyed it!  "
                                 "You can exit at any time _")
                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                return task.done

        Triggers.task_1 = True

        return task.cont

    def update_phase_3(self, phase):

        Triggers.phases[phase] = False
        Triggers.phases[phase + 1] = True
        Triggers.phase = True

        self.minor_trigger = True
        self.major_trigger = True

        return

    def update_particles(self, system, toggle, pos, hpr):

        if toggle:
            if system == 'air':
                self.PE_1.loadConfig('Configurations/Air.ptf')
                self.PE_2.loadConfig('Configurations/Air.ptf')

                self.PE_1.setPos(pos)
                self.PE_1.setHpr(hpr)
                self.PE_1.setScale(0.1)

                self.PE_2.setPos(pos)
                self.PE_2.setHpr(hpr)
                self.PE_2.setScale(0.1)

                if self.PE_1.getZ() < 1.5:
                    self.PE_2.setZ(self.PE_1.getZ() + 0.5)
                else:
                    self.PE_2.setZ(self.PE_1.getZ() - 0.5)

                self.PE_2.setX(- self.PE_1.getX())
                self.PE_2.setR(self.PE_1.getR() - 180)

                self.PE_1.start(self.satellite)
                self.PE_2.start(self.satellite)

            else:
                self.PE_3.loadConfig('Configurations/Fire.ptf')

                self.PE_3.setPos(pos)
                self.PE_3.setHpr(hpr)
                self.PE_3.setScale(1)

                self.PE_3.start(self.satellite)

        else:
            self.PE_1.disable()
            self.PE_2.disable()
            self.PE_3.disable()

        return

    def update_warnings(self, task):

        phase = np.where(Triggers.phases)[0][0]

        if self.failure_trigger:
            self.text3.setText("MISSION FAILED" + "\n" + "press 'i' to exit")
            self.text3.setTextColor(1, 0, 0, 1)
            self.text3_NP.reparentTo(self.aspect2d)

            self.sound_warning_major.stop()

            return task.done

        if phase == 0:

            if abs(Satellite.earth_angle * (180 / np.pi)) < 1:
                self.failure_trigger = True

                return task.cont

            if abs(Satellite.earth_angle * (180 / np.pi)) < 10 and self.major_trigger:

                self.text3.setText("Warning: delta-V maneuver position near, arm the thruster now!")
                self.text3.setTextColor(1, 0, 0, 1)
                self.text3_NP.reparentTo(self.aspect2d)

                self.sound_warning_minor.stop()
                self.sound_warning_major.play()

                self.major_trigger = False

            elif abs(Satellite.earth_angle * (180 / np.pi)) < 30 and self.minor_trigger:

                self.text3.setText("Warning: delta-V maneuver position approaching, please arm the thruster!")
                self.text3.setTextColor(1, 0.65, 0, 1)
                self.text3_NP.reparentTo(self.aspect2d)

                self.sound_warning_minor.play()

                self.minor_trigger = False

        else:

            self.sound_warning_minor.stop()
            self.sound_warning_major.stop()

        return task.cont

    def update_skip_1(self):

        Trajectory.transfer_1_time_elapsed = ToMoon.transfer_time_1_elapsed

        Moon.vx = ToMoon.S_1_moon_vx
        Moon.vy = ToMoon.S_1_moon_vy
        Moon.vz = ToMoon.S_1_moon_vz
        Moon.v = np.sqrt(Moon.vx ** 2 + Moon.vy ** 2 + Moon.vz ** 2)

        Moon.x = ToMoon.S_1_moon_x
        Moon.y = ToMoon.S_1_moon_y
        Moon.z = ToMoon.S_1_moon_z
        Moon.d = np.sqrt(Moon.x ** 2 + Moon.y ** 2 + Moon.z ** 2)

        Satellite.vx = ToMoon.S_1_satellite_vx
        Satellite.vy = ToMoon.S_1_satellite_vy
        Satellite.vz = ToMoon.S_1_satellite_vz
        Satellite.v = np.sqrt(Satellite.vx ** 2 + Satellite.vy ** 2 + Satellite.vz ** 2)

        Satellite.x = ToMoon.S_1_satellite_x
        Satellite.y = ToMoon.S_1_satellite_y
        Satellite.z = ToMoon.S_1_satellite_z
        Satellite.d = np.sqrt(Satellite.x ** 2 + Satellite.y ** 2 + Satellite.z ** 2)

        return

    def update_skip_2(self):

        Trajectory.transfer_2_time_elapsed = ToMoon.transfer_time_2_elapsed

        Moon.vx = ToMoon.S_2_moon_vx
        Moon.vy = ToMoon.S_2_moon_vy
        Moon.vz = ToMoon.S_2_moon_vz
        Moon.v = np.sqrt(Moon.vx ** 2 + Moon.vy ** 2 + Moon.vz ** 2)

        Moon.x = ToMoon.S_2_moon_x
        Moon.y = ToMoon.S_2_moon_y
        Moon.z = ToMoon.S_2_moon_z
        Moon.d = np.sqrt(Moon.x ** 2 + Moon.y ** 2 + Moon.z ** 2)

        Satellite.vx = ToMoon.S_2_satellite_vx
        Satellite.vy = ToMoon.S_2_satellite_vy
        Satellite.vz = ToMoon.S_2_satellite_vz
        Satellite.v = np.sqrt(Satellite.vx ** 2 + Satellite.vy ** 2 + Satellite.vz ** 2)

        Satellite.x = ToMoon.S_2_satellite_x
        Satellite.y = ToMoon.S_2_satellite_y
        Satellite.z = ToMoon.S_2_satellite_z
        Satellite.d = np.sqrt(Satellite.x ** 2 + Satellite.y ** 2 + Satellite.z ** 2)

        return

    def update_self_2(self):

        if not Triggers.phase_sub:

            Triggers.task_2 = True

            Physics.save()
            Earth.save()
            Moon.save()
            Satellite.save()
            Trajectory.save()
            Triggers.save()

            Triggers.task_2 = False

            print('Progress saved!')

            print(round(Trajectory.transfer_1_time_elapsed))
            print(round(Trajectory.transfer_1_time))

        else:
            print('Progress could not be saved!')

        return

    def __init__(self):
        ShowBase.__init__(self)

        # Models

        self.scale = 10 ** 3
        self.sphere = 100

        self.earth = loader.loadModel("Models/Earth.gltf")
        self.earth.setScale(Earth.r / (self.scale * self.sphere))
        self.earth.setHpr(0, -23, 0)
        self.earth.reparentTo(render)

        self.moon = loader.loadModel("Models/Moon.gltf")
        self.moon.setScale(Moon.r / (self.scale * self.sphere))
        self.moon.reparentTo(render)

        self.satellite = loader.loadModel("Models/Satellite2.gltf")
        self.satellite.setScale(1)
        self.satellite.setHpr(Satellite.angle_yaw, 90, 90)
        self.satellite.reparentTo(render)

        self.sun = loader.loadModel("Models/Sun.gltf")
        self.sun.setScale(40)
        self.sun.setPos(-300000, 0, 0)
        self.sun.reparentTo(render)
        self.sun.setLightOff(True)

        self.sky = loader.loadModel('Models/Sky.gltf')
        self.sky.setScale(300000)
        self.sky.reparentTo(render)
        self.sky.setLightOff(True)

        # Lights

        self.directionalLightScene = pc.DirectionalLight('dLightScene')
        self.directionalLightScene.setColor((2.0, 2.0, 2.0, 1))
        self.directionalLightSceneNP = render.attachNewNode(self.directionalLightScene)
        self.directionalLightSceneNP.setHpr(-90, 0, 0)

        self.earth.setLight(self.directionalLightSceneNP)
        self.moon.setLight(self.directionalLightSceneNP)

        self.directionalLightSat = pc.DirectionalLight('dLightSat')
        self.directionalLightSatNP = render.attachNewNode(self.directionalLightSat)
        self.directionalLightSatNP.setHpr(-90, 0, 0)

        self.ambientLight = pc.AmbientLight('ambientLight')
        self.ambientLight.setColor((0.02, 0.02, 0.02, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        self.render.setLight(self.ambientLightNP)

        self.ambientLightParticles = pc.AmbientLight('ambientLight')
        self.ambientLightParticles.setColor((1.0, 1.0, 1.0, 1))
        self.ambientLightParticlesNP = render.attachNewNode(self.ambientLightParticles)

        # Filters

        self.filters = CommonFilters(base.win, base.cam)
        self.filters.setBloom(blend=(0, 0, 0, 1), desat=-0.1, intensity=0.3,
                              size=2)

        # Antialiasing

        render.setAntialias(pc.AntialiasAttrib.MAuto)

        # Camera

        self.parentNodeCam = render.attachNewNode('parentCam')
        self.parentNodeCam.reparentTo(self.satellite)
        self.parentNodeCam.setHpr(-90, -35, -90)

        self.cam.reparentTo(self.parentNodeCam)
        self.cam.lookAt(self.parentNodeCam)
        self.cam.setPos(0, -30, 0)

        # Key commands

        self.disableMouse()

        self.accept("escape", sys.exit)

        self.accept('wheel_up', lambda: self.cam.setY(self.cam.getY() + 10))
        self.accept('wheel_down', lambda: self.cam.setY(self.cam.getY() - 10))

        self.accept("w", lambda: self.parentNodeCam.setH(self.parentNodeCam.getH() + 2))
        self.accept("s", lambda: self.parentNodeCam.setH(self.parentNodeCam.getH() - 2))

        self.accept("w-repeat", lambda: self.parentNodeCam.setH(self.parentNodeCam.getH() + 2))
        self.accept("s-repeat", lambda: self.parentNodeCam.setH(self.parentNodeCam.getH() - 2))

        self.accept("d", lambda: self.parentNodeCam.setP(self.parentNodeCam.getP() + 2))
        self.accept("a", lambda: self.parentNodeCam.setP(self.parentNodeCam.getP() - 2))

        self.accept("d-repeat", lambda: self.parentNodeCam.setP(self.parentNodeCam.getP() + 2))
        self.accept("a-repeat", lambda: self.parentNodeCam.setP(self.parentNodeCam.getP() - 2))

        self.accept("x", lambda: self.parentNodeCam.setHpr(-90, -30, -90))

        self.accept("m", self.update_self_2)

        # Particles

        self.enableParticles()

        self.PE_1 = ParticleEffect()
        self.PE_2 = ParticleEffect()
        self.PE_3 = ParticleEffect()

        self.PE_1.setLight(self.ambientLightParticlesNP)
        self.PE_2.setLight(self.ambientLightParticlesNP)
        self.PE_3.setLight(self.ambientLightParticlesNP)

        # Text

        self.dash_speed = 0.4
        self.symbol_speed = 0.01
        self.symbol_counter = 0

        self.time_symbol_reference = 0
        self.time_dash_reference = 0
        self.time_total = 0

        self.text_display_time = 6
        self.text_counter = 0

        self.font = loader.loadFont('Fonts/Space.otf')

        self.text = pc.TextNode('Board computer')
        self.text.setFont(self.font)
        self.text.setTextColor(1, 1, 1, 1)
        self.text.setAlign(pc.TextNode.ALeft)
        self.text.setShadow(0.1, 0.1)
        self.text.setShadowColor(0, 0, 0, 1)
        self.text.setWordwrap(30)
        self.text.setFrameColor(0, 0, 0, 1)
        self.text.setFrameAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text.setCardColor(0, 0, 0, 0.6)
        self.text.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text_NP = render.attachNewNode(self.text)
        self.text_NP.setScale(0.05)
        self.text_NP.setPos(0.1, 0, -0.12)

        self.text2 = pc.TextNode('Camera menu')
        self.text2.setFont(self.font)
        self.text2.setTextColor(1, 1, 1, 1)
        self.text2.setAlign(pc.TextNode.ACenter)
        self.text2.setShadow(0.1, 0.1)
        self.text2.setShadowColor(0, 0, 0, 1)
        self.text2.setFrameColor(0, 0, 0, 1)
        self.text2.setFrameAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text2.setCardColor(0, 0, 0, 0.6)
        self.text2.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text2_NP = render.attachNewNode(self.text2)
        self.text2_NP.setScale(0.05)
        self.text2_NP.setPos(-0.38, 0, 0.58)
        self.text2_trigger = False

        self.accept("c", lambda: self.update_menus('controls', True) if not self.text2_trigger else self.update_menus(
            'controls', False))

        self.text3 = pc.TextNode('Sub-phase menu')
        self.text3.setFont(self.font)
        self.text3.setTextColor(1, 1, 1, 1)
        self.text3.setAlign(pc.TextNode.ACenter)
        self.text3.setShadow(0.1, 0.1)
        self.text3.setShadowColor(0, 0, 0, 1)
        self.text3.setFrameColor(0, 0, 0, 1)
        self.text3.setFrameAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text3.setCardColor(0, 0, 0, 0.6)
        self.text3.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text3_NP = render.attachNewNode(self.text3)
        self.text3_NP.setScale(0.05)
        self.text3_NP.setPos(0, 0, 0)

        if Triggers.phase_0:

            self.text3.setText("Press 'i' to initialize")
            self.text3_NP.reparentTo(self.aspect2d)

            Triggers.phase_0 = False

        self.text4 = pc.TextNode('Trajectory menu')
        self.text4.setFont(self.font)
        self.text4.setAlign(pc.TextNode.ACenter)
        self.text4.setShadow(0.1, 0.1)
        self.text4.setShadowColor(0, 0, 0, 1)
        self.text4.setFrameColor(0, 0, 0, 1)
        self.text4.setFrameAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text4.setCardColor(0, 0, 0, 0.6)
        self.text4.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text4_NP = render.attachNewNode(self.text4)
        self.text4_NP.setScale(0.05)
        self.text4_NP.setPos(0.6, 0, 0.35)
        self.text4_trigger = False

        self.accept("t", lambda: self.update_menus('trajectory', True) if not self.text4_trigger else self.update_menus(
            'trajectory', False))

        self.text5 = pc.TextNode('Time menu')
        self.text5.setFont(self.font)
        self.text5.setAlign(pc.TextNode.ARight)
        self.text5.setShadow(0.1, 0.1)
        self.text5.setShadowColor(0, 0, 0, 1)
        self.text5.setFrameColor(0, 0, 0, 1)
        self.text5.setFrameAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text5.setCardColor(0, 0, 0, 0.6)
        self.text5.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text5_NP = render.attachNewNode(self.text5)
        self.text5_NP.setScale(0.05)
        self.text5_NP.setPos(-0.1, 0, -0.12)

        # Sounds

        self.sound_typing = loader.loadSfx('Sounds/Typing.ogg')
        self.sound_typing.setVolume(0.1)
        self.sound_typing.setLoop(True)

        self.sound_warning_minor = loader.loadSfx('Sounds/Warning_minor.ogg')
        self.sound_warning_minor.setVolume(0.1)
        self.sound_warning_minor.setLoop(True)

        self.sound_warning_major = loader.loadSfx('Sounds/Warning_major.ogg')
        self.sound_warning_major.setVolume(0.1)
        self.sound_warning_major.setLoop(True)

        self.sound_launch_1 = loader.loadSfx('Sounds/Launch_1.ogg')
        self.sound_launch_1.setVolume(1.0)

        self.sound_launch_2 = loader.loadSfx('Sounds/Launch_2.ogg')
        self.sound_launch_2.setVolume(1.0)

        self.sound_launch_3 = loader.loadSfx('Sounds/Launch_3.ogg')
        self.sound_launch_3.setVolume(1.0)

        self.sound_background_1 = loader.loadSfx('Sounds/Background_1.ogg')
        self.sound_background_1.setVolume(1.0)
        self.sound_background_1_length = 101
        self.sound_background_1_time = 30

        self.sound_background_2 = loader.loadSfx('Sounds/Background_2.ogg')
        self.sound_background_2.setVolume(0.6)
        self.sound_background_2_length = 282

        self.sound_background_3 = loader.loadSfx('Sounds/Background_3.ogg')
        self.sound_background_3.setVolume(1.0)
        self.sound_background_3_length = 208

        # Logic

        self.failure_trigger = False
        self.minor_trigger = True
        self.major_trigger = True

        self.accept('i', self.update_phase_1)

        # Phase 0

        self.phase_0_text = [list("Welcome aboard the Apollo 11 command module _"),
                             list("The module is currently orbiting the Earth at 4000 km and is expected to reach the "
                                  "Moon in a few days _"),
                             list("You are tasked to navigate the module towards the Moon and into a 1000 km orbit _"),
                             list("The trajectory calculations have already been done by me, the onboard computer _"),
                             list("I am however not permitted to initiate the thrusters myself and will therefore ask "
                                  "for your control input at certain times _"),
                             list("During the journey you can enjoy the view by rotating the camera, press 'c' to view "
                                  "the camera control menu and again to hide it _"),
                             list("You can also keep track of the trajectory by pressing 't' and again to hide the "
                                  "menu _"),
                             list("The first step is to arm the module's thruster in preparation for the first "
                                  "transfer _"),
                             list("It will engage at precisely the right moment to enter the Hohmann transfer orbit "
                                  "towards the Moon _")]

        self.phase_0_list = np.zeros(len(self.phase_0_text), dtype=bool)
        self.phase_0_delay = np.zeros(len(self.phase_0_text))
        self.phase_0_text_time = np.zeros(len(self.phase_0_text))
        self.phase_0_text_time[0] = self.text_display_time + len(self.phase_0_text[0]) * self.symbol_speed

        for i in range(len(self.phase_0_list) - 1):
            self.phase_0_text_time[i + 1] = self.text_display_time + len(self.phase_0_text[i + 1]) * self.symbol_speed
            self.phase_0_delay[i + 1] = self.phase_0_delay[i] + self.phase_0_text_time[i]

        # Phase 1

        self.phase_1_text = [list("Initiating start sequence _"),
                             list("Earth attitude alignment: disabled _"),
                             list("Fuel booster pumps: on _"),
                             list("System pressures: checked _"),
                             list("Ignition: on _"),
                             list("Main engine start in: _"),
                             list("5 _"),
                             list("4 _"),
                             list("3 _"),
                             list("2 _"),
                             list("1 _")]

        self.phase_1_list = np.zeros(len(self.phase_1_text), dtype=bool)
        self.phase_1_delay = np.zeros(len(self.phase_1_text))
        self.phase_1_text_time = np.zeros(len(self.phase_1_text))
        self.phase_1_text_time[0] = self.text_display_time + len(self.phase_1_text[0]) * self.symbol_speed

        for i in range(len(self.phase_1_list) - 1):

            if i < (len(self.phase_1_list) - 6):

                text_display_time = 3

                self.phase_1_text_time[i + 1] = text_display_time + len(self.phase_1_text[i + 1]) * self.symbol_speed
                self.phase_1_delay[i + 1] = self.phase_1_delay[i] + self.phase_1_text_time[i]

            else:

                text_display_time = 1

                self.phase_1_text_time[i + 1] = text_display_time + len(self.phase_1_text[i + 1]) * self.symbol_speed
                self.phase_1_delay[i + 1] = self.phase_1_delay[i] + self.phase_1_text_time[i]

        self.phase_1_total_text_time = sum(self.phase_1_text_time)

        # Phase 2

        self.phase_2_text = [list("Delta-V maneuver completed, main engine shut down _"),
                             list("The journey towards the Moon will take roughly 4 days and about 10 hours in this "
                                  "simulation _"),
                             list("Fortunately the major part of the transfer can be skipped, bringing the module "
                                  "close to the second transfer around the Moon _"),
                             list("In this case both corrective burns during the first transfer will be completed and "
                                  "all that remains is the attitude change before the second transfer _")]

        self.phase_2_list = np.zeros(len(self.phase_2_text), dtype=bool)
        self.phase_2_delay = np.zeros(len(self.phase_2_text))
        self.phase_2_text_time = np.zeros(len(self.phase_2_text))
        self.phase_2_text_time[0] = self.text_display_time + len(self.phase_2_text[0]) * self.symbol_speed

        for i in range(len(self.phase_2_list) - 1):
            self.phase_2_text_time[i + 1] = self.text_display_time + len(self.phase_2_text[i + 1]) * self.symbol_speed
            self.phase_2_delay[i + 1] = self.phase_2_delay[i] + self.phase_2_text_time[i]

        # Phase 3

        self.phase_3_text = [list("Skip completed, the module has now completed 98% of the first transfer _"),
                             list("The second transfer is about 10 minutes away and requires a deceleration _"),
                             list("In order to do so the module has to be turned 180 degrees and aligned with the "
                                  "Lunar surface using the attitude controller _")]

        self.phase_3_list = np.zeros(len(self.phase_3_text), dtype=bool)
        self.phase_3_delay = np.zeros(len(self.phase_3_text))
        self.phase_3_text_time = np.zeros(len(self.phase_3_text))
        self.phase_3_text_time[0] = self.text_display_time + len(self.phase_3_text[0]) * self.symbol_speed

        for i in range(len(self.phase_3_list) - 1):
            self.phase_3_text_time[i + 1] = self.text_display_time + len(self.phase_3_text[i + 1]) * self.symbol_speed
            self.phase_3_delay[i + 1] = self.phase_3_delay[i] + self.phase_3_text_time[i]

        # Phase 4

        self.phase_4_text = [list("Alignment completed _"),
                             list("All that remains is to re-arm the thruster for the second transfer _")]

        self.phase_4_list = np.zeros(len(self.phase_4_text), dtype=bool)
        self.phase_4_delay = np.zeros(len(self.phase_4_text))
        self.phase_4_text_time = np.zeros(len(self.phase_4_text))
        self.phase_4_text_time[0] = self.text_display_time + len(self.phase_4_text[0]) * self.symbol_speed

        for i in range(len(self.phase_4_list) - 1):
            self.phase_4_text_time[i + 1] = self.text_display_time + len(self.phase_4_text[i + 1]) * self.symbol_speed
            self.phase_4_delay[i + 1] = self.phase_4_delay[i] + self.phase_4_text_time[i]

        # Phase 5

        self.phase_5_text = [list("Initiating second start sequence _"),
                             list("Fuel booster pumps: on _"),
                             list("System pressures: checked _"),
                             list("Ignition: on _"),
                             list("Main engine start in: _"),
                             list("5 _"),
                             list("4 _"),
                             list("3 _"),
                             list("2 _"),
                             list("1 _")]

        self.phase_5_list = np.zeros(len(self.phase_5_text), dtype=bool)
        self.phase_5_delay = np.zeros(len(self.phase_5_text))
        self.phase_5_text_time = np.zeros(len(self.phase_5_text))
        self.phase_5_text_time[0] = self.text_display_time + len(self.phase_5_text[0]) * self.symbol_speed

        for i in range(len(self.phase_5_list) - 1):

            if i < (len(self.phase_5_list) - 6):

                text_display_time = 3

                self.phase_5_text_time[i + 1] = text_display_time + len(self.phase_5_text[i + 1]) * self.symbol_speed
                self.phase_5_delay[i + 1] = self.phase_5_delay[i] + self.phase_5_text_time[i]

            else:

                text_display_time = 1

                self.phase_5_text_time[i + 1] = text_display_time + len(self.phase_5_text[i + 1]) * self.symbol_speed
                self.phase_5_delay[i + 1] = self.phase_5_delay[i] + self.phase_5_text_time[i]

        self.phase_5_total_text_time = sum(self.phase_5_text_time)

        # Phase 6

        self.phase_6_text = [list("Second delta-V maneuver completed, main engine shut down _"),
                             list("The second transfer takes about 25 minutes in this simulation _"),
                             list("It transfers the module from its current height to the final orbit of 1000 km _"),
                             list("Again, the major part of this transfer can be skipped to bring the module close to "
                                  "the final delta-V maneuver _")]

        self.phase_6_list = np.zeros(len(self.phase_6_text), dtype=bool)
        self.phase_6_delay = np.zeros(len(self.phase_6_text))
        self.phase_6_text_time = np.zeros(len(self.phase_6_text))
        self.phase_6_text_time[0] = self.text_display_time + len(self.phase_6_text[0]) * self.symbol_speed

        for i in range(len(self.phase_6_list) - 1):
            self.phase_6_text_time[i + 1] = self.text_display_time + len(self.phase_6_text[i + 1]) * self.symbol_speed
            self.phase_6_delay[i + 1] = self.phase_6_delay[i] + self.phase_6_text_time[i]

        # Phase 7

        self.phase_7_text = [list("Second skip completed, the module has now completed 70% of the second transfer _"),
                             list("The final delta-V maneuver is about 4 minutes away and it is required that you arm "
                                  "the module's thruster one last time _")]

        self.phase_7_list = np.zeros(len(self.phase_7_text), dtype=bool)
        self.phase_7_delay = np.zeros(len(self.phase_7_text))
        self.phase_7_text_time = np.zeros(len(self.phase_7_text))
        self.phase_7_text_time[0] = self.text_display_time + len(self.phase_7_text[0]) * self.symbol_speed

        for i in range(len(self.phase_7_list) - 1):
            self.phase_7_text_time[i + 1] = self.text_display_time + len(self.phase_7_text[i + 1]) * self.symbol_speed
            self.phase_7_delay[i + 1] = self.phase_7_delay[i] + self.phase_7_text_time[i]

        # Phase 8

        self.phase_8_text = [list("Initiating final start sequence _"),
                             list("Lunar attitude alignment: enabled _"),
                             list("Fuel booster pumps: on _"),
                             list("System pressures: checked _"),
                             list("Ignition: on _"),
                             list("Main engine start in: _"),
                             list("5 _"),
                             list("4 _"),
                             list("3 _"),
                             list("2 _"),
                             list("1 _")]

        self.phase_8_list = np.zeros(len(self.phase_8_text), dtype=bool)
        self.phase_8_delay = np.zeros(len(self.phase_8_text))
        self.phase_8_text_time = np.zeros(len(self.phase_8_text))
        self.phase_8_text_time[0] = self.text_display_time + len(self.phase_8_text[0]) * self.symbol_speed

        for i in range(len(self.phase_8_list) - 1):

            if i < (len(self.phase_8_list) - 6):

                text_display_time = 3

                self.phase_8_text_time[i + 1] = text_display_time + len(self.phase_8_text[i + 1]) * self.symbol_speed
                self.phase_8_delay[i + 1] = self.phase_8_delay[i] + self.phase_8_text_time[i]

            else:

                text_display_time = 1

                self.phase_8_text_time[i + 1] = text_display_time + len(self.phase_8_text[i + 1]) * self.symbol_speed
                self.phase_8_delay[i + 1] = self.phase_8_delay[i] + self.phase_8_text_time[i]

        self.phase_8_total_text_time = sum(self.phase_8_text_time)

        # Phase 9

        self.phase_9_text = [list("Welcome _"),
                             list("To the Moon _")]

        self.phase_9_list = np.zeros(len(self.phase_9_text), dtype=bool)
        self.phase_9_delay = np.zeros(len(self.phase_9_text))
        self.phase_9_text_time = np.zeros(len(self.phase_9_text))
        self.phase_9_text_time[0] = self.text_display_time + len(self.phase_9_text[0]) * self.symbol_speed

        for i in range(len(self.phase_9_list) - 1):
            self.phase_9_text_time[i + 1] = self.text_display_time + len(self.phase_9_text[i + 1]) * self.symbol_speed
            self.phase_9_delay[i + 1] = self.phase_9_delay[i] + self.phase_9_text_time[i]

        # Tasks

        taskMgr.add(self.update_physics, 'Physics task')
        taskMgr.add(self.update_light, 'Light task')
        taskMgr.add(self.update_warnings, 'Warnings task')

        if Triggers.task_1:
            self.update_phase_1()


game = Main()
game.run()
