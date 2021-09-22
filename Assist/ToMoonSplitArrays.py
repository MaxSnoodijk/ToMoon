from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.particles.ParticleEffect import ParticleEffect
from pathlib import Path

import numpy as np
import panda3d.core as pc
import sys
import pickle
import os

pc.loadPrcFile('Configurations/Config.prc')

configuration = 'n'


class Data:

    folder_position = 'Data_temp/Position/'
    folder_position_time = 'Data_temp/Position_time/'
    folder_time = 'Data_temp/Time/'

    position_files = os.listdir(folder_position)
    position_time_files = os.listdir(folder_position_time)
    time_files = os.listdir(folder_time)

    position = np.genfromtxt(folder_position + position_files[0])
    position_time = np.genfromtxt(folder_position_time + position_time_files[0])
    position_time_passed = 0
    time = np.genfromtxt(folder_time + time_files[0])
    time_step = 25

    count = 0


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
            self.time_simulation = Data.time[0] * 0.7
            self.time_entry = round(self.time_simulation / Data.time_step)
            self.time_skip = 0.98 * (Data.time[1] - Data.time[0]) + Data.time[0]

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

            self.x = Data.position[Physics.time_entry, 4]
            self.y = Data.position[Physics.time_entry, 5]
            self.z = 0
            self.d = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

            self.vx = Data.position[Physics.time_entry, 6]
            self.vy = Data.position[Physics.time_entry, 7]
            self.vz = 0
            self.v = np.sqrt(self.vx ** 2 + self.vy ** 2 + self.vz ** 2)

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

            self.x = Data.position[Physics.time_entry, 0]
            self.y = Data.position[Physics.time_entry, 1]
            self.z = 0
            self.d = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

            self.vx = Data.position[Physics.time_entry, 2]
            self.vy = Data.position[Physics.time_entry, 3]
            self.vz = 0
            self.v = np.sqrt(self.vx ** 2 + self.vy ** 2 + self.vz ** 2)

            self.angle_earth = 0
            self.angle_moon = 0
            self.angle_yaw = (np.arctan(self.vy / self.vx)) * (180 / np.pi)

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

            # Time

            self.time_factor = 10

            # Launch 1

            self.launch_1_time = Data.time[0]
            self.launch_1_time_sound_start = 168
            self.launch_1_time_sound_stop = 234
            self.launch_1_time_difference = self.launch_1_time_sound_stop - self.launch_1_time_sound_start

            # Launch 2

            self.launch_2_time = Data.time[1]
            self.launch_2_time_sound_start = 155
            self.launch_2_time_sound_stop = 218
            self.launch_2_time_difference = self.launch_2_time_sound_stop - self.launch_2_time_sound_start

            # Launch 3

            self.launch_3_time = Data.time[2]
            self.launch_3_time_sound_start = 297
            self.launch_3_time_sound_stop = 317
            self.launch_3_time_difference = self.launch_3_time_sound_stop - self.launch_3_time_sound_start

            # Alignment

            self.turn_speed = 0
            self.turn_angle = 0
            self.angle_to_turn = 0

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
            self.phase_3 = True
            self.phase_4 = None
            self.phase_5 = True
            self.phase_6 = None
            self.phase_7 = None
            self.phase_8 = True
            self.phase_9 = True

            self.orbit_earth = True
            self.transfer_1 = False
            self.transfer_2 = False
            self.orbit_moon = False

            self.reverse = False

            self.alignment = False
            self.alignment_auto = True
            self.reverse = False
            self.flip = True

            self.launch = True

            self.decision = False

            self.time = False
            self.skip = False

            self.boost_1 = True
            self.boost_2 = True

            self.completed = False

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Triggers = Initial_Triggers()


class Main(ShowBase):

    def update_physics(self, task):

        dt = globalClock.getDt()

        Physics.time += dt

        if dt < 1:

            dt_simulation = dt * Trajectory.time_factor

            Physics.time_simulation += dt_simulation

            t = int(np.floor(Physics.time_simulation))

            if Physics.time_simulation > Data.position_time[Data.count]:

                Data.count += 1

                if (Data.count + 1) <= len(Data.position_files):
                    Data.position_time_passed = Data.position_time[Data.count - 1]
                    Data.position = np.genfromtxt(Data.folder_position + Data.position_files[Data.count])

                    if not Triggers.skip:
                        Physics.time_simulation = Data.position_time[Data.count - 1]

                else:
                    Physics.time_entry = len(Data.position) - 1
                    Triggers.completed = True

            Physics.time_entry = int(np.floor((Physics.time_simulation - Data.position_time_passed) / Data.time_step))

            if t % 25 == 0:

                Satellite.x = Data.position[Physics.time_entry, 0]
                Satellite.y = Data.position[Physics.time_entry, 1]
                Satellite.z = 0

                Satellite.vx = Data.position[Physics.time_entry, 2]
                Satellite.vy = Data.position[Physics.time_entry, 3]
                Satellite.vz = 0

                Moon.x = Data.position[Physics.time_entry, 4]
                Moon.y = Data.position[Physics.time_entry, 5]
                Moon.z = 0

                Moon.vx = Data.position[Physics.time_entry, 6]
                Moon.vy = Data.position[Physics.time_entry, 7]
                Moon.vz = 0

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

            if Triggers.reverse and not Triggers.alignment:

                if Triggers.alignment_auto:
                    Satellite.angle_yaw = (np.arctan(Satellite.vy / Satellite.vx)) * (180 / np.pi) - 180
                else:
                    Satellite.angle_yaw = (np.arctan((Satellite.vy - Moon.vy) / (Satellite.vx - Moon.vx))) * \
                                          (180 / np.pi) - 180

            elif Triggers.reverse and Triggers.alignment:

                if Trajectory.turn_angle < ((Trajectory.angle_to_turn / 2) + 1):
                    Trajectory.turn_speed += 0.001
                elif Trajectory.turn_angle < Trajectory.angle_to_turn:
                    Trajectory.turn_speed -= 0.001
                else:
                    Trajectory.turn_speed = 0
                    Trajectory.turn_angle = Trajectory.angle_to_turn

                Satellite.angle_yaw = (np.arctan(Satellite.vy / Satellite.vx)) * (180 / np.pi) + Trajectory.turn_angle

                Trajectory.turn_angle += Trajectory.turn_speed

            else:

                if Triggers.alignment_auto:
                    Satellite.angle_yaw = (np.arctan(Satellite.vy / Satellite.vx)) * (180 / np.pi)
                else:
                    Satellite.angle_yaw = (np.arctan((Satellite.vy - Moon.vy) / (Satellite.vx - Moon.vx))) * \
                                          (180 / np.pi)

            if Triggers.alignment_auto:
                if Satellite.vx > 0:
                    self.satellite.setH(Satellite.angle_yaw)
                else:
                    self.satellite.setH(180 + Satellite.angle_yaw)

            else:
                if (Satellite.vx - Moon.vx) > 0:
                    self.satellite.setH(Satellite.angle_yaw)
                else:
                    self.satellite.setH(180 + Satellite.angle_yaw)

            Moon.a = Physics.gravity(Moon.d, Earth)
            Moon.ax = (Moon.x / Moon.d) * Moon.a
            Moon.ay = (Moon.y / Moon.d) * Moon.a
            Moon.az = (Moon.z / Moon.d) * Moon.a

            Moon.vx -= Moon.ax * dt_simulation
            Moon.vy -= Moon.ay * dt_simulation
            Moon.vz -= Moon.az * dt_simulation
            Moon.v = np.sqrt(Moon.vx ** 2 + Moon.vy ** 2 + Moon.vz ** 2)

            Moon.x += Moon.vx * dt_simulation
            Moon.y += Moon.vy * dt_simulation
            Moon.z += Moon.vz * dt_simulation
            Moon.d = np.sqrt(Moon.x ** 2 + Moon.y ** 2 + Moon.z ** 2)

            Satellite.a = Physics.gravity(Satellite.d, Earth)
            Satellite.ax = (-Satellite.x / Satellite.d) * Satellite.a
            Satellite.ay = (-Satellite.y / Satellite.d) * Satellite.a
            Satellite.az = (-Satellite.z / Satellite.d) * Satellite.a

            Satellite.a = Physics.gravity(Moon.d_sat, Moon)
            Satellite.ax += (-Moon.d_x / Moon.d_sat) * Satellite.a
            Satellite.ay += (-Moon.d_y / Moon.d_sat) * Satellite.a
            Satellite.az += (-Moon.d_z / Moon.d_sat) * Satellite.a

            Satellite.vx += Satellite.ax * dt_simulation
            Satellite.vy += Satellite.ay * dt_simulation
            Satellite.vz += Satellite.az * dt_simulation
            Satellite.v = np.sqrt(Satellite.vx ** 2 + Satellite.vy ** 2 + Satellite.vz ** 2)

            Satellite.x += Satellite.vx * dt_simulation
            Satellite.y += Satellite.vy * dt_simulation
            Satellite.z += Satellite.vz * dt_simulation
            Satellite.d = np.sqrt(Satellite.x ** 2 + Satellite.y ** 2 + Satellite.z ** 2)

            Satellite.angle_earth = np.arctan(Satellite.y / Satellite.x)
            Satellite.angle_moon = np.arctan((Satellite.y - Moon.y) / (Satellite.x - Moon.x))

            Earth.h += (360 * dt_simulation) / (24 * 3600)

        return task.cont

    def update_light(self, task):

        fade_angle = np.pi / 6

        if Satellite.d < 4 * Earth.r:

            if Satellite.x <= 0:

                self.directionalLightSat.setColor((1.0, 1.0, 1.0, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif abs(Satellite.angle_earth) <= fade_angle:

                self.directionalLightSat.setColor((0, 0, 0, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif Satellite.angle_earth > fade_angle:

                intensity = (Satellite.angle_earth - fade_angle) / (2 * fade_angle)

                self.directionalLightSat.setColor((intensity, intensity, intensity, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif Satellite.angle_earth < - fade_angle:

                intensity = - (Satellite.angle_earth + fade_angle) / (2 * fade_angle)

                self.directionalLightSat.setColor((intensity, intensity, intensity, 1))
                self.satellite.setLight(self.directionalLightSatNP)

        elif Moon.d_sat < 4 * Moon.r:

            if (Satellite.x - Moon.x) <= 0:

                self.directionalLightSat.setColor((1.0, 1.0, 1.0, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif abs(Satellite.angle_moon) <= fade_angle:

                self.directionalLightSat.setColor((0, 0, 0, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif Satellite.angle_moon > fade_angle:

                intensity = (Satellite.angle_moon - fade_angle) / (2 * fade_angle)

                self.directionalLightSat.setColor((intensity, intensity, intensity, 1))
                self.satellite.setLight(self.directionalLightSatNP)

            elif Satellite.angle_moon < - fade_angle:

                intensity = - (Satellite.angle_moon + fade_angle) / (2 * fade_angle)

                self.directionalLightSat.setColor((intensity, intensity, intensity, 1))
                self.satellite.setLight(self.directionalLightSatNP)

        else:

            self.directionalLightSat.setColor((1.0, 1.0, 1.0, 1))
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
                                       + str(round(((Physics.time_simulation - Data.time[0]) / (Data.time[1] - Data.time[0])) * 100)))

                elif Triggers.transfer_2:

                    self.text4.setText("Trajectory information" + "\n" + "\n" + "Velocity  (m/s):  "
                                       + str(round(Satellite.v)) + "\n" + 'Distance to Earth  (km):  '
                                       + str(round((Satellite.d - Earth.r) / 10 ** 3)) + "\n"
                                       + 'Distance to Moon  (km):  ' + str(round((Moon.d_sat - Moon.r) / 10 ** 3))
                                       + "\n" + 'Transfer 2  (%):  '
                                       + str(round(((Physics.time_simulation - Data.time[1]) / (Data.time[2] - Data.time[1])) * 100)))

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

            if Triggers.phase_0:
                Triggers.phase_0 = False

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

                start_time_stringer = str(round((Trajectory.launch_1_time - Physics.time_simulation) / Trajectory.time_factor))

                time_stringer = start_time_stringer + ' seconds _'
                time_stringer_list = list(time_stringer)

                for i in range(len(time_stringer_list)):
                    text_list.append(time_stringer_list[i])

                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.phase_1 = False

            if Physics.time_simulation < (Trajectory.launch_1_time - (Trajectory.launch_1_time_sound_start * Trajectory.time_factor)):
                Triggers.sound_launch = True

            if Physics.time_simulation > (Trajectory.launch_1_time - (Trajectory.launch_1_time_sound_start * Trajectory.time_factor)) and Triggers.sound_launch:
                self.sound_launch_1.play()

                Triggers.sound_launch = False

            if Physics.time_simulation > (Trajectory.launch_1_time - (self.phase_1_total_text_time * Trajectory.time_factor)):

                if self.text_counter < len(self.phase_1_list):
                    text_list = self.phase_1_text[self.text_counter]
                    text_delay = self.phase_1_delay[self.text_counter]
                    text_time = self.phase_1_text_time[self.text_counter]

                    taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                          extraArgs=[text_list, self.phase_1_list, self.text_counter, text_time],
                                          appendTask=True)

                    self.text_counter += 1

            if Physics.time_simulation >= Trajectory.launch_1_time and Triggers.launch:
                self.update_particles('fire', True, (0, 0, -1.5), (0, 0, 90))

                Triggers.launch = False

                Triggers.orbit_earth = False
                Triggers.transfer_1 = True

            if Physics.time_simulation >= (Trajectory.launch_1_time + (Trajectory.launch_1_time_difference * Trajectory.time_factor)):
                self.update_particles('fire', False, (0, 0, 0), (0, 0, 0))
                self.update_phase_3(phase)

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

            elif all(self.phase_2_list) and not Triggers.decision:

                self.sound_background_1.play()

                self.update_phase_3(phase)

                self.text3.setText("Press 'y' to initialize the transfer skip or 'n' to accelerate the simulation")
                self.text3_NP.reparentTo(self.aspect2d)

                Triggers.decision = True

                self.text_counter = 1

                Triggers.phase_sub = True
                Triggers.task_1 = False

                return task.done

        if phase == 3:

            if Triggers.phase_3 and Triggers.time:

                text_list = list("Simulation speed up enabled _")
                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.phase_3 = False

            if Physics.time_simulation > Data.time[3] and Triggers.boost_1:
                Triggers.boost_1 = False

                text_list = list("First trajectory correction completed _")
                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

            if Physics.time_simulation > Data.time[4] and Triggers.boost_2:
                Triggers.boost_2 = False

                text_list = list("Second trajectory correction completed _")
                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

            if Physics.time_simulation > Physics.time_skip and Triggers.time:
                Trajectory.time_factor = 10

                Triggers.time = False

                text_list = list("Simulation speed up disabled, the module has now completed 98% of the first transfer _")
                text_time = self.phase_3_text_time[0]

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, self.phase_3_list, 0, text_time], appendTask=True)

            if Triggers.skip and Physics.time_simulation < Data.position_time[Data.count]:
                self.parentNodeCam.setHpr(-90, -30, -90)

                text_list = self.phase_3_text[0]
                text_time = self.phase_3_text_time[0]

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, self.phase_3_list, 0, text_time], appendTask=True)

                Triggers.skip = False

            if self.text_counter < len(self.phase_3_list) and Physics.time_simulation > Physics.time_skip and not Triggers.skip:

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

                return task.done

        if phase == 4:

            if Triggers.alignment:

                if not Triggers.reverse:

                    rel_angle = np.arctan((Moon.vy - Satellite.vy) / (Moon.vx - Satellite.vx)) * (180 / np.pi)
                    Trajectory.angle_to_turn = round(180 + rel_angle - Satellite.angle_yaw)

                    Triggers.reverse = True

                    # Turn left

                    self.update_particles('air', True, (0.57, 0.57, 0.2), (0, 0, -90))

                if Trajectory.turn_angle > (Trajectory.angle_to_turn / 2) and Triggers.flip:

                    # Turn right / stop turn

                    self.update_particles('air', True, (0.57, 0.57, -0.25), (0, 0, 90))

                    Triggers.flip = False

                if Trajectory.turn_angle == Trajectory.angle_to_turn:
                    Triggers.alignment = False
                    Triggers.alignment_auto = False

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

            Triggers.alignment_auto = False

            if Triggers.phase_5:

                text_list = list("Thruster re-armed, it will start in ")

                start_time_stringer = str(round((Trajectory.launch_2_time - Physics.time_simulation) / Trajectory.time_factor))

                time_stringer = start_time_stringer + ' seconds _'
                time_stringer_list = list(time_stringer)

                for i in range(len(time_stringer_list)):
                    text_list.append(time_stringer_list[i])

                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.phase_5 = False

            if Triggers.sound:

                # Time after first background song

                if Physics.time_simulation > (Physics.time_skip + (Trajectory.time_factor * (self.sound_background_1_length + 30))):

                    # Time before second launch song

                    if Physics.time_simulation < (Trajectory.launch_2_time - (Trajectory.time_factor * (Trajectory.launch_2_time_sound_start + self.sound_background_2_length + 30))):
                        self.sound_background_2.play()

                        Triggers.sound = False

            if Physics.time_simulation < (Trajectory.launch_2_time - (Trajectory.launch_2_time_sound_start * Trajectory.time_factor)):
                Triggers.sound_launch = True

            if Physics.time_simulation > (Trajectory.launch_2_time - (Trajectory.launch_2_time_sound_start * Trajectory.time_factor)) and Triggers.sound_launch:
                self.sound_launch_2.play()

                Triggers.sound_launch = False

            if Physics.time_simulation > (Trajectory.launch_2_time - (self.phase_5_total_text_time * Trajectory.time_factor)):

                if self.text_counter < len(self.phase_5_list):
                    text_list = self.phase_5_text[self.text_counter]
                    text_delay = self.phase_5_delay[self.text_counter]
                    text_time = self.phase_5_text_time[self.text_counter]

                    taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                          extraArgs=[text_list, self.phase_5_list, self.text_counter, text_time],
                                          appendTask=True)

                    self.text_counter += 1

            if Triggers.launch:
                if Physics.time_simulation > Trajectory.launch_2_time:
                    self.update_particles('fire', True, (0, 0, -1.5), (0, 0, 90))

                    Triggers.launch = False
                    Triggers.transfer_1 = False
                    Triggers.transfer_2 = True

            if Physics.time_simulation > (Trajectory.launch_2_time + (Trajectory.launch_2_time_difference * Trajectory.time_factor)):
                self.update_particles('fire', False, (0, 0, 0), (0, 0, 0))
                self.update_phase_3(phase)

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

                self.text3.setText("Press 'i' to initialize the speed up")
                self.text3_NP.reparentTo(self.aspect2d)

                self.text_counter = 0

                Triggers.phase_sub = True
                Triggers.task_1 = False

                return task.done

        if phase == 7:

            Triggers.time = True
            Trajectory.time_factor = 30

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

                start_time_stringer = str(round((Trajectory.launch_3_time - Physics.time_simulation) / Trajectory.time_factor))

                time_stringer = start_time_stringer + ' seconds _'
                time_stringer_list = list(time_stringer)

                for i in range(len(time_stringer_list)):
                    text_list.append(time_stringer_list[i])

                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.phase_8 = False

            if Physics.time_simulation > (Trajectory.launch_3_time - (10 * (Trajectory.launch_3_time_sound_start + 30))) and Triggers.time:
                Trajectory.time_factor = 10

                text_list = list("Simulation speed up disabled, the module has now completed 90% of the second transfer and is close to the final delta-V maneuver _")
                text_time = self.text_display_time + len(text_list) * self.symbol_speed

                Triggers.time = False

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

            if not Triggers.time:

                if Physics.time_simulation < (Trajectory.launch_3_time - (Trajectory.time_factor * Trajectory.launch_3_time_sound_start)):
                    Triggers.sound_launch = True

                if Physics.time_simulation > (Trajectory.launch_3_time - (Trajectory.time_factor * Trajectory.launch_3_time_sound_start)) and Triggers.sound_launch:
                    self.sound_launch_3.play()

                    Triggers.sound_launch = False

                if Physics.time_simulation > (Trajectory.launch_3_time - (Trajectory.time_factor * self.phase_8_total_text_time)):

                    if self.text_counter < len(self.phase_8_list):
                        text_list = self.phase_8_text[self.text_counter]
                        text_delay = self.phase_8_delay[self.text_counter]
                        text_time = self.phase_8_text_time[self.text_counter]

                        taskMgr.doMethodLater(text_delay, self.update_text, 'Phase text task',
                                              extraArgs=[text_list, self.phase_8_list, self.text_counter, text_time],
                                              appendTask=True)

                        self.text_counter += 1

                if Triggers.launch:
                    if Physics.time_simulation > Trajectory.launch_3_time:
                        self.update_particles('fire', True, (0, 0, -1.5), (0, 0, 90))

                        Triggers.launch = False
                        Triggers.transfer_2 = False
                        Triggers.orbit_moon = True

                if Physics.time_simulation >= (Trajectory.launch_3_time + (Trajectory.time_factor * Trajectory.launch_3_time_difference)):
                    self.update_particles('fire', False, (0, 0, 0), (0, 0, 0))
                    self.update_phase_3(phase)

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

            if Physics.time_simulation > (Trajectory.launch_3_time + (Trajectory.time_factor * (Trajectory.launch_3_time_difference + self.sound_background_3_length + 20))) and not Triggers.completed:
                text_list = list("Thank you for using the program, I hope you enjoyed it!  "
                                 "The simulation will stop automatically after two orbits and you can exit before at any time _")
                text_time = (2 * self.text_display_time) + len(text_list) * self.symbol_speed

                taskMgr.add(self.update_text, 'Phase text task',
                            extraArgs=[text_list, text_list, 0, text_time], appendTask=True)

                Triggers.completed = True

            if Physics.time_entry == (len(Data.position) - 1):

                self.text3.setText("SIMULATION COMPLETED \n press 'esc' to exit")
                self.text3_NP.reparentTo(self.aspect2d)

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
                self.PE_1_2.loadConfig('Configurations/Air.ptf')
                self.PE_2.loadConfig('Configurations/Air.ptf')
                self.PE_2_2.loadConfig('Configurations/Air.ptf')

                self.PE_1.setPos(pos)
                self.PE_1.setHpr(hpr)
                self.PE_1.setScale(0.1)

                self.PE_1_2.setPos(pos)
                self.PE_1_2.setHpr(hpr)
                self.PE_1_2.setScale(0.1)

                self.PE_2.setPos(pos)
                self.PE_2.setHpr(hpr)
                self.PE_2.setScale(0.1)

                self.PE_2_2.setPos(pos)
                self.PE_2_2.setHpr(hpr)
                self.PE_2_2.setScale(0.1)

                if self.PE_1.getZ() < 0.2:
                    self.PE_2.setZ(self.PE_1.getZ() + 0.5)
                else:
                    self.PE_2.setZ(self.PE_1.getZ() - 0.45)

                self.PE_2.setX(- self.PE_1.getX())
                self.PE_2.setR(self.PE_1.getR() - 180)

                self.PE_1_2.setY(- self.PE_1.getY())
                self.PE_2_2.setPos(self.PE_2.getX(), - self.PE_2.getY(), self.PE_2.getZ())
                self.PE_2_2.setR(self.PE_2.getR())

                self.PE_1.start(self.satellite)
                self.PE_1_2.start(self.satellite)
                self.PE_2.start(self.satellite)
                self.PE_2_2.start(self.satellite)

            else:
                self.PE_3.loadConfig('Configurations/Fire.ptf')

                self.PE_3.setPos(pos)
                self.PE_3.setHpr(hpr)
                self.PE_3.setScale(1)

                self.PE_3.start(self.satellite)

        else:
            self.PE_1.disable()
            self.PE_1_2.disable()
            self.PE_2.disable()
            self.PE_2_2.disable()
            self.PE_3.disable()

        return

    def update_warnings(self, task):

        phase = np.where(Triggers.phases)[0][0]

        if self.failure_trigger:
            self.text3.setText("MISSION FAILED \n press 'esc' to exit")
            self.text3.setTextColor(1, 0, 0, 1)
            self.text3_NP.reparentTo(self.aspect2d)

            self.sound_warning_major.stop()

            return task.done

        #if Triggers.phase_0 and Physics.time_simulation > 0.75 * Data.time[0]:
         #   print("\n Simulation ended due to user inactivity \n")
          #  sys.exit()

        if Triggers.phase_sub:

            if phase == 1:

                if Physics.time_simulation > (Data.time[0] - (Trajectory.time_factor * (2 * self.phase_1_total_text_time))):
                    self.failure_trigger = True

                if Physics.time_simulation > (Data.time[0] - (Trajectory.time_factor * ((2 * self.phase_1_total_text_time) + 12))) and self.major_trigger:

                    self.text3.setText("Warning: delta-V maneuver position near, arm the thruster now!")
                    self.text3.setTextColor(1, 0, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.stop()
                    self.sound_warning_major.play()

                    self.major_trigger = False

                elif Physics.time_simulation > (Data.time[0] - (Trajectory.time_factor * ((2 * self.phase_1_total_text_time) + 30))) and self.minor_trigger:

                    self.text3.setText("Warning: delta-V maneuver position approaching, please arm the thruster!")
                    self.text3.setTextColor(1, 0.65, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.play()

                    self.minor_trigger = False

            if phase == 3:

                if Physics.time_simulation > (Data.time[0] + (Trajectory.time_factor * ((2 * self.phase_2_total_text_time) + Trajectory.launch_1_time_difference + 60))):
                    self.failure_trigger = True

                if Physics.time_simulation > (Data.time[0] + (Trajectory.time_factor * ((2 * self.phase_2_total_text_time) + Trajectory.launch_1_time_difference + 48))) and self.major_trigger:

                    self.text3.setText("Warning: please select a simulation option now (y/n)!")
                    self.text3.setTextColor(1, 0, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.stop()
                    self.sound_warning_major.play()

                    self.major_trigger = False

                elif Physics.time_simulation > (Data.time[0] + (Trajectory.time_factor * ((2 * self.phase_2_total_text_time) + Trajectory.launch_1_time_difference + 30))) and self.minor_trigger:

                    self.text3.setText("Warning: please select a simulation option (y/n)!")
                    self.text3.setTextColor(1, 0.65, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.play()

                    self.minor_trigger = False

            if phase == 4:

                if Physics.time_simulation > (Physics.time_skip + (Trajectory.time_factor * ((2 * self.phase_3_total_text_time) + 60))):
                    self.failure_trigger = True

                if Physics.time_simulation > (Physics.time_skip + (Trajectory.time_factor * ((2 * self.phase_3_total_text_time) + 48))) and self.major_trigger:

                    self.text3.setText("Warning: please initiate alignment now!")
                    self.text3.setTextColor(1, 0, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.stop()
                    self.sound_warning_major.play()

                    self.major_trigger = False

                elif Physics.time_simulation > (Physics.time_skip + (Trajectory.time_factor * ((2 * self.phase_3_total_text_time) + 30))) and self.minor_trigger:

                    self.text3.setText("Warning: please initiate alignment!")
                    self.text3.setTextColor(1, 0.65, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.play()

                    self.minor_trigger = False

            if phase == 5:

                if Physics.time_simulation > (Data.time[1] - (Trajectory.time_factor * (2 * self.phase_5_total_text_time))):
                    self.failure_trigger = True

                if Physics.time_simulation > (Data.time[1] - (Trajectory.time_factor * ((2 * self.phase_5_total_text_time) + 12))) and self.major_trigger:

                    self.text3.setText("Warning: delta-V maneuver position near, arm the thruster now!")
                    self.text3.setTextColor(1, 0, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.stop()
                    self.sound_warning_major.play()

                    self.major_trigger = False

                elif Physics.time_simulation > (Data.time[1] - (Trajectory.time_factor * ((2 * self.phase_5_total_text_time) + 30))) and self.minor_trigger:

                    self.text3.setText("Warning: delta-V maneuver position approaching, please arm the thruster!")
                    self.text3.setTextColor(1, 0.65, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.play()

                    self.minor_trigger = False

            if phase == 7:

                if Physics.time_simulation > (Data.time[1] + (Trajectory.time_factor * ((2 * self.phase_6_total_text_time) + Trajectory.launch_1_time_difference + 60))):
                    self.failure_trigger = True

                if Physics.time_simulation > (Data.time[1] + (Trajectory.time_factor * ((2 * self.phase_6_total_text_time) + Trajectory.launch_1_time_difference + 48))) and self.major_trigger:

                    self.text3.setText("Warning: please initiate the speed up now!")
                    self.text3.setTextColor(1, 0, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.stop()
                    self.sound_warning_major.play()

                    self.major_trigger = False

                elif Physics.time_simulation > (Data.time[1] + (Trajectory.time_factor * ((2 * self.phase_6_total_text_time) + Trajectory.launch_1_time_difference + 30))) and self.minor_trigger:

                    self.text3.setText("Warning: please initiate the speed up!")
                    self.text3.setTextColor(1, 0.65, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.play()

                    self.minor_trigger = False

            if phase == 8:

                if Physics.time_simulation > (Data.time[1] + (10 * ((2 * (self.phase_6_total_text_time + self.phase_7_total_text_time)) + Trajectory.launch_1_time_difference + 270))):
                    self.failure_trigger = True

                if Physics.time_simulation > (Data.time[1] + (10 * ((2 * (self.phase_6_total_text_time + self.phase_7_total_text_time)) + Trajectory.launch_1_time_difference + 234))) and self.major_trigger:

                    self.text3.setText("Warning: delta-V maneuver position near, arm the thruster now!")
                    self.text3.setTextColor(1, 0, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.stop()
                    self.sound_warning_major.play()

                    self.major_trigger = False

                elif Physics.time_simulation > (Data.time[1] + (10 * ((2 * (self.phase_6_total_text_time + self.phase_7_total_text_time)) + Trajectory.launch_1_time_difference + 180))) and self.minor_trigger:

                    self.text3.setText("Warning: delta-V maneuver position approaching, please arm the thruster!")
                    self.text3.setTextColor(1, 0.65, 0, 1)
                    self.text3_NP.reparentTo(self.aspect2d)

                    self.sound_warning_minor.play()

                    self.minor_trigger = False

        else:
            self.text3.setTextColor(1, 1, 1, 1)

            self.sound_warning_minor.stop()
            self.sound_warning_major.stop()

        return task.cont

    def update_decision(self, decision):

        if Triggers.decision:

            if decision == 'y':
                Physics.time_simulation = Physics.time_skip

                Triggers.skip = True
                Triggers.boost_1 = False
                Triggers.boost_2 = False

            else:
                Trajectory.time_factor = 300

                Triggers.time = True

            self.update_phase_1()

            Triggers.decision = False

        return

    def update_self(self):

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

        self.satellite = loader.loadModel("Models/Satellite.gltf")
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
        self.directionalLightScene.setColor((1.0, 1.0, 1.0, 1))
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

        self.accept("m", self.update_self)

        self.accept('y', lambda: self.update_decision('y'))
        self.accept('n', lambda: self.update_decision('n'))

        # Particles

        self.enableParticles()

        self.PE_1 = ParticleEffect()
        self.PE_1_2 = ParticleEffect()
        self.PE_2 = ParticleEffect()
        self.PE_2_2 = ParticleEffect()
        self.PE_3 = ParticleEffect()

        self.PE_1.setLight(self.ambientLightParticlesNP)
        self.PE_1_2.setLight(self.ambientLightParticlesNP)
        self.PE_2.setLight(self.ambientLightParticlesNP)
        self.PE_2_2.setLight(self.ambientLightParticlesNP)
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
                             list("The journey towards the Moon will take roughly 4 days in real life _"),
                             list("Fortunately you have two choices to drastically reduce the simulation time _"),
                             list(
                                 "You can skip the major part of the first transfer, bringing the module close to the second transfer around the Moon _"),
                             list(
                                 "In this case both corrective burns will be completed and all that remains is the attitude change before the second transfer _"),
                             list(
                                 "Or you can speed up the simulation, allowing you to travel 30 times faster than you are now _"),
                             list(
                                 "It will then take roughly 20 minutes to complete the first transfer and you get to enjoy the view _")]

        self.phase_2_list = np.zeros(len(self.phase_2_text), dtype=bool)
        self.phase_2_delay = np.zeros(len(self.phase_2_text))
        self.phase_2_text_time = np.zeros(len(self.phase_2_text))
        self.phase_2_text_time[0] = self.text_display_time + len(self.phase_2_text[0]) * self.symbol_speed

        for i in range(len(self.phase_2_list) - 1):
            self.phase_2_text_time[i + 1] = self.text_display_time + len(self.phase_2_text[i + 1]) * self.symbol_speed
            self.phase_2_delay[i + 1] = self.phase_2_delay[i] + self.phase_2_text_time[i]

        self.phase_2_total_text_time = sum(self.phase_2_text_time)

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

        self.phase_3_total_text_time = sum(self.phase_3_text_time)

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

        self.phase_4_total_text_time = sum(self.phase_4_text_time)

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
                             list("The second transfer takes about 20 minutes in this simulation _"),
                             list("It transfers the module from its current height to the final orbit of 1000 km _"),
                             list("Again, the simulation can be sped up to 3 times the current speed, reducing the total time to a mere 6 minutes _")]

        self.phase_6_list = np.zeros(len(self.phase_6_text), dtype=bool)
        self.phase_6_delay = np.zeros(len(self.phase_6_text))
        self.phase_6_text_time = np.zeros(len(self.phase_6_text))
        self.phase_6_text_time[0] = self.text_display_time + len(self.phase_6_text[0]) * self.symbol_speed

        for i in range(len(self.phase_6_list) - 1):
            self.phase_6_text_time[i + 1] = self.text_display_time + len(self.phase_6_text[i + 1]) * self.symbol_speed
            self.phase_6_delay[i + 1] = self.phase_6_delay[i] + self.phase_6_text_time[i]

        self.phase_6_total_text_time = sum(self.phase_6_text_time)

        # Phase 7

        self.phase_7_text = [list("Simulation speed up enabled _"),
                             list("The final delta-V maneuver is about 5 minutes away at this simulation rate and it is required that you arm "
                                  "the module's thruster one last time _")]

        self.phase_7_list = np.zeros(len(self.phase_7_text), dtype=bool)
        self.phase_7_delay = np.zeros(len(self.phase_7_text))
        self.phase_7_text_time = np.zeros(len(self.phase_7_text))
        self.phase_7_text_time[0] = self.text_display_time + len(self.phase_7_text[0]) * self.symbol_speed

        for i in range(len(self.phase_7_list) - 1):
            self.phase_7_text_time[i + 1] = self.text_display_time + len(self.phase_7_text[i + 1]) * self.symbol_speed
            self.phase_7_delay[i + 1] = self.phase_7_delay[i] + self.phase_7_text_time[i]

        self.phase_7_total_text_time = sum(self.phase_7_text_time)

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