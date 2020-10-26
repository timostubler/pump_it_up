from library.componentes.chamber import Pump, PlotPump
from library.componentes.velves import Velve, PlotVelve
from library.componentes.tubes import Tube, PlotTubes
from library.signals import Fermi, Rectangle, Sinus, PlotSignal
from simulation.first_order import tube_test, velve_test, system_test
from graphics.create_plots import PlotManager
from library.parameter_manager import ParameterManager

import numpy as np


plots = [
    PlotSignal(),
    PlotVelve(),
    PlotPump(),
    PlotTubes()
]
for plot in plots:
    plot.plot()

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

# Parameter Sweep Exemplary Function:
def change_external_pressure():

    param_range = np.linspace(1, 10, 10)/100

    for new_param in param_range:

        # params.parameter.Pr1 = new_param
        params.components.signal.frequency = new_param

        components, parameter = params()
        time, y_data = system_test(**components, **parameter)

        pm = PlotManager()
        pm.plot_dict(time, y_data,
                     title='Simple Pump',
                     xlabel='Time [s]',
                     ylabel='Voltage [V]',
                     filename='simulation_full')


if __name__ == '__main__':

    change_external_pressure()
