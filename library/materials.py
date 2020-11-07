

class Fluid(object):  # Klasse fürs Medium

    ethaD = 1e-3  # [Pa*s] dynamische Viskosität von Wasser @T=20°C
    Rgs = 1  # spezifische Gaskonstante Rgs
    rho = 0.9982067  # [g*cm^-3] Dichte Wasser @T=20°C
    T = 293  # K


if __name__ == '__main__':

    material = Fluid()
    print(material)