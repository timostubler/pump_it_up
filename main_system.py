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
    T = 1e-6  # simulationsdauer
    steps = 500  # anzahl der zeitschritte

    class pump():
        _comp = Pump_old
        K = 1
        RC = 0.1

    class velve_in:
        _comp = Velve
        R_open = 2e6
        R_close = 1e11
        direction = 'forward'
        # direction = 'backward'

    class velve_out:
        _comp = Velve
        R_open = 2e6
        R_close = 1e15
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

    class signal:
        _comp = Rectangle
        amplitude = 1e5
        frequency = 1000e3
        offset = 0

def corner_frequency():


    system = System()

    param_range = np.linspace(0, 1e5, 10) / 1

    chamber_pressure = dict()
    for new_param in param_range:

        system.Pr_in = new_param

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = system_test(**components, **parameter)
        chamber_pressure.update({f'{new_param:.4f}':y_data['chamber']})

        pm = PlotManager()
        pm.plot_dict(time, y_data,
                     title='Simple Pump',
                     xlabel='Time [s]',
                     ylabel='Voltage [V]',
                     filename=f'backpressure/{new_param:.4f}')

    chamber_pressure.update({'signal': y_data['signal']})
    pm.plot_dict(time, chamber_pressure,
                 title='Backpressure',
                 xlabel='Time [s]',
                 ylabel='Chamber pressure [Pa]',
                 filename=f'backpressure/pressure_sweep')


if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    corner_frequency()
