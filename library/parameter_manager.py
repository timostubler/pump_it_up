from library.componentes.chamber import PumpBase, PlotPump, Pump, Pump_fermi
from library.componentes.velves import VelveBase, PlotVelve, Velve, Velve_fermi
from library.componentes.tubes import TubeBase, PlotTubes, Tube
from library.signals import SignalBase, Fermi, Rectangle, Sinus, PlotSignal
import yaml


class ParameterManager:

    _reference_parameters = dict(
        Pr_in=None,  # reservoirdruck
        Pr_out=None,  # reservoirdruck
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
        Pr_in=None,  # reservoirdruck
        Pr_out=None,  # reservoirdruck
        Pc0=None,  # startdruck in der pumpkammer
        T=None,  # simulationsdauer
        steps=None,  # anzahl der zeitschritte

    class components:
        pump=Pump_fermi
        signal=Rectangle
        velve_in=Velve#_fermi
        velve_out=Velve#_fermi
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

    pass