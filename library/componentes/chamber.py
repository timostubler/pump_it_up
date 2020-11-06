from library.materials import Fluid
from graphics.create_plots import PlotManager
import matplotlib.pyplot as plt
import numpy as np
from library.signals import Sinus, Rectangle
from scipy.integrate import odeint

class PumpBase(Fluid):

    def __repr__(self):
        return str(dict(
        ))





class Pump_fermi(Fluid):
    '''
    Auslenkung realer Piezoaktor z.B.: 2um
    (https://www.physikinstrumente.de/de/produkte/piezoelektrische-wandler-transducer-piezoaktoren/pd0xx-runde-picma-chip-aktoren-100850/#specification)
    '''

    RC = None  # trägheit
    K = None  # s / V

    def __init__(self, K, RC, time, signal):
        super().__init__()
        # self.nu = nu  # mass for the slope

        self.diameter = 5.7 * 10 ** -3  # m
        self.A = np.pi * self.diameter / 4

        self.z_0 = 5 * 10 ** -6 # ruhelage
        self.z_max = 35 * 10 ** -6  # m ANNAHME
        self.z_min = -15 * 10 ** -6  # m ANNAHME

        self.C_min = 0.5e-17
        self.C_max = 1.5e-17

        self.p_max = 50*1e3 # Pa
        self.p_min = -38*1e3 # Pa

        self.p_scale = 5e10 # Pa scale

        self.RC = RC # trägheit
        self.s0 = 0
        self.K = K # s / V

        self.stroke = self.get_stroke(time, signal)
        self.scale = self.stroke

        self.stroke = self.stroke * 2e-6 + self.z_0
        # self.stroke_min = min(self.stroke)
        # self.stroke_max = max(self.stroke)

        self.stroke_reference = dict(zip(time, self.stroke))
        self.scale_reference = dict(zip(time, self.scale))

    def get_stroke(self, time, signal):
        def ds_dt(s, t):
            return (self.K * signal(t) - s) / self.RC
        stroke = -1 * odeint(ds_dt, self.s0, time)
        return stroke

    def C(self, time):
        return (((self.scale_reference[time] + 1)/2 * (abs(self.C_max) + abs(self.C_min))) + self.C_min)

    def p(self, time):
        return -1 * (((+1*self.scale_reference[time] + 1)/2 * (abs(self.p_max) + abs(self.p_min))) + self.p_min)

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

        time = np.linspace(-1, 1, 1000)
        signal = Rectangle(amplitude=1, frequency=4, offset=0)
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

    signal = Rectangle(amplitude=1, frequency=2, offset=0)
    time = np.linspace(0, 1, 1000)
    voltage = [signal(t) for t in time]

    pump = Pump_fermi(K=1e-6, RC=0.1, time=time, signal=signal)
    pressure = [pump.p(t) for t in time]
    capacity = [pump.C(t) for t in time]

    fig, (ax1, ax3, ax5) = plt.subplots(3, 1)

    ax2 = ax1.twinx()
    ax4 = ax3.twinx()
    ax6 = ax5.twinx()

    ax1.plot(time, voltage, color='black')
    ax2.plot(time, pump.stroke, color='green', label='stroke')

    ax3.plot(time, voltage, color='black')
    ax4.plot(time, capacity, color='blue', label='capacity')

    ax5.plot(time, voltage, color='black')
    ax6.plot(time, pressure, color='red', label='pressure')

    plt.legend()
    plt.show()

