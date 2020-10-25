from graphics.create_plots import PlotManager
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import unit_impulse


class SignalBase:

    amplitude = None
    frequency = None
    offset = None

    def __init__(self, amplitude=None, frequency=None, offset=None, **kwargs):
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset

    def __repr__(self):
        return str(dict(
            amplitude=self.amplitude,
            frequency=self.frequency,
            offset =self.offset
        ))

class Rectangle(SignalBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, t):
        if (t % (1/self.frequency)) <= (1/self.frequency) / 2:
            return self.amplitude + self.offset
        else:
            return -self.amplitude + self.offset

class Sinus(SignalBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, t):
        return self.amplitude * (np.sin(2 * np.pi * t / (1/self.frequency))) + self.offset

    """
    a: Value for slope steepness of fermi edge
    t: Time, fermi edge located by modulo logic
    """

class Fermi(SignalBase):

    a = None

    def __init__(self, a, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a = a

    def __call__(self, t):
        # intermediate points
        if (t % (1/self.frequency)) == ((1/self.frequency) / 4):  # or t <= (1/self.frequency)/4:
            return self.amplitude + self.offset
        if (t % (1/self.frequency)) == (3 * (1/self.frequency) / 4):
            return -self.amplitude + self.offset

        # falling edge regime
        if (t % (1/self.frequency)) < (3 * (1/self.frequency) / 4) and (t % (1/self.frequency)) > ((1/self.frequency) / 4):
            return 2 * self.amplitude / (
                        np.exp((t % (1/self.frequency) - (1/self.frequency) / 2) / self.a) + 1) - self.amplitude + self.offset

        # rising edge regime
        if t == 0:
            return 0 + + self.offset

        if (t % (1/self.frequency)) < ((1/self.frequency) / 4) and t < (1/self.frequency) / 2:
            return -2 * self.amplitude / (np.exp((t % (1/self.frequency) - 0) / self.a) + 1) + self.amplitude + self.offset

        if (t % (1/self.frequency)) > (3 * (1/self.frequency) / 4) and (t % (1/self.frequency)) < (1/self.frequency):
            return -2 * self.amplitude / (
                        np.exp((t % (1/self.frequency) - (1/self.frequency)) / self.a) + 1) + self.amplitude + self.offset

        if (t % (1/self.frequency)) == 0:
            return 0 + self.offset

        if (t % (1/self.frequency)) < ((1/self.frequency) / 4) and (t % (1/self.frequency)) > 0 and t > (1/self.frequency) / 2:
            return -2 * self.amplitude / (np.exp((t % (1/self.frequency) - 0) / self.a) + 1) + self.amplitude + self.offset

    def __repr__(self):
        return str(dict(
            amplitude=self.amplitude,
            frequency=self.frequency,
            offset =self.offset,
            a=self.a
        ))

class Diraac(SignalBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, t):
        if (t % (1/self.frequency)) == 0:
            return unit_impulse(t)
        elif (t % (1/self.frequency) and t % (1/self.frequency)/2) == 0:
            return -unit_impulse(t)


class PlotSignal(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):

        t = np.linspace(0.25, 1.75, 500)
        fermi_params = np.linspace(0.005, 0.025, 5)

        y_data = dict()
        for ai in fermi_params:
            signal = Fermi(amplitude=5, frequency=1, a=ai, offset=0)
            y_data[f'fermi a={ai}'] = [signal(ti) for ti in t]

        self.plot_dict(t, y_data,
            title='Fermi',
            xlabel='Time [s]',
            ylabel='Voltage [V]')

if __name__ == '__main__':

    plot = PlotSignal()
    plot.plot()

