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
        RC=0.00001

    class velve_in:
        _comp = Velve
        R_open = 2e6
        R_close = 1e15
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


def backpressure():


    system = System()

    external_pressure = np.linspace(0, 1e5, 10)

    chamber_pressure = dict()

    for pressure in external_pressure:

        # system.tube_in.length = new_param
        system.Pr_in = pressure

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = system_test(**components, **parameter)
        chamber_pressure.update({f'{pressure:.4f}':y_data['chamber']})

        pm = PlotManager()
        pm.plot_dict(time, y_data,
                     title='Simple Pump',
                     xlabel='Time [s]',
                     ylabel='Voltage [V]',
                     filename=f'backpressure/{pressure:.4f}')

    chamber_pressure.update({'signal_voltage': y_data['signal_voltage']})
    pm.plot_dict(time, chamber_pressure,
                 title='External Pressure on Reservoir',
                 xlabel='Time [s]',
                 ylabel='Chamber pressure [Pa]',
                 filename=f'backpressure/pressure_sweep')


if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    backpressure()
