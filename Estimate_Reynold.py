import numpy as np

''' Estimate Reynolds-Number as first guess '''
# Rohrparameter
d = 1*1e-3 # m
l = 0.3 # m
A = np.pi*(d/2)**2

# Pumpenauslegung und Druckdifferenz
delta_p = 50*1e3 # Pa
# SToffwerte @ 20°C
etha_w = 1002.0*1e-6 # kg m^-1 s^-1
nu_w = 1.004 *1e-6 # m^2 s^-1
rho_w = 998.21 # kg/m^-3

# Hagen-Poiseuille-Law:
dV_dt = (np.pi*((d/2)**4)*delta_p)/(8*etha_w*l)

# Mittlere Geschwindigkeit:
v_m = dV_dt/A

# Reynolds-Formula:
Rey = (v_m*d)/nu_w
print(f'Reynolds-Number is: {Rey}')

# Calculate Pipe Friction Parameter lambda:
lambda_pipe = 64/Rey

''' Get Resistance Support Values for Pipe Elbows ''' # from table
# Correspondence data of Reynolds number and res. zeta values (for 90° and R/D=4)
rey_zeta_elbow_data = [[500,1.6],[550,1.5],[600,1.4],[700, 1.2], [800,1.2], [1000,0.9],[2000,0.575]]

if __name__ == '__main__':
    pass