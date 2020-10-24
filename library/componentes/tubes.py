from graphics.create_plots import PlotManager
from library.materials import Fluid
import numpy as np
import matplotlib.pyplot as plt


class Tube(Fluid): # Klasse Rohr

    def __init__(self, d, l):
        super().__init__()
        self.D = d # m Diameter
        self.L = l # m Length

    def R(self):
        return (8 * self.ethaD * self.L) / (np.pi * (self.D / 2)**4) # Schlauchwiderstand.

class PlotTubes(PlotManager):

    def __init__(self):
        pass

    def plot(self):
        self.plot_diameter()
        self.plot_length()

    def plot_length(self):

        fig, ax1 = plt.subplots(nrows=1, ncols=1)
        ax1.set_xlabel('Length [m]')
        ax1.set_ylabel('Resistance [Ohm]')

        length = np.linspace(1e-3, 100e-3, 100)
        diameter = np.linspace(1e-3, 10e-3, 10)

        colors = self.get_cmap(len(diameter))

        for i, d in enumerate(diameter):

            tube_resistance = [Tube(d, l).R() for l in length]

            ax1.plot(length, tube_resistance, color=colors[i], label=f'{d :.4f} m')

        plt.legend(title='Diameter')
        self._dump(fig, 'tube_length')


    def plot_diameter(self):

        fig, ax1 = plt.subplots(nrows=1, ncols=1)
        ax1.set_xlabel('Diameter [m]')
        ax1.set_ylabel('Resistance [Ohm]')

        length = np.linspace(1e-3, 100e-3, 10)
        diameter = np.linspace(1e-3, 10e-3, 100)

        colors = self.get_cmap(len(length))

        for i, l in enumerate(length):

            tube_resistance = [Tube(d, l).R() for d in diameter]

            ax1.plot(diameter, tube_resistance, color=colors[i], label=f'{l :.4f} m')

        plt.legend(title='Length')
        self._dump(fig, 'tube_diameter')

if __name__ == '__main__':
    

    plot = PlotTubes()
    plot.plot()