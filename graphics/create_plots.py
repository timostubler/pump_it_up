from matplotlib import cm
import matplotlib.pyplot as plt

class PlotManager:

    root = 'graphics/plots'

    @staticmethod
    def get_cmap(colors, the_cmap='plasma'):
        cmap = cm.get_cmap(the_cmap, colors)
        return [cmap(c) for c in range(colors)]

    def _dump(self, fig, name):
        fig.savefig(f'{self.root}/{name}.png')
        plt.show()

