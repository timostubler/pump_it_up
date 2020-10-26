
class ConstantsDict(object):  # Klasse fürs Medium
    ''' Physical Constants'''

    g = 9.81 # [m s^-2]

    def __repr__(self):
        return str(dict(
            g=self.g,
        ))

if __name__ == '__main__':

    constants = ConstantsDict()
    print(constants)