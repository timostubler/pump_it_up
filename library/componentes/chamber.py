from library.materials import Fluid
from graphics.create_plots import PlotManager
import matplotlib.pyplot as plt
import numpy as np
from library.signals import Sinus, Rectangle

class PumpBase(Fluid):

    def __repr__(self):
        return str(dict(
        ))

class Pump_fermi(Fluid):
    '''
    Auslenkung realer Piezoaktor z.B.: 2um
    (https://www.physikinstrumente.de/de/produkte/piezoelektrische-wandler-transducer-piezoaktoren/pd0xx-runde-picma-chip-aktoren-100850/#specification)
    '''

    def __init__(self, nu):
        super().__init__()

        self.nu = nu  # mass for the slope

        self.diameter = 5.7 * 10 ** -3  # m
        self.A = np.pi * self.diameter / 4

        self.z_0 = 1 * 10 ** -3  # m
        self.z_max = 35 * 10 ** -6  # m ANNAHME
        self.z_min = -15 * 10 ** -6  # m ANNAHME

        self.C_min = 0.5e-17
        self.C_max = 1.5e-17

        self.p_max = 50 * 10 ** 3  # Pa back pressure air
        self.p_min = -38 * 10 ** 3  # Pa suction pressure air

    def stroke(self, voltage):
        return (self.zmin - self.zmax) / (np.exp((voltage) / self.nu) + 1) + self.zmax

    def C(self, voltage):
        return (self.C_max - self.C_min) / (np.exp((voltage) / self.nu) + 1) + self.C_min

    def p(self, voltage):
        return (self.p_min - self.p_max) / (np.exp((voltage) / self.nu) + 1) + self.p_max

    def __repr__(self):
        return " TUDOS "

class PlotPump(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):
        # self.plot_pump(Pump(), name='pump')
        self.plot_pump(Pump_fermi(nu=5e3), name='pump_fermi')

    def plot_pump(self, pump, name):
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
        ax3 = ax1.twinx()
        ax4 = ax2.twinx()
        colors = self.get_cmap(3)

        ax1.set_xlabel('Time [s]')
        ax3.set_xlabel('Voltage [V]')
        ax4.set_xlabel('Voltage [V]')
        ax1.set_ylabel('Pressure [Pa]')
        ax2.set_ylabel('Capacity [F]')

        time = np.linspace(0, 1, 100)
        signal = Rectangle(amplitude=5, frequency=4, offset=0)
        voltage = [signal(t) for t in time]
        # stroke = [pump.stroke(ui) for ui in u]
        capacity = [pump.C(signal(t)) for t in time]
        pressure = [pump.p(signal(t)) for t in time]

        # ax1.plot(u, stroke, color=colors[0])
        ax1.plot(time, pressure, color=colors[0])
        ax3.plot(time, voltage, color=colors[1], marker='.')
        ax2.plot(time, capacity, color=colors[0])
        ax4.plot(time, voltage, color=colors[1], marker='.')

        self._dump(fig, name)


if __name__ == '__main__':

    plot = PlotPump()
    plot.plot()