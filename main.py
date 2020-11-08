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

    Pr_in = 10e3 # reservoirdruck
    Pr_out = -10e3  # reservoirdruck
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
        RC=0.00001

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


def leakage_sweep():

    fname = 'velve_in_Rclose'

    system = System()

    param_range = np.linspace(1e10, 1e15, 10) / 1
    #param_range = np.linspace(10e-3, 100e-3, 10) / 1

    velve_leakage = dict()
    for new_param in param_range:

        sweep_unit = ' [Res.]'
        system.velve_in.R_close = new_param
        # system.velve_out.R_close = new_param

        print('R_close:', new_param)

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = system_test(**components, **parameter)
        velve_leakage.update({f'{new_param:.4f}'+f'{sweep_unit}':y_data['chamber']})
        # velve_leakage.update({f'{new_param:.4f}' + f'{sweep_unit}': y_data['flow']})

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

    velve_leakage.update({'signal_voltage': y_data['signal_voltage']})
    pm.plot_dict(time, velve_leakage,
                 title='',
                 xlabel='Time [s]',
                 ylabel='Voltage / Pressure (normal.)',
                 filename=f'{fname}/length_sweep')


if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    leakage_sweep()
