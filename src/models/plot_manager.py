import numpy as np
import random as rand
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib import style
from scipy.interpolate import griddata
style.use("fivethirtyeight")


class PlotManager():
    """
    Class for simple plot managing.

    Handles the creation and making of graphs.

    Attributes
    ----------
    parent : QLayout
       Layount in which the canvas is shown.
    figure : Figure
        Contains the plot.
    toolbar : NavigationToolbar2QT
        Widget that allows zooming and panning in the graph.
    canvas : FigureCanvasQTAgg
        Canvas for displaying plots.
    """

    def __init__(self, parent):
        """
        Initializes the plot manager

        Parameters
        ----------
        parent : QLayout
            Parent layout.
        """
        self.parent = parent
        self.figure = Figure(figsize=(4, 3), dpi=50)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas)

    def clear(self):
        """
        Removes the current canvas.
        """
        self.parent.removeWidget(self.toolbar)
        self.figure = Figure(figsize=(4, 3), dpi=50)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, coordinates=False)

    def plot2d(self, x: list[float | int], y: list[float | int], prediction: list[float | int], labels: list[str]):
        """
        Fills the figure with a 2d plot using the data provided.
        """
        axes = self.figure.add_subplot(111)
        axes.set_facecolor("none")
        axes.scatter(x, y, label="Datos Reales")
        axes.plot(x, prediction, color="red", label="Línea de Regresión")
        axes.set_xlabel(labels[0])
        axes.set_ylabel(labels[1])
        axes.legend()

    def plot3d(self, x: list[float | int], y: list[float | int], z: list[float | int], prediction: list[float | int], labels: list[str]):
        """
        Fills the figure with a 2d plot using the data provided.
        """
        axes = self.figure.add_subplot(111, projection="3d")
        axes.set_facecolor("none")
        axes.plot(x, y, z, "o", markersize=2,
                  alpha=0.5, label="Datos Reales")
        # Generate a regression plane
        axes.plot(x, y, prediction)

        xi = np.linspace(min(x), max(x), 100)
        yi = np.linspace(min(y), max(y), 100)
        prediction = np.linspace(min(prediction), max(prediction), 100)
        x = rand.choices(x, k=100)
        y = rand.choices(y, k=100)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata((x, y), prediction, (xi, yi), method="linear")

        axes.plot_surface(xi, yi, zi, color="red",
                          alpha=0.5, label="Plano de Regresion")
        axes.set_xlabel(labels[0])
        axes.set_ylabel(labels[1])
        axes.set_zlabel(labels[2])
        axes.legend()

    def draw(self):
        """
        Shows the plot and the toolbar.
        """
        self.parent.addWidget(self.canvas)
        self.parent.addWidget(self.toolbar)
        self.canvas.draw()
