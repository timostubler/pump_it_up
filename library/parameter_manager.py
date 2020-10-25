from library.componentes.chamber import PumpBase, PlotPump, Pump
from library.componentes.velves import VelveBase, PlotVelve, Velve
from library.componentes.tubes import TubeBase, PlotTubes, Tube
from library.signals import SignalBase, Fermi, Rectangle, Sinus, PlotSignal
import yaml


class ParameterManager:

    _reference_parameters = dict(
        Rv=None,  # ventilwiderstand
        Cp=None,  # pumpkammerkapazität
        Pr1=None,  # reservoirdruck
        Pr2=None,  # reservoirdruck
        Pc0=None,  # startdruck in der pumpkammer
        T=None,  # simulationsdauer
        steps=None,  # anzahl der zeitschritte
    )

    _reference_components = dict(
        pump=None,
        signal=None,
        velve_in=None,
        velve_out=None,
        tube_in=None,
        tube_out=None,
    )

    class parameter:
        Rv=None,  # ventilwiderstand
        Cp=None,  # pumpkammerkapazität
        Pr1=None,  # reservoirdruck
        Pr2=None,  # reservoirdruck
        Pc0=None,  # startdruck in der pumpkammer
        T=None,  # simulationsdauer
        steps=None,  # anzahl der zeitschritte

    class components:
        pump=Pump
        signal=Rectangle
        velve_in=Velve
        velve_out=Velve
        tube_in=Tube
        tube_out=Tube

    def __init__(self, initial_parameters):
        for key, value in initial_parameters.items():
            if hasattr(self.parameter, key):
                setattr(self.parameter, key, value)

        for key, value in initial_parameters.items():
            if hasattr(self.components, key):
                value = getattr(self.components, key)(**value)
                setattr(self.components, key, value)

    def _collect_parameters(self):

        parameter = dict()
        components = dict()

        for key in self._reference_parameters:
            # print(key, getattr(self.parameter, key))
            parameter[key] = self.parameter.__dict__[key]

        for key in self._reference_components:
            # print(key, getattr(self.components, key))
            components[key] = self.components.__dict__[key]
        return parameter, components

    def __call__(self):
        return self._collect_parameters()

    def __str__(self):
        parameters, components = self._collect_parameters()
        return f'\nstorage of {self.__class__.__name__}\nparameters:\n{yaml.dump(parameters)}\ncomponents:\n{yaml.dump(components)}'



if __name__ == '__main__':

    global_parameters = dict(

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
            frequency=1,
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

    parameter = ParameterManager(global_parameters)

    print(parameter)
    parameter.parameter.Cp = 89
    parameter.components.velve_in.R_open = 15235

    v, c = parameter()
    print(v)
    print(c)
