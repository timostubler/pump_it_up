

class Fluid(object):  # Klasse fürs Medium
    ''' Parameters for Water @ Normaldruck und T=20°C '''

    nu = 1.004*1e-6 # [m^2 s^-1]
    etha = 1002*1e-6 # [kg m^-1 s^-1]
    rho = 998.21 # [kg/m^-3] Dichte Wasser @T=20°C

    def __repr__(self):
        return str(dict(
            nu=self.nu,
            etha=self.etha,
            rho=self.rho
        ))

if __name__ == '__main__':

    material = Fluid()
    print(material)