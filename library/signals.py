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

class Constant(SignalBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, t):
            return self.amplitude + self.offset

class RectangleCount(SignalBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i=0

    def __call__(self, t):
        if (t % (1/self.frequency)) <= (1/self.frequency) / 2:
            self.i += 1
            if self.i < 2:
                return self.amplitude + self.offset
            else:
                return 0.001
        else:
            if self.i == 1:
                return -self.amplitude + self.offset
            else:
                return 0.001

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
        return self.amplitude * (np.sin(2 * np.pi * self.frequency * t)) + self.offset

class PlotSignal(PlotManager):

    def __init__(self):
        super().__init__()

    def plot(self):
        t = np.linspace(0, 1e-3, 1000)
        print(t)
        y_data = dict()
        signal = Sinus(amplitude=5, frequency=3e3, offset=0)
        print(signal)
        y_data[f'Rectangle'] = [signal(ti) for ti in t]

        self.plot_dict(t, y_data,
            title='Rectangle',
            xlabel='Time [s]',
            ylabel='Voltage [V]')

if __name__ == '__main__':

    plot = PlotSignal()
    plot.plot()

