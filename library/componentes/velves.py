from graphics.create_plots import PlotManager
from library.materials import Fluid
import numpy as np


class VelveBase(Fluid):

    R_open = None
    R_close = None
    direction = None
    R_last = None

    def __repr__(self):
        return str(dict(
            R_open=self.R_open,
            R_close=self.R_close,
            direction =self.direction,
        ))

class Velve(VelveBase):

    def __init__(self, R_open, R_close, direction):
        super().__init__()
        self.R_open = R_open
        self.R_close = R_close
        self.direction = direction
        self.R_last = R_open

    def R(self, u):
        self.R_last = getattr(self, self.direction)(u)
        return self.R_last

    def constant(self, u):
        return self.R_open #  * u

    def backward(self, u):
        if u > 0: # druckhub
            return self.R_close
        else: # saughub
            return self.R_open

    def forward(self, u):
        if u > 0: # druckhub
            return self.R_open
        else: # saughub
            return self.R_close


class Velve_fermi(VelveBase):

    def __init__(self, R_open, R_close, direction, nu=0.05, v_switch=0):
        super().__init__()
        self.R_open = R_open
        self.R_close = R_close
        self.R_last = R_open
        self.direction = direction
        self.nu = nu  # mass for the slope
        self.v_switch = v_switch  # voltage to open
        self.all_R = list()

    def R(self, u):
        self.R_last = getattr(self, self.direction)(u)
        self.all_R.append(self.R_last)
        return self.R_last

    def constant(self, u):
        return self.R_open

    def backward(self, u):
        return (self.R_open - self.R_close) / (np.exp((u - self.v_switch) / self.nu) + 1) + self.R_close

    def forward(self, u):
        return (self.R_close - self.R_open) / (np.exp((u - self.v_switch) / self.nu) + 1) + self.R_open


class PlotVelve(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):
        contanier = dict()
        configuration = 'backward'
        voltage = np.linspace(-3, 3, 251)

        velve_const = Velve(R_open=100, R_close=1e3, direction=configuration)
        contanier[f'constant'] = [velve_const.R(ui) for ui in voltage]

        for nui in np.linspace(0.05, 0.5, 10):
            velve = Velve_fermi(R_open=100, R_close=1e3, direction=configuration, nu=nui)
            contanier[f'{nui :.2f} nu'] = [velve.R(ui) for ui in voltage]

        self.plot_dict(voltage, contanier,
                       title=f'Fermi velve - {configuration}',
                       xlabel='Voltage [V]',
                       ylabel='Resistance []')

if __name__ == '__main__':

    plot = PlotVelve()
    plot.plot()