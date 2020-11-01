from library.componentes.chamber import Pump, PlotPump
from library.componentes.velves import Velve, PlotVelve
from library.componentes.tubes import Tube, PlotTubes
from library.signals import Fermi, Rectangle, Sinus, PlotSignal
from simulation.first_order import velve_test, system_test
from graphics.create_plots import PlotManager
from library.parameter_manager import ParameterManager

import numpy as np


plots = [
    PlotSignal(),
    PlotVelve(),
    PlotPump(),
    PlotTubes()
]


def backpressure():

    running_params = dict(

        Rv=1,  # ventilwiderstand
        Cp=1,  # pumpkammerkapazität
        Pr1=0,  # reservoirdruck
        Pr2=0,  # reservoirdruck
        Pc0=0,  # startdruck in der pumpkammer
        T=30,  # simulationsdauer
        steps=500,  # anzahl der zeitschritte

        pump=dict(

        ),
        signal=dict(
            amplitude=1e5,
            frequency=50e-3,
            offset=0,
            a=1,
        ),
        velve_in=dict(
            R_open=1,
            R_close=1e6,
            direction='forward'
        ),
        velve_out=dict(
            R_open=1,
            R_close=1e6,
            direction='backward'
        ),
        tube_in=dict(
            d=5e-3,
            l=100e-3
        ),
        tube_out=dict(
            d=5e-3,
            l=100e-3
        )
    )

    params = ParameterManager(running_params)

    param_range = np.linspace(0, 1e5, 10) / 1

    chamber_pressure = dict()
    for new_param in param_range:

        # params.components.tube_in.l += new_param
        # params.components.signal.frequency = new_param
        params.parameter.Pr1 = new_param

        components, parameter = params()
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

    backpressure()
