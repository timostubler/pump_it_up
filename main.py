from library.signals import PlotSignal
from library.componentes.velves import PlotVelve
from library.componentes.chamber import PlotPump
from library.componentes.tubes import PlotTubes

if __name__ == '__main__':

    plots = [
        PlotSignal(),
        PlotVelve(),
        PlotPump(),
        PlotTubes()
    ]

    for plot in plots:
        plot.plot()