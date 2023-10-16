from PyQt6 import QtCore, QtWidgets

from pyqt_test.plot import MplCanvas, MpWidget

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 test")

        fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)
        plot = {"fig": fig, "axs": axs}

        sc = MplCanvas(parent=self, width=12, height=7, dpi=100, plot=plot)
        #sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        x = np.linspace(0, 3 * np.pi, 500)
        y = np.sin(x)
        dydx = np.cos(0.5 * (x[:-1] + x[1:]))  # first derivative

        # Create a set of line segments so that we can color them individually
        # This creates the points as a N x 1 x 2 array so that we can stack points
        # together easily to get the segments. The segments array for line collection
        # needs to be (numlines) x (points per line) x 2 (for x and y)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)     

        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(dydx.min(), dydx.max())
        lc = LineCollection(segments, cmap='viridis', norm=norm)
        # Set the values used for colormapping
        lc.set_array(dydx)
        lc.set_linewidth(2)
        line = axs[0].add_collection(lc)
        fig.colorbar(line, ax=axs[0])

        # Use a boundary norm instead
        cmap = ListedColormap(['r', 'g', 'b'])
        norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(dydx)
        lc.set_linewidth(2)
        line = axs[1].add_collection(lc)
        fig.colorbar(line, ax=axs[1])

        axs[0].set_xlim(x.min(), x.max())
        axs[0].set_ylim(-1.1, 1.1)
        

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = MpWidget(sc)
        self.setCentralWidget(widget)
