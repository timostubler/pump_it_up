from graphics.create_plots import PlotManager
from library.materials import Fluid
from library.physical_constants import ConstantsDict
import numpy as np

class ReservoirBase(Fluid):

    d = None # m diameter
    h = None # m height
    h_act = None # Füllstand

    def __repr__(self):
        return str(dict(
            d=self.d,
            h=self.h,
            h_act=self.h_act
        ))

class Reservoir(ReservoirBase):
    # TODO: Link ambient pressure to some imaginary case (e.g. reactor with chemical reaction @ specific pressure)
    # TODO: Link self.h_act with incoming or outgoing dV_dt
    def __init__(self, d, h, h_act):
        super().__init__()
        self.d = d
        self.h = h
        self.h_act = h_act
        self.A = np.pi * (self.d / 2) ** 2
        self.g = ConstantsDict.g

        self.p_amb = 1e5 # [Pa]

    @property
    def P(self):
        ''' Actual pressure of the reservoir calculated by Pascals Law'''
        return (Fluid.rho*self.h_act*self.g + self.p_amb)


class PlotReservoir(PlotManager):

    def __init__(self):
        super().__init__()
        self.height_act = np.linspace(1e-3, 1000e-3, 1000)
        self.p_amb = np.linspace(1e5, 10*1e5, 100)
        self.h = 10000
        self.d = 100e-3

    def plot(self):
        self.plot_pressure()

    def plot_pressure(self):
        reservoir_p = []
        for i, h_act in enumerate(self.height_act):
            reservoir_p.append([Reservoir(self.d, self.h, h_act).P for p in self.p_amb])
        reservoir_p = np.array(reservoir_p)

        self.plot_colormesh(
            reservoir_p,
            xy=(self.height_act, self.p_amb),
            title='Pressure at Reservoir Ground',
            xlabel='Height [m]',
            ylabel='Ambient Pressure [Pa]',
            filename='reservoir_ground_pressure'
        )


if __name__ == '__main__':
    plot = PlotReservoir()
    plot.plot()