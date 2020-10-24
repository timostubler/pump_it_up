import pandas as pd
import numpy as np
from scipy.integrate import odeint

from library.materials import Fluid
from library.signals import Signal
from library.componentes.chamber import Pump
from library.componentes.velves import Velve
from library.componentes.tubes import Tube

Pump1 = Pump()
Tube1 = Tube()

#Druckamplitude und Offset aus Pumpenparametern berechnen
VAmp = Pump1.VAmp
VOff = Pump1.VOff

Cp = 1 # pumpkammerkapazität
Rs = 2 # Dummy schlauchwiderstand
Rv = 1 # ventilwiderstand

Pr1 = 0 # reservoirdruck
Pr2 = 0 # reservoirdruck
Pc0 = 0 # startdruck in der pumpkammer

T = 35*(Rs+Rv)*Cp # ladedauer | warum nicht faktor 5 !?
steps = 500 # anzahl der zeitschritte
t_space = np.linspace(0, 3*T, steps, endpoint=True)

Signal1 = Signal(amplitude=VAmp, frequency=1/T, offset=VOff)
Vs = Signal1.fermi_edges # Spannungs-Anregungssignal der pumpe
Ps = Pump1.pressure # Druck-Anregungssignal der pumpe

Velve1 = Velve(R=Rv)  
Rvelve1 = Velve1.const # ventiltyp

Velve2 = Velve(R=Rv)
Rvelve2 = Velve2.const
    
i_scale = 5 # hängt auch von der anzahl der zeitschritte ab!

##############################################################################

def dp_dt(p, t):
    Vsignal = Vs(t, a=0.01)
    Psignal = Ps(Vsignal)
    p = p[0]
    # pv1 = Rv*(Psignal-Pr1-p)/(Rv+Rs)
    # pv2 = Rv*(Psignal-Pr2-p)/(Rv+Rs)
    pv1 = Psignal-Pr1-p-Rs*(Psignal-Pr1-p)/(Rv+Rs)
    pv2 = Psignal-Pr2-p-Rs*(Psignal-Pr2-p)/(Rv+Rs)
    return Cp*((Psignal-Pr1-p)/(Rs+Rvelve1(pv1))+(Psignal-Pr2-p)/(Rs+Rvelve2(pv2)))#, Psignal
    
Pc = odeint(dp_dt, Pc0, t_space)[:,0]

data = pd.DataFrame(columns = ['t', 'Ps', 'Pc', 'Pr1', 'Pr2', 'i'])
data['Pc'] =  Pc
data['t'] =  t_space
#data['Ps'] = [Psignal for t in t_space]
data['Pr1'] = [Pr1 for _ in t_space]
data['Pr2'] = [Pr2 for _ in t_space]
data['i'] = np.gradient(Pc)*i_scale

axes = data.plot(x='t', y=['Ps', 'Pc', 'Pr1', 'Pr2', 'i'], grid=True)
axes.set_title('Simple Pump')
axes.set_xlabel('Time [s]')
axes.set_ylabel('Voltage [V]')

print('nettostrom:', data['i'].sum())

