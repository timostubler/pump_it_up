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

    Pr_in = 1e3 # reservoirdruck
    Pr_out = 10e3  # reservoirdruck
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
        RC=0.00001

    class velve_in:
        _comp = Velve
        R_open = 2e6
        R_close = 1e20
        # direction = 'forward'
        direction = 'backward'

    class velve_out:
        _comp = Velve
        R_open = 2e6
        R_close = 1e20
        direction = 'forward'
        # direction = 'backward'

    class tube_in:
        _comp = Tube
        diameter = 1e-3
        length = 100e-3

    class tube_out:
        _comp = Tube
        diameter = 1e-3
        length = 100e-3


def leakage_sweep():

    fname = 'velve_out_Rclose_wflow'

    system = System()

    param_range = np.linspace(1e10, 1e13, 10) / 1
    #param_range = np.linspace(10e-3, 100e-3, 10) / 1

    velve_leakage = dict()
    i=0
    for new_param in param_range:

        sweep_unit = ' [$m^3 s^{-1}/Pa$]'
        # system.velve_in.R_close = new_param
        system.velve_out.R_close = new_param

        print('R_close:', new_param)

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = system_test(**components, **parameter)

        if i==0:
            velve_leakage.update({'signal_voltage': y_data['signal_voltage']})

        # velve_leakage.update({f'{round(new_param*1e-9)}'+f' *1e9 {sweep_unit}':y_data['chamber']})
        velve_leakage.update({f'{round(new_param*1e-9)}' + f' *1e9 {sweep_unit}': y_data['flow']})

        pm = PlotManager()

        pm.plot_dict(time, y_data,
                     title='',
                     xlabel='Time [s]',
                     ylabel='Voltage / Pressure / Flow (normal.)',
                     filename=f'{fname}/{round(new_param*1e-9)}')

        i+=1

    pm.plot_dict(time, velve_leakage,
                 title='',
                 xlabel='Time [s]',
                 ylabel='Voltage / Flow (normal.)',
                 filename=f'{fname}/leakage_sweep')


if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    leakage_sweep()
