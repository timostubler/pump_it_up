from library.componentes.chamber import Pump, PlotPump
from library.componentes.velves import Velve, PlotVelve
from library.componentes.tubes import Tube, PlotTubes
from library.signals import Fermi, Rectangle, Sinus, PlotSignal
from simulation.first_order import tube_test, velve_test, system_test
from graphics.create_plots import PlotManager


parameter = dict(
    Rv=1,  # ventilwiderstand
    Cp=1,  # pumpkammerkapazität
    Pr1=0,  # reservoirdruck
    Pr2=0,  # reservoirdruck
    Pc0=0,  # startdruck in der pumpkammer
    T=150,  # simulationsdauer
    steps=500,  # anzahl der zeitschritte
)

components = dict(
    pump=Pump(),
    signal=Fermi(amplitude=1, frequency=1 / 70, a=1),
    velve_in=Velve(R_open=1, R_close=100, direction='backward'),
    velve_out=Velve(R_open=1, R_close=10, direction='forward'),
    tube_in=Tube(d=1, l=1),
    tube_out=Tube(d=1, l=1),
)

plots = [
    PlotSignal(),
    PlotVelve(),
    PlotPump(),
    PlotTubes()
]


for plot in plots:
    plot.plot()


time, y_data = velve_test(**components, **parameter)

pm = PlotManager()
pm.plot_dict(time, y_data,
             title='Simple Pump',
             xlabel='Time [s]',
             ylabel='Voltage [V]',
             filename='simulation_full')
