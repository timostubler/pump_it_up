from library.materials import Fluid
from graphics.create_plots import PlotManager
import matplotlib.pyplot as plt
import numpy as np


class Velve:

    def __init__(self, R_open, R_close, direction):
        self.R_open = R_open
        self.R_close = R_close
        self.direction = direction

    def R(self, u):
        return getattr(self, self.direction)(u)

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


class Velve_fermi:

    def __init__(self, R_open, R_close, direction, nu=0.1, v_switch=0):
        self.R_open = R_open
        self.R_close = R_close
        self.R_actual = R_open
        self.direction = direction
        self.nu = nu  # mass for the slope
        self.v_switch = v_switch  # voltage to open

    def R(self, u):
        return getattr(self, self.direction)(u)

    def constant(self, u):
        self.R_actual = self.R_actual
        return self.R_actual

    def backward(self, u):
        self.R_actual = (self.R_open - self.R_close) / (np.exp((u - self.v_switch) / self.nu) + 1) + self.R_close
        return self.R_actual

    def forward(self, u):
        self.R_actual = (self.R_close - self.R_open) / (np.exp((u - self.v_switch) / self.nu) + 1) + self.R_open
        return self.R_actual


class PlotVelve(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):
        self.plot_fermi()
        self.plot_rectangle()

    def plot_fermi(self):
        fig, ax1 = plt.subplots(nrows=1, ncols=1)
        #ax1.set_yscale('log')
        ax1.set_xlabel('Voltage [V]')
        ax1.set_ylabel('Resistance [Ohm]')
        colors = self.get_cmap(3)

        velve_const = Velve_fermi(R_open=0.5e3, R_close=1e3, direction='constant')
        velve_forward = Velve_fermi(R_open=1, R_close=1e3, direction='forward')
        velve_backward = Velve_fermi(R_open=1, R_close=1e3, direction='backward')

        u = np.linspace(-1, 1, 251)
        v_const = [velve_const.R(ui) for ui in u]
        v_fw = [velve_forward.R(ui) for ui in u]
        v_bw = [velve_backward.R(ui) for ui in u]

        ax1.plot(u, v_const, label='constant', color=colors[0])
        ax1.plot(u, v_fw, label='forward', color=colors[1])
        ax1.plot(u, v_bw, label='backward', color=colors[2])

        plt.legend()

        self._dump(fig, 'velve_fermi')

    def plot_rectangle(self):

        fig, ax1 = plt.subplots(nrows=1, ncols=1)
        # ax1.set_yscale('log')
        ax1.set_xlabel('Voltage [V]')
        ax1.set_ylabel('Resistance [Ohm]')
        colors = self.get_cmap(3)

        velve_const = Velve(R_open=0.5e3, R_close=1e3, direction='constant')
        velve_forward = Velve(R_open=1, R_close=1e3, direction='forward')
        velve_backward = Velve(R_open=1, R_close=1e3, direction='backward')

        u = np.linspace(-1, 1, 251)
        v_const = [velve_const.R(ui) for ui in u]
        v_fw = [velve_forward.R(ui) for ui in u]
        v_bw = [velve_backward.R(ui) for ui in u]

        ax1.plot(u, v_const, label='constant', color=colors[0])
        ax1.plot(u, v_fw, label='forward', color=colors[1])
        ax1.plot(u, v_bw, label='backward', color=colors[2])

        plt.legend()

        self._dump(fig, 'velve_rectangle')

if __name__ == '__main__':

    plot = PlotVelve()
    plot.plot()