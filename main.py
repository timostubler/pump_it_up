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


def corner_frequency():

    amplitude = []
    pm = PlotManager()
    system = System()

    frequency_range = np.linspace(2e3, 500e3, 301)

    chamber_pressure = dict()

    for i, frequency in enumerate(frequency_range):
        print(frequency)
        # system.tube_in.length = new_param
        system.signal.frequency = frequency
        system.T = 2 / frequency

        components = system.get_components()
        parameter = system.get_parameter()
        time, y_data = system_test(**components, **parameter)

        if not i:
            chamber_pressure.update({'signal': y_data['signal']})


        amplitude.append(max(abs(y_data['chamber'])))

        chamber_pressure.update({f'{frequency//1000} kHz':y_data['chamber']})


        # pm.plot_dict(time*1e3, y_data,
        #              title='',
        #              xlabel='Time [ms]',
        #              ylabel='Pressure [#]',
        #              filename=f'frequency/{frequency:.4f} Hz')

    amplitude = np.array(amplitude)

    pm.plot_dict(time*1e6, chamber_pressure,
                 title='',
                 xlabel='Time [#]',
                 ylabel='Chamber pressure [#]',
                 filename=f'frequency/frequency_sweep')


    pm.plot_dict(frequency_range/1000, {'amplitude': amplitude/1000},
                 title='',
                 xlabel='Frequency [kHz]',
                 ylabel='Chamber pressure amplitude [kHz]',
                 filename=f'frequency/frequency_sweep')

    print(frequency_range)
    print(amplitude)

    import matplotlib.pyplot as plt

    plt.figure()
    #plt.semilogx(frequency_range, amplitude)

    # plt.xscale('log')
    plt.xlabel('Frequency [kHz]')
    plt.ylabel('Magnitude [dB]')

    # plt.plot(frequency_range, (np.log10(amplitude)+2)/2)
    # plt.plot(frequency_range, np.log10(amplitude))
    amplitude = 20*np.log10(amplitude/amplitude.max())
    plt.semilogx(frequency_range, amplitude)
    plt.show()

if __name__ == '__main__':

    # for plot in plots:
    #     plot.plot()

    corner_frequency()
