from library.componentes.chamber import PlotPump, Pump_fermi
from library.componentes.velves import Velve, PlotVelve, Velve_fermi
from library.componentes.tubes import Tube, PlotTubes
from library.signals import Rectangle, Sinus, PlotSignal
from simulation.first_order import velve_test, system_test


class SystemManager:

    def get_components(self):
        objects = ['signal', 'velve_in', 'velve_out', 'tube_in', 'tube_out', 'pump']
        result = dict()
        for obj in objects:
            inst = getattr(self, obj)
            attributes = inst.__dict__
            attributes = [i for i in attributes.keys() if i[:1] != '_']
            params = {key: getattr(inst, key) for key in attributes}
            if obj == 'pump':
                params['T'] = self.T
                params['steps'] = self.steps
                params['signal'] = result['signal']
            result[obj] = inst._comp(**params)
        return result

    def get_parameter(self):
        return dict(
            Pr_in=self.Pr_in,
            Pr_out=self.Pr_out,
            Pc0=self.Pc0,
            T=self.T,
            steps=self.steps,
        )

if __name__ == '__main__':

    system = System()
    system.pump.K =  56
    system.velve_in.R_open = 'xxx'
    print(system.get_parameter())
    print(system.get_objects())
