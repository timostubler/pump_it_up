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

    Pr_in = 0e3 # reservoirdruck
    Pr_out = 0e3  # reservoirdruck
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

    fname = 'leakage_velve_in_Rclose'

    system = System()

    param_range1 = np.linspace(1e14, 1e15, 8) / 1
    # param_range1 = param_range1[::-1]

    param_range2 = np.linspace(2e15, 1e16, 2) / 1
    # param_range2 = param_range2[::-1]

    param_range = np.concatenate([param_range1,param_range2])
    param_range = param_range[::-1]
    velve_leakage = dict()
    i=0
    for new_param in param_range:

        sweep_unit = ' [$m^3 s^{-1}/Pa$]'
        system.velve_in.R_close = new_param
        # system.velve_out.R_close = new_param

        print('R_close:', new_param)

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = velve_test(**components, **parameter)

        if i==0:
            velve_leakage.update({'signal_voltage': y_data['signal_voltage']})

        velve_leakage.update({f'{round(new_param*1e-9)}':y_data['chamber']})
        # velve_leakage.update({f'{round(new_param*1e-9)}':y_data['flow']})

        pm = PlotManager()

        # pm.plot_dict(time, y_data,
        #              title='',
        #              xlabel='Time [s]',
        #              ylabel='Voltage / Pressure / Flow (normal.)',
        #              filename=f'{fname}/{round(new_param*1e-9)}')

        i+=1



    pm.plot_dict(time, velve_leakage,
                 title='',
                 xlabel='Time [s]',
                 ylabel='Voltage / Pressure (normal.)',
                 filename=f'{fname}/leakage_sweep')


if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    leakage_sweep()
