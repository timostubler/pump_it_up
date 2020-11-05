from library.componentes.chamber import PlotPump
from library.componentes.velves import Velve, PlotVelve
from library.componentes.tubes import Tube, PlotTubes
from library.signals import Rectangle, Sinus, PlotSignal
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

        Pr_in=0,  # reservoirdruck
        Pr_out=0,  # reservoirdruck
        Pc0=0,  # startdruck in der pumpkammer
        T=1e-6,  # simulationsdauer
        steps=500,  # anzahl der zeitschritte

        pump=dict(
        ),
        signal=dict(
            amplitude=1e5,
            frequency=1000e3,
            offset=0,
            a=1,
        ),
        velve_in=dict(
            R_open=2e6,
            R_close=1e11,
            direction='forward',
            #direction='backward',
        ),
        velve_out=dict(
            R_open=2e6,
            R_close=1e15,
            #direction='forward',
            direction='backward',
        ),
        tube_in=dict(
            diameter=1e-3,
            length=100e-3
        ),
        tube_out=dict(
            diameter=1e-3,
            length=100e-3
        )
    )

    params = ParameterManager(running_params)

    param_range = np.linspace(0, 1e5, 10) / 1

    chamber_pressure = dict()
    for new_param in param_range:

        # params.components.tube_in.length += new_param
        # params.components.signal.frequency = new_param
        params.parameter.Pr_in = new_param

        components, parameter = params()
        time, y_data = velve_test(**components, **parameter)
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
