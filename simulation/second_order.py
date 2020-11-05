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

    pass