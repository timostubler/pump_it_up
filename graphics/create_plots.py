import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os

class PlotManager:

    root = 'graphics/plots'

    _cmaps_container = [
        'viridis', 'plasma', 'seismic', 'viridis_r',
        'binary', 'gist_yarg', 'gist_gray', 'gray',
        'bone', 'pink', 'spring', 'summer',
        'autumn', 'winter', 'cool', 'Wistia',
        'hot', 'afmhot', 'gist_heat', 'copper'
    ]

    def __init__(self):
        self.cmap_type = self._cmaps_container[0]
        self.open_figures = True

    def get_cmap(self, colors):
        """
        :param colors: int
        :return: list of colors
        """
        cmap = cm.get_cmap(self.cmap_type, colors+1)
        cmap = [cmap(c) for c in range(colors+1)]
        cmap.pop()
        return cmap

    def _dump(self, fig, name):
        filepath = f'{self.root}/{name}'.replace('\\', '/')
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        fig.savefig(f'{self.root}/{name}.png')
        self.show()

    def show(self):
        if self.open_figures:
            plt.show()
        else:
            plt.close('all')

    def plot_single(self, x, y, title='', xlabel='', ylabel='', filename=None, **kwargs):
        fig, ax = plt.subplots(1, 1)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.plot(x, y, **kwargs, color=self.get_cmap(2)[0])
        self.show()
        if filename:
            self._dump(fig, filename)

    def plot_dict(self, x, y_dict, title='', xlabel='', ylabel='', filename=None):
        fig, ax = plt.subplots(1, 1)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        labels = list(y_dict)
        colors = self.get_cmap(len(labels))
        for i, label in enumerate(labels):
            # print(label, y_dict[label])
            ax.plot(x, y_dict[label], label=label, color=colors[i])#, marker='.')
        plt.legend()
        self.show()
        if filename:
            self._dump(fig, filename)

    def plot_colormesh(self, z, xy=None, title='', xlabel='x', ylabel='y', filename=None):
        """
        :param z: numpy 2D array
        :param xy: tuple (numpy 1D array, numpy 1D array)
        :param title: string
        :param xlabel: string
        :param ylabel: string
        """
        z = z.transpose()
        if xy:
            x, y = self.meshgrid_from_linspace(*xy)
        else:
            n, m = z.shape
            x, y = self.meshgrid(n, m)

        fig = plt.figure()
        ax = fig.add_subplot(111, title=title)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        im = ax.pcolormesh(x, y, z, cmap=self.cmap_type, shading='auto')
        fig.colorbar(im)
        if filename:
            self._dump(fig, filename)
        self.show()

    def plot_surface(self, z, xy=None, title='', xlabel='x', ylabel='y', zlabel='z'):
        """
        :param z: numpy 2D array
        :param xy: tuple (numpy 1D array, numpy 1D array)
        :param title: string
        :param xlabel: string
        :param ylabel: string
        :param zlabel: string
        """
        if xy:
            z = z.transpose()
            x, y = self.meshgrid_from_linspace(*xy)
        else:
            n, m = z.shape
            x, y = self.mgrid(n, m)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        ax.plot_surface(x, y, z, cmap=self.cmap_type)
        self.show()

    def meshgrid(self, n, m):
        return np.meshgrid(
            np.linspace(0, m, m + 1),
            np.linspace(0, n, n + 1)
        )

    def meshgrid_from_linspace(self, x, y):
        return np.meshgrid(x, y)

    def mgrid(self, n, m):
        return np.mgrid[:n, :m]

    def example(self):
        x = np.linspace(-2*np.pi, 2*np.pi, 60)
        y = np.linspace(-np.pi, np.pi, 30)
        z = np.sin(x[:, None] * y[None, :]) + np.cos(x[:, None] * y[None, :])
        self.plot_colormesh(z, xy=(x, y))
        self.plot_colormesh(z)
        self.plot_surface(z, xy=(x, y))
        self.plot_surface(z)

if __name__ == '__main__':

    pm = PlotManager()
    pm.example()
