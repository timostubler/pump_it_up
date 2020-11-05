from scipy.integrate import odeint
import numpy as np

def velve_test(signal, pump, velve_in, tube_in, Pc0, Pr1, T, steps, **kwargs):

    def dp_dt(pc, t):
        Cp = pump.C(signal(t))
        Psignal = pump.p(signal(t))
        pv_in = 0  # Psignal - Pr1 - p - tube_in.R * (Psignal - Pr1 - p) / (velve_in.R_last+ tube_in.R)
        return (Psignal - pc + Pr1) / ((tube_in.R + velve_in.R(pv_in)) * Cp)  # f(x)

    t_space = np.linspace(0, T, steps, endpoint=True)
    Pc = odeint(dp_dt, Pc0, t_space)[:, 0]
    Ps = [signal(t) for t in t_space]
    Pr1 = [Pr1 for _ in t_space]
    i = np.gradient(Pc)
    i /= i.max()
    return t_space, dict(
        signal=Ps / np.abs(Ps).max(),
        chamber=Pc / np.abs(Pc).max(),
        reservoir_in=Pr1 / Pr1.max(),
        #flow=i,
    )

count = 0
def system_test(signal, pump, velve_in, velve_out, tube_in, tube_out,
          Pr1, Pr2, Pc0, T, steps):
    print(steps)

    def dp_dt(p, t):
        p = p[0]
        global count
        count += 1
        print(f'count {count}:', t, velve_in.R_last)
        Psignal = pump.p(signal(t))
        Cp = pump.C(signal(t))
        # TODO: check R_last
        pv_in = Psignal - Pr1 - p - tube_in.R * (Psignal - Pr1 - p) / (velve_in.R_last+ tube_in.R)
        pv_out = Psignal - Pr2 - p - tube_out.R * (Psignal - Pr2 - p) / (velve_out.R_last + tube_out.R)
        print(f'pv in: {pv_in} pv out: {pv_out}')
        i1 = (Psignal - Pr1 - p) / (tube_in.R + velve_in.R(pv_in))
        i2 = (Psignal - Pr2 - p) / (tube_out.R + velve_out.R(pv_out))
        return (i1 + i2) / Cp

    t_space = np.linspace(0, T, steps, endpoint=True)
    result = odeint(dp_dt, Pc0, t_space, printmessg=True)
    Pc = result[:, 0]

    Ps = np.array([signal(t) for t in t_space])
    Pr1 = np.array([Pr1 for _ in t_space])
    Pr2 = np.array([Pr2 for _ in t_space])
    i = np.gradient(Pc)
    i /= i.max()
    print('nettostrom:', i.sum())

    return t_space, dict(
        signal=Ps / np.abs(Ps).max(),
        chamber=Pc / np.abs(Pc).max(),
        reservoir_in=Pr1 / Pr1.max(),
        reservoir_out=Pr2 / Pr2.max(),
        #flow=i,
    )


if __name__ == '__main__':

    from library.parameter_manager import ParameterManager
    from graphics.create_plots import PlotManager
    from library.componentes.chamber import Pump
    from library.componentes.velves import Velve
    from library.componentes.tubes import Tube
    from library.signals import Fermi, Rectangle, Sinus

    running_params = dict(

        Rv=1,  # ventilwiderstand
        Cp=1,  # pumpkammerkapazität
        Pr1=0,  # reservoirdruck
        Pr2=0,  # reservoirdruck
        Pc0=0,  # startdruck in der pumpkammer
        T=150,  # simulationsdauer
        steps=500,  # anzahl der zeitschritte

        pump=dict(),
        signal=dict(
            amplitude=1,
            frequency=10e-3,
            offset=0,
            a=1,
        ),
        velve_in=dict(
            R_open=1,
            R_close=1,
            direction='forward'
        ),
        velve_out=dict(
            R_open=1,
            R_close=1,
            direction='backward'
        ),
        tube_in=dict(
            d=1,
            l=1
        ),
        tube_out=dict(
            d=1,
            l=1
        )
    )

    params = ParameterManager(running_params)

    # params.parameter.Pr1 = 1
    # params.components.signal.frequency = 1

    components, parameter = params()
    time, y_data = system_test(**components, **parameter)

    pm = PlotManager()
    pm.plot_dict(time, y_data,
        title='Simple Pump',
        xlabel='Time [s]',
        ylabel='Voltage [V]',
        filename='simulation_full')
