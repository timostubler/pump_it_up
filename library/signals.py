from graphics.create_plots import PlotManager
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import unit_impulse


class Signal:

    def __init__(self, amplitude, frequency, offset=0):
        self.amplitude = amplitude
        self.period = 1 / frequency
        self.offset = offset

    def rect(self, t):
        if (t % self.period) <= self.period / 2:
            return self.amplitude + self.offset
        else:
            return -self.amplitude + self.offset

    def sin(self, t):
        return self.amplitude * (np.sin(2 * np.pi * t / self.period)) + self.offset

    """
    a: Value for slope steepness of fermi edge
    t: Time, fermi edge located by modulo logic
    """

    def fermi_edges(self, t, a):

        # a=0.01

        # intermediate points
        if (t % self.period) == (self.period / 4):  # or t <= self.period/4:
            return self.amplitude + self.offset
        if (t % self.period) == (3 * self.period / 4):
            return -self.amplitude + self.offset

        # falling edge regime
        if (t % self.period) < (3 * self.period / 4) and (t % self.period) > (self.period / 4):
            return 2 * self.amplitude / (
                        np.exp((t % self.period - self.period / 2) / a) + 1) - self.amplitude + self.offset

        # rising edge regime
        if t == 0:
            return 0 + + self.offset

        if (t % self.period) < (self.period / 4) and t < self.period / 2:
            return -2 * self.amplitude / (np.exp((t % self.period - 0) / a) + 1) + self.amplitude + self.offset

        if (t % self.period) > (3 * self.period / 4) and (t % self.period) < self.period:
            return -2 * self.amplitude / (
                        np.exp((t % self.period - self.period) / a) + 1) + self.amplitude + self.offset

        if (t % self.period) == 0:
            return 0 + self.offset

        if (t % self.period) < (self.period / 4) and (t % self.period) > 0 and t > self.period / 2:
            return -2 * self.amplitude / (np.exp((t % self.period - 0) / a) + 1) + self.amplitude + self.offset


    def dirac(self, t):
        if (t % self.period) == 0:
            return unit_impulse(t)
        elif (t % self.period and t % self.period/2) == 0:
            return -unit_impulse(t)


class PlotSignal(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):

        fig, ax1 = plt.subplots(1, 1)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Voltage [V]')

        t = np.linspace(0.25, 1.75, 500)
        fermi_params = np.linspace(0.005, 0.025, 5)
        colors = self.get_cmap(len(fermi_params)+1)

        signal = Signal(amplitude=5, frequency=1)
        rect = [signal.rect(ti) for ti in t]

        ax1.plot(t, rect, label='rectangle', color=colors[0])
        for i, ai in enumerate(fermi_params):
            fermi = [signal.fermi_edges(ti, a=ai) for ti in t]
            ax1.plot(t, fermi, label=f'fermi a={ai}', color=colors[i+1])

        sinus = [signal.sin(ti) for ti in t]
        ax1.plot(t, sinus, label='sinus', color=colors[0])
        
        # dirac = [signal.dirac(ti) for ti in t]
        # ax1.plot(t, dirac, label='dirac', color=colors[0])

        plt.legend()

        self._dump(fig, 'signal')



if __name__ == '__main__':

    plot = PlotSignal()
    plot.plot()

