from library.componentes.chamber import PlotPump, Pump_fermi, Pump_old
from library.componentes.velves import Velve, PlotVelve, Velve_fermi
from library.componentes.tubes import Tube, PlotTubes
from library.signals import Rectangle, Sinus, PlotSignal
from simulation.first_order import velve_test, system_test
from graphics.create_plots import PlotManager
from system_manager import SystemManager
import numpy as np

plots = [
    PlotSignal(),
    PlotVelve(),
    PlotPump(),
    PlotTubes()
]


class System(SystemManager):

    Pr_in = 0 # reservoirdruck
    Pr_out = 0  # reservoirdruck
    Pc0 = 0  # startdruck in der pumpkammer
    T = 1e-3  # simulationsdauer
    steps = 100  # anzahl der zeitschritte

    class signal:
        _comp = Rectangle
        amplitude = 1
        frequency = 2e3
        offset = 0

    class pump():
        _comp = Pump_fermi
        K = 1
        RC = 0.00001

    class velve_in:
        _comp = Velve
        R_open = 2e6
        R_close = 1e20
        direction = 'forward'
        # direction = 'backward'

    class velve_out:
        _comp = Velve
        R_open = 2e6
        R_close = 1e20
        # direction = 'forward'
        direction = 'backward'

    class tube_in:
        _comp = Tube
        diameter = 1e-3
        length = 100e-3

    class tube_out:
        _comp = Tube
        diameter = 1e-3
        length = 100e-3


def backpressure():

    """
    veleve in geht bei 44.44 kPa nicht mehr auf
    vevel_out geht bei 50 kPa nicht mehr auf
    """

    amplitude_in = dict()
    amplitude_out = dict()

    pm = PlotManager()

    system = System()

    external_pressure = np.linspace(0, 0.6e5, 31)

    chamber_pressure = dict()

    for i, pressure in enumerate(external_pressure):



        # system.tube_in.length = new_param
        system.Pr_in = pressure
        system.Pr_out = -pressure

        pres_label = pressure//1000

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = system_test(**components, **parameter)

        if not i:
            chamber_pressure.update({'signal': y_data['signal_voltage']})

        chamber_pressure.update({f'{pres_label} kPa':y_data['chamber']})

        amplitude_in[pres_label] = max(y_data['chamber'])
        amplitude_out[pres_label] = min(y_data['chamber'])

        # pm.plot_dict(time*1e3, y_data,
        #              title='',
        #              xlabel='Time [ms]',
        #              ylabel='Pressure [#]',
        #              filename=f'backpressure/{pressure:.4f}')

        print(f'{(i + 1) / len(external_pressure) * 100 :.2f} %')

    pm.plot_dict(time*1e3, chamber_pressure,
                 title='',
                 xlabel='Time [ms]',
                 ylabel='Pressure [#]',
                 filename=f'backpressure/backpressure_sweep')

    print(amplitude_in)
    print(amplitude_out)

    amplitude = dict()
    amplitude['Pr in'] = list(amplitude_in.values())
    amplitude['Pr out'] = list(amplitude_out.values())


    pm.plot_dict(list(amplitude_in.keys()), amplitude,
                 title='',
                 xlabel='External pressure [kPa]',
                 ylabel='Chamber pressure [#]',
                 filename=f'backpressure/backpressure_sweep')


if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    backpressure()
