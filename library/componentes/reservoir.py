from library.materials import Fluid
from graphics.create_plots import PlotManager
import matplotlib.pyplot as plt
import numpy as np

class ReservoirBase(Fluid):

    p_amb = None
    z_level = None
    diameter = None
    direction = None

    def __repr__(self):
        return str(dict(
            p_amb=self.p_amb,
            z_level=self.z_level,
            diameter=self.diameter,
            direction =self.direction,
        ))

class Reservoir(ReservoirBase):

    def __init__(self, p_amb, z_level, diameter, direction):
        super().__init__()
        self.p_amb = p_amb
        self.z_level = z_level
        self.diameter = diameter
        self.direction = direction
        self.p_last = self.cal_pasc(self.z_level) + self.p_amb

    def p_res(self, z):
        self.p_last = getattr(self, self.direction)(z)
        return self.p_last

    def rear(self, z):
        p_last = self.cal_pasc(self.z_level+z)
        return p_last

    def front(self, z):
        z=0 # keine Füllstandsänderung am vorderen Reservoir
        p_last = self.cal_pasc(self.z_level+z)
        return p_last

    def cal_pasc(self, z):
        ''' Pascal´sches Gesetz '''
        g = 9.81 # [m/s²]
        pres = Fluid.rho*g*(z) + self.p_amb
        return pres

    def area(self):
        resarea = np.pi*(self.diameter**2)/4
        return resarea


class PlotReservoir(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):
        contanier = dict()
        configuration = 'rear'
        levels = np.linspace(0, 3, 251)

        reservoir_rear = Reservoir(p_amb=1e5, z_level=0, diameter=0.05, direction=configuration)
        for pi in np.linspace(0.5, 10, 20):
            reservoir_rear.p_amb = pi
            contanier[f'{pi :.2f} p_amb'] = [reservoir_rear.p_res(zi) for zi in levels]

        self.plot_dict(levels, contanier,
                       title=f'Reservoir - {configuration}',
                       xlabel='Level [m]',
                       ylabel='Pressure [Pa]')

if __name__ == '__main__':

    plot = PlotReservoir()
    plot.plot()