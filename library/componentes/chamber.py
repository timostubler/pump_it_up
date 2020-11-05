from library.materials import Fluid
from graphics.create_plots import PlotManager
import matplotlib.pyplot as plt
import numpy as np

class PumpBase(Fluid):

    Pmin=None
    Pmax=None
    Vmin=None
    Vmax=None

    zmax = None
    zmin = None

    def __repr__(self):
        return str(dict(
        ))

class Pump(PumpBase):
    """ TUDOS pump from FH slides """

    Pmin = -38  # kPa suction pressure air
    Pmax = 50  # kPa back pressure air
    Vmin = -76  # V operation voltage
    Vmax = 240  # V operation voltage

    zmax = 35 * 10 ** -6  # m ANNAHME
    zmin = -15 * 10 ** -6  # m ANNAHME
    diameter = 5.7 * 10 ** -3  # m

    def __init__(self):
        super().__init__()
        # self.diameter = 5.7 * 10 ** -3  # m
        # self.A = np.pi * ((self.diameter) ** 2) / 4
        #
        # # self.Vmax = 240  # V operation voltage
        # # self.Vmin = -76  # V operation voltage
        # self.VAmp = (abs(self.Vmax) + abs(self.Vmin)) / 2
        # self.VOff = self.Vmax - self.VAmp
        #
        # # self.zmax = 35 * 10 ** -6  # m ANNAHME
        # # self.zmin = -15 * 10 ** -6  # m ANNAHME
        # self.zAmp = (abs(self.zmax) + abs(self.zmin)) / 2  # Amplituden-Berechnung
        # self.zOff = self.zmax - self.zAmp  # Offset-Berechnung
        #
        # self.Pmax = 50  # kPa back pressure air
        # self.Pmin = -38  # kPa suction pressure air
        # self.PAmp = (abs(self.Pmax) + abs(self.Pmin)) / 2
        # self.POff = self.Pmax - self.PAmp

    def stroke(self, voltage):  # Hub
        if voltage > 0:
            if voltage > self.Vmax:
                return self.zmax
            else:
                return self.zmax * voltage / self.Vmax
        else:
            if voltage < self.Vmin:
                return self.zmin
            else:
                return self.zmin * voltage / self.Vmin

    def C(self, voltage):
        # C = A*z/(Rgs*T)
        A = np.pi * ((self.diameter) ** 2) / 4
        return A * self.stroke(voltage) / (self.Rgs * self.T)

    def p(self, voltage):
        if voltage > 0:
            if voltage > self.Vmax:
                return self.Pmax
            else:
                return self.Pmax * voltage / self.Vmax
        else:
            if voltage < self.Vmin:
                return self.Pmin
            else:
                return self.Pmin * voltage / self.Vmin


class Pump_fermi(Fluid):

    def __repr__(self):
        return " TUDOS "

    def __init__(self, nu=0.0001):
        super().__init__()

        self.nu = nu  # mass for the slope
        self.diameter = 5.7 * 10 ** -3  # m
        self.A = np.pi * self.diameter / 4
        self.z0 = 1 * 10 ** -3  # m
        self.V0 = self.A * self.z0
        ''' 
        Auslenkung realer Piezoaktor z.B.: 2um
        (https://www.physikinstrumente.de/de/produkte/piezoelektrische-wandler-transducer-piezoaktoren/pd0xx-runde-picma-chip-aktoren-100850/#specification) 
        '''

        self.zmax = 35 * 10 ** -6  # m ANNAHME
        self.zmin = -15 * 10 ** -6  # m ANNAHME
        self.zAmp = (self.zmax + abs(self.zmin)) / 2
        self.zOff = self.zmax - (self.zmax + abs(self.zmin)) / 2

        self.Vmax = 240  # V operation voltage
        self.Vmin = -76  # V operation voltage
        self.VAmp = (self.Vmax + abs(self.Vmin)) / 2
        self.VOff = self.Vmax - (self.Vmax + abs(self.Vmin)) / 2

        self.Pmax = 50 * 10 ** 3  # Pa back pressure air
        self.Pmin = -38 * 10 ** 3  # Pa suction pressure air
        self.PAmp = (self.Pmax + abs(self.Pmin)) / 2
        self.POff = self.Pmax - (self.Pmax + abs(self.Pmin)) / 2

    def stroke(self, voltage):
        return (self.zmin - self.zmax) / (np.exp((voltage) / self.nu) + 1) + self.zmax

    def C(self, voltage):
        # return 9.26 * 10 ** -9
        Cmin, Cmax = 0.5e-17, 1.5e-17
        return (Cmax - Cmin) / (np.exp((voltage) / self.nu) + 1) + Cmin

    def p(self, voltage):
        return (self.Pmin - self.Pmax) / (np.exp((voltage) / self.nu) + 1) + self.Pmax


class PlotPump(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):
        self.plot_pump(Pump(), name='pump')
        self.plot_pump(Pump_fermi(), name='pump_fermi')

    def plot_pump(self, pump, name):
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True)
        colors = self.get_cmap(3)

        ax3.set_xlabel('Voltage [V]')
        ax1.set_ylabel('Pressure [Pa]')
        ax2.set_ylabel('Stroke [m]')
        ax3.set_ylabel('Capacity [F]')

        u = np.linspace(-1, 1, 251)
        stroke = [pump.stroke(ui) for ui in u]
        capacity = [pump.C(ui) for ui in u]
        pressure = [pump.p(ui) for ui in u]

        ax1.plot(u, stroke, color=colors[0])
        ax2.plot(u, pressure, color=colors[0])
        ax3.plot(u, capacity, color=colors[0])

        self._dump(fig, name)


if __name__ == '__main__':

    plot = PlotPump()
    plot.plot()