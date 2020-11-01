from scipy.integrate import odeint
import numpy as np

def velve_test(signal, pump, velve_in, tube_in, Pc0, Pr1, T, steps, **kwargs):

    def dp_dt(pc, t):
        pv_in = 0
        Cp = pump.C(signal(t))
        return (signal(t) - pc + Pr1) / ((tube_in.R + velve_in.R(pv_in)) * Cp)  # f(x)

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

count = 0
def system_test(signal, pump, velve_in, velve_out, tube_in, tube_out,
          Cp, Pr1, Pr2, Pc0, T, steps):
    print(steps)

    def dp_dt(p, t):
        global count
        count += 1
        #print(f't @ {len(velve_in.all_R)}:', t, velve_in.R_last)
        print(f'count {count}:', t, velve_in.R_last)
        Psignal = pump.p(signal(t))
        Cp = 1e-17#(np.pi * ((30e-2) / 2)**2 * 5e-2) / 0.5e5
        p = p[0]
        # pv1 = Rv * (Psignal - Pr1 - p) / (Rv + Rs)
        # pv2 = Rv * (Psignal - Pr2 - p) /( Rv + Rs)
        pv1 = 1e3 #Psignal - Pr1 - p - tube_in.R * (Psignal - Pr1 - p) / (velve_in.R_last+ tube_in.R)
        pv2 = 1e3 #Psignal - Pr2 - p - tube_out.R * (Psignal - Pr2 - p) / (velve_out.R_last + tube_out.R)
        # TODO: unterschiedliche werte für Rv und velve.R()
        i1 = (Psignal - Pr1 - p) / (tube_in.R + velve_in.R_last)
        i2 = (Psignal - Pr2 - p) / (tube_out.R + velve_out.R_last)
        return (i1 + i2) / Cp

    t_space = np.linspace(0, T, steps, endpoint=True)
    #print(t_space)
    #raise BaseException('yeeehaaaa')
    result = odeint(dp_dt, Pc0, t_space, printmessg=True)
    Pc = result[:, 0]
    #info = result[1]['hu']
    #print(f'info: {info}')

    Ps = np.array([signal(t) for t in t_space])
    Pr1 = np.array([Pr1 for _ in t_space])
    Pr2 = np.array([Pr2 for _ in t_space])
    #i_scale = 5  # hängt auch von der anzahl der zeitschritte ab!
    i = np.gradient(Pc) #* i_scale
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
