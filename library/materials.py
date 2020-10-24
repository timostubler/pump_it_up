

class Fluid(object):  # Klasse fürs Medium

    def __init__(self):
        self.ethaD = 1 * 10 ** -3  # [Pa/s] dynamische Viskosität von Wasser @T=20°C
        self.Rgs = 1  # spezifische Gaskonstante Rgs
        self.rho = 0.9982067  # [g*cm^-3] Dichte Wasser @T=20°C
        self.T = 293  # K


    def __str__(self):
        return str(self.__dict__)

if __name__ == '__main__':

    material = Fluid()
    print(material)