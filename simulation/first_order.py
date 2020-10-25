from scipy.integrate import odeint
import numpy as np

def tube_test(signal, tube_in, Cp, Pr1, Pc0, T, steps, **kwargs):

    def dp_dt(pc, t):
        return (signal(t) - pc) / (tube_in.R * Cp)  # f(x)

    t_space = np.linspace(0, T, steps, endpoint=True)
    Pc = odeint(dp_dt, Pc0, t_space)[:, 0]
    Ps = [signal(t) for t in t_space]
    Pr1 = [Pr1 for _ in t_space]
    i_scale = 5  # hängt auch von der anzahl der zeitschritte ab!
    i = np.gradient(Pc) * i_scale
    i /= i.max()
    return t_space, dict(
        signal=Ps,
        chamber=Pc,
        reservoir_in=Pr1,
        #flow=i,
    )

def velve_test(signal, velve_in, Cp, Pr1, Pc0, T, steps, **kwargs):

    def dp_dt(pc, t):
        return (signal(t) - pc) / (velve_in.R(signal(t)-pc) * Cp)  # f(x)

    t_space = np.linspace(0, T, steps, endpoint=True)
    Pc = odeint(dp_dt, Pc0, t_space)[:, 0]
    Ps = [signal(t) for t in t_space]
    Pr1 = [Pr1 for _ in t_space]
    i_scale = 5  # hängt auch von der anzahl der zeitschritte ab!
    i = np.gradient(Pc) * i_scale
    i /= i.max()
    return t_space, dict(
        signal=Ps,
        chamber=Pc,
        reservoir_in=Pr1,
        #flow=i,
    )

def system_test(signal, pump, velve_in, velve_out, tube_in, tube_out,
          Rv, Cp, Pr1, Pr2, Pc0, T, steps):

    def dp_dt(p, t):

        Vsignal = signal(t)
        Psignal = pump.p(Vsignal)
        p = p[0]
        # pv1 = Rv * (Psignal - Pr1 - p) / (Rv + Rs)
        # pv2 = Rv * (Psignal - Pr2 - p) /( Rv + Rs)
        pv1 = Psignal - Pr1 - p - tube_in.R * (Psignal - Pr1 - p) / (Rv + tube_in.R)
        pv2 = Psignal - Pr2 - p - tube_out.R * (Psignal - Pr2 - p) / (Rv + tube_out.R)
        # TODO: unterschiedliche werte für Rv und velve.R()
        i1 = (Psignal - Pr1 - p) / (tube_in.R + velve_in.R(pv1))
        i2 = (Psignal - Pr2 - p) / (tube_out.R + velve_out.R(pv2))
        return Cp * (i1 + i2)

    t_space = np.linspace(0, T, steps, endpoint=True)
    Pc = odeint(dp_dt, Pc0, t_space)[:, 0]

    Ps = [signal(t) for t in t_space]
    Pr1 = [Pr1 for _ in t_space]
    Pr2 = [Pr2 for _ in t_space]
    i_scale = 5  # hängt auch von der anzahl der zeitschritte ab!
    i = np.gradient(Pc) * i_scale
    i /= i.max()
    print('nettostrom:', i.sum())

    return t_space, dict(
        signal=Ps,
        chamber=Pc,
        reservoir_in=Pr1,
        reservoir_out=Pr2,
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
    time, y_data = velve_test(**components, **parameter)

    pm = PlotManager()
    pm.plot_dict(time, y_data,
        title='Simple Pump',
        xlabel='Time [s]',
        ylabel='Voltage [V]',
        filename='simulation_full')
