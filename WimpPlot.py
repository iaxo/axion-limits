from __future__ import annotations

import numpy as np
from AxionPlot import extract_kwargs
from scipy.interpolate import interp1d
from XPlotter import BasePlot, ExPltItem


# ==============================================================================#
class WimpPlot:

    def __init__(
        self,
        experiments=[],
        labels=[],
        excludedRegion=True,
        showplot=True,
        saveplotname=None,
        figx=9,
        figy=7,
        xmin=0.1,
        xmax=20,
        ymin=1e-46,
        ymax=1e-34,
        ticksopt_x="normal",
        ticksopt_y="normal",
        labelx=r"WIMP mass [GeV/c$^{2}$]",
        labely=r"SI WIMP-nucleon cross section $\sigma_{\chi n}^\mathrm{SI}$ [cm$^{2}$]",
        **excludedRegionOptions,  # color, alpha, lw, zorder, etc.
    ):
        # plot the background
        self.baseplot = BasePlot(
            xlab=labelx,
            ylab=labely,
            figsizex=figx,
            figsizey=figy,
            y_min=ymin,
            y_max=ymax,
            x_min=xmin,
            x_max=xmax,
            ticksopt_x=ticksopt_x,
            ticksopt_y=ticksopt_y,
        )

        self.wimpDB = []
        # print(self.axionDB.get_rows())

        # Plotting Data
        print("\n")
        self.PlotData(experiments)
        if excludedRegion:
            self.PlotExcludedRegion(**excludedRegionOptions)
        print("\n")
        self.PlotLabels(labels)
        print("\n")

        if showplot:
            self.baseplot.ShowPlot()

        if type(saveplotname) == str:
            if len(saveplotname) > 0:
                self.baseplot.SavePlot(saveplotname)

    def PlotData(self, data: list):
        print("Plotting data:")
        for row in data:
            kwargs = {}
            if type(row[3]) == str:
                kwargs = extract_kwargs(row[3])
            elif type(row[3]) == dict:
                kwargs = row[3]
            pltItem = ExPltItem(
                row[0], row[1], row[2], **kwargs
            )  # row[0] = name, row[1] = type, row[2] = path, row[3] = drawOptions
            pltItem.DrawItem(self.baseplot)
            self.wimpDB.append(pltItem)

    def PlotLabels(self, labels: list):
        print("Plotting labels:")
        for label in labels:
            kwargs = {}
            if type(label[3]) == str:
                kwargs = extract_kwargs(label[3])
            elif type(label[3]) == dict:
                kwargs = label[3]
            # if "picker" not in kwargs:
            #   kwargs["picker"] = True
            print("->", label[0], label[1], label[2], kwargs)
            self.baseplot.plot.text(x=label[1], y=label[2], s=label[0], **kwargs)

    def PlotExcludedRegion(self, **kwargs):
        # if kwargs does not contain one of the following, use the default values
        if "color" not in kwargs:
            kwargs["color"] = "#aaffc3"
        if "alpha" not in kwargs:
            kwargs["alpha"] = 0.5
        if ("lw" not in kwargs) and ("linewidth" not in kwargs):
            kwargs["lw"] = 0
        if "zorder" not in kwargs:
            kwargs["zorder"] = -101

        (x_excluded, y_excluded) = self.getExcludedRegion()
        if len(y_excluded) > 0:
            print("Plotting excluded region.")
            self.baseplot.plot.fill_between(
                x_excluded,
                y_excluded,
                self.baseplot.plot.get_ylim()[1] * 10,
                **kwargs,
            )

    ## -------- CALCULATE THE EXCLUDED PARAMETER SPACE --------
    def getExcludedRegion(self):
        if len(self.wimpDB) <= 0:
            print("Error: no available data for computing excluded region.")
            return ([], [])
        if type(self.wimpDB[0]) != ExPltItem:
            print(
                "Error: the data is not in the correct format. Make sure to call first PlotData()"
            )
            return ([], [])

        xlim = self.baseplot.plot.get_xlim()
        x_val_arr = np.logspace(
            start=np.log10(xlim[0]), stop=np.log10(xlim[1]), num=1000
        )

        interp_array = []
        for item in self.wimpDB:
            if item.typeitem != "line":  # use only curves
                continue
            if (
                item.name == 1
            ):  # exclude projections # TODO CHANGE THIS TO AVOID PROJECTIONS
                continue
            interpolator = interp1d(
                item.data[:, 0], item.data[:, 1], bounds_error=False, fill_value=1e-10
            )
            interp_array.append(interpolator(np.power(x_val_arr, 1)))
        if len(interp_array) <= 0:
            print(
                "Warning: no available lines (not projection) for computing excluded region."
            )
            return (x_val_arr, [])
        exp_upper_lim = np.min(
            interp_array, axis=0
        )  # minimum value of cross section across all above included curves for each mass
        return (x_val_arr, exp_upper_lim)
