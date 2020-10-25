from numpy import linspace
from scipy.integrate import odeint
from math import sin

def model(signal, R, L, C, T, uc0, i0, steps):

    def dx_dt(x, dt):
        return [x[1] / C, -x[0] / L - x[1] * R / L + signal(dt) / L]

    ts = linspace(0, T * 2, steps)
    res = odeint(dx_dt, [uc0, i0], ts)

    return ts, dict(
        uc=res[:, 0],
        i= res[:, 1],
        ue=[signal(dt) for dt in ts],
    )


if __name__ == '__main__':

    from graphics.create_plots import PlotManager

    class Signal:

        def __init__(self, ue, f):
            self.f = f
            self.ue = ue

        def const(self, dt):
            return self.ue

        def rect(self, dt):
            if (dt % 1 / self.f > 1 / (2 * self.f)):
                return 0
            else:
                return self.ue

        def sinus(self, dt):
            return self.ue * (sin(self.f, dt))

    components = dict(
        signal=Signal(ue=5, f=2).rect,
        R=1e-1, # Ω
        L=1e-3, # H
        C=1e-2, # F
        T=.5, # s
        uc0=0, # V
        i0=0, # A
        steps=500,
    )

    time, y_data = model(**components)

    pm = PlotManager()
    pm.plot_dict(time, y_data,
        title='RLC Schwingkreis',
        xlabel='Time [s]',
        ylabel='Voltage [V]'
    )