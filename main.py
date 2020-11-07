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
    steps = 1000  # anzahl der zeitschritte

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
        diameter = 1*1e-3
        length = 100e-3

    class tube_out:
        _comp = Tube
        diameter = 1*1e-3
        length = 100e-3


def tube_length_sweep():

    fname = 'tube_both_length_wflow'

    system = System()

    param_range = np.linspace(100*1e-3, 100000*1e-3, 10) / 1
    #param_range = np.linspace(10e-3, 100e-3, 10) / 1

    tube_length = dict()
    for new_param in param_range:

        sweep_unit = ' [m]'
        system.tube_in.length = new_param
        system.tube_out.length = new_param

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = system_test(**components, **parameter)
        # tube_length.update({f'{new_param:.4f}'+f'{sweep_unit}':y_data['chamber']})
        tube_length.update({f'{new_param:.4f}' + f'{sweep_unit}': y_data['flow']})

        pm = PlotManager()
        # pm.plot_twin(time, y_data['signal_voltage'], y_data['chamber'],
        #              title='',
        #              xlabel='Time [s]',
        #              ylabel1='Voltage [V]',
        #              ylabel2='Pressure [Pa]',
        #              filename=f'{fname}/{new_param:.4f}')

        # pm.plot_dict(time, y_data,
        #              title='',
        #              xlabel='Time [s]',
        #              ylabel='Voltage / Pressure (normal.)',
        #              filename=f'{fname}/{new_param:.4f}')

    tube_length.update({'signal_voltage': y_data['signal_voltage']})
    pm.plot_dict(time, tube_length,
                 title='',
                 xlabel='Time [s]',
                 ylabel='Voltage / Flow (normal.)',
                 filename=f'{fname}/length_sweep')


if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    tube_length_sweep()
