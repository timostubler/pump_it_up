from scipy.integrate import odeint
import numpy as np

# TODO: check R_last


def velve_test(signal, pump, velve_in, tube_in, Pc0, Pr_in, T, steps, **kwargs):

    def dp_dt(pc, t):
        p = pc[0]
        Cp = pump.C(t)
        Psignal = pump.p(t)
        pv_in = Psignal - Pr_in - p - tube_in.R * (Psignal - Pr_in - p) / (velve_in.R_last + tube_in.R)
        return (Psignal - Pr_in - p) / ((tube_in.R + velve_in.R(pv_in)) * Cp)

    t_space = np.linspace(0, T, steps)
    voltage= np.array([signal(t) for t in t_space])
    Pc = odeint(dp_dt, Pc0, t_space)[:, 0]
    Ps = np.array([pump.p(t) for t in t_space])
    Pr_in = np.array([Pr_in for _ in t_space])
    i = np.gradient(Pc)
    i /= i.max()
    norm = np.abs(Ps).max()
    return t_space, dict(
        signal_voltage= voltage,
        signal_pressure=Ps / norm,
        chamber=Pc / norm,
        reservoir_in=Pr_in / norm,
        #flow=i,
    )

def system_test(signal, pump, velve_in, velve_out, tube_in, tube_out, Pr_in, Pr_out, Pc0, T, steps):

    def dp_dt(p, t):
        p = p[0]
        Psignal = pump.p(t)
        Cp = pump.C(t)
        pv_in = Psignal - Pr_in - p - tube_in.R * (Psignal - Pr_in - p) / (velve_in.R_last + tube_in.R)
        pv_out = Psignal - Pr_out - p - tube_out.R * (Psignal - Pr_out - p) / (velve_out.R_last + tube_out.R)
        i1 = (Psignal - Pr_in - p) / (tube_in.R + velve_in.R(pv_in))
        i2 = (Psignal - Pr_out - p) / (tube_out.R + velve_out.R(pv_out))
        return (i1 + i2) / Cp

    t_space = np.linspace(0, T, steps)
    result = odeint(dp_dt, Pc0, t_space)
    Pc = result[:, 0]
    voltage = np.array([signal(t) for t in t_space])
    Ps = np.array([pump.p(t) for t in t_space])
    Pr_in = np.array([Pr_in for _ in t_space])
    Pr_out = np.array([Pr_out for _ in t_space])
    i = np.gradient(Pc)
    i /= i.max()
    norm = np.abs(Ps).max()
    return t_space, dict(
        signal_voltage= voltage,
        signal_pressure=Ps / norm,
        chamber=Pc / norm,
        reservoir_in=Pr_in / norm,
        reservoir_out=Pr_out / norm,
        flow=i,
    )


if __name__ == '__main__':

    pass