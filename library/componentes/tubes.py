from graphics.create_plots import PlotManager
from library.materials import Fluid
import numpy as np


class TubeBase(Fluid):

    def __repr__(self):
        return str(dict(
            diameter = self.diameter,
            length = self.length,
        ))

class Tube(TubeBase):

    def __init__(self, diameter, length):
        super().__init__()
        self.diameter = diameter
        self.length = length

    @property
    def R(self):
        return (8 * self.ethaD * self.length) / (np.pi * (self.diameter / 2)**4) # Schlauchwiderstand.

    @property
    def reynolds(self):
        # TODO: mit von Fluid verbinden
        ''' Estimate Reynolds-Number as first guess '''
        # Rohrparameter
        A = np.pi * (self.diameter / 2) ** 2

        # Pumpenauslegung und Druckdifferenz
        delta_p = 50 * 1e3  # Pa
        # SToffwerte @ 20°C
        etha_w = 1002.0 * 1e-6  # kg m^-1 s^-1
        nu_w = 1.004 * 1e-6  # m^2 s^-1
        rho_w = 998.21  # kg/m^-3
        # Hagen-Poiseuille-Law:
        dV_dt = (np.pi * ((self.diameter / 2) ** 4) * delta_p) / (8 * etha_w * self.lenght)

        # Mittlere Geschwindigkeit:
        v_m = dV_dt / A

        # Reynolds-Formula:
        reynolds_number = (v_m * self.diameter) / nu_w

        # Calculate Pipe Friction Parameter lambda:
        lambda_pipe = 64 / reynolds_number

        ''' Get Resistance Support Values for Pipe Elbows '''  # from table
        # Correspondence data of Reynolds number and res. zeta values (for 90° and R/D=4)
        rey_zeta_elbow_data = [[500, 1.6], [550, 1.5], [600, 1.4], [700, 1.2], [800, 1.2], [1000, 0.9],
                               [2000, 0.575]]
        return reynolds_number


class PlotTubes(PlotManager):

    def __init__(self):
        super().__init__()
        self.length = np.linspace(10e-3, 1000e-3, 100)
        self.diameter = np.linspace(10e-3, 100e-3, 100)

    def plot(self):
        self.plot_resistance()
        self.plot_reynolds()

    def plot_resistance(self):
        tube_resistance = []
        for i, lenght in enumerate(self.length):
            tube_resistance.append([Tube(diameter, lenght).R for diameter in self.diameter])
        tube_resistance = np.array(tube_resistance)

        self.plot_colormesh(
            tube_resistance,
            xy=(self.length, self.diameter),
            title='Resistance',
            xlabel='Lenght [m]',
            ylabel='Diameter [m]',
            filename='tube_resistance'
        )

    def plot_reynolds(self):
        tube_reynolds = []
        for i, lenght in enumerate(self.length):
            tube_reynolds.append([Tube(diameter, lenght).reynolds for diameter in self.diameter])
        tube_resistance = np.array(tube_reynolds)

        self.plot_colormesh(
            tube_resistance,
            xy=(self.length, self.diameter),
            title='Reynolds number',
            xlabel='Lenght [m]',
            ylabel='Diameter [m]',
            filename='reynolds_number'
        )

if __name__ == '__main__':
    

    # plot = PlotTubes()
    # plot.plot()


    print(Tube(diameter=1e-3, lenght=1e-3).R)

