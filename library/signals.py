from graphics.create_plots import PlotManager
import numpy as np


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

class PlotSignal(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):
        t = np.linspace(0.25, 1.75, 500)
        y_data = dict()
        signal = Rectangle(amplitude=5, frequency=1, offset=0)
        y_data[f'Rectangle'] = [signal(ti) for ti in t]

        self.plot_dict(t, y_data,
            title='Rectangle',
            xlabel='Time [s]',
            ylabel='Voltage [V]')

if __name__ == '__main__':

    plot = PlotSignal()
    plot.plot()

