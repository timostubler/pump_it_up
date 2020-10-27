from graphics.create_plots import PlotManager
from library.materials import Fluid
import numpy as np

class TubeBase(Fluid):

    d = None # m diameter
    l = None # m length
    a = None # deg angle

    def __repr__(self):
        return str(dict(
            d=self.d,
            l=self.l,
            a =self.a,
        ))

class Tube(TubeBase):

    def __init__(self, d, l):
        super().__init__()
        self.d = d
        self.l = l
        self.A = np.pi * (self.d / 2) ** 2

    @property
    def R(self):
        ''' Calculate inherent Tube Resistance based on the friction number lambda and geometric parameters'''
        return (self.lambda_friction) * (self.l/self.d) * (Fluid.rho/(2*self.A**2))
        # return (8 * self.ethaD * self.l) / (np.pi * (self.d / 2)**4) # Schlauchwiderstand.

    @property
    def lambda_friction(self):
        ''' Friction Number for laminar flows and small reynold values '''
        return (64/self.reynolds)

    @property
    def reynolds(self):
        ''' Estimate Reynolds-Number as first guess without any tube resistance considerations, since i.e. then the flow velocity would be highest, Re should be smaller then Re_krit for laminar flow'''

        # Druckdifferenz zwischen Pumpkammer- und jeweiligen Reservoir Values
        delta_p = 50 * 1e3  # Pa #TODO: connect with Pmax/Pmin and reservoir pressure values for forwards/backward direction differentiation

        # Stoffwerte Wasser @ 20°C from Fluid Class:
        etha_w = Fluid.etha
        nu_w = Fluid.nu

        # Hagen-Poiseuille-Law:
        dV_dt = (np.pi * ((self.d / 2) ** 4) * delta_p) / (8 * etha_w * self.l) # [m^3 s^-1]

        # Mittlere Geschwindigkeit:
        v_m = dV_dt / self.A # [m s^-1]

        # Reynolds-Formula:
        reynolds_number = (v_m * self.d) / nu_w

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
        for i, l in enumerate(self.length):
            tube_resistance.append([Tube(d, l).R for d in self.diameter])
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
        for i, l in enumerate(self.length):
            tube_reynolds.append([Tube(d, l).reynolds for d in self.diameter])
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
    

    plot = PlotTubes()
    plot.plot()
