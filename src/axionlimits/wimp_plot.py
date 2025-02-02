from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d
from .x_plotter import BasePlot, ExPltItem
from .utils import extract_kwargs, custom_formatter


# ==============================================================================#
class WimpPlot(BasePlot):

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
        tickformatter_x=custom_formatter,
        tickformatter_y=custom_formatter,
        labelx=r"WIMP mass [GeV/c$^{2}$]",
        labely=r"SI WIMP-nucleon cross section $\sigma_{\chi n}^\mathrm{SI}$ [cm$^{2}$]",
        labelfontsize=14,
        **excludedRegionOptions,  # color, alpha, lw, zorder, etc.
    ):
        # plot the background
        super().__init__(
            saveplotname=saveplotname,
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
            labelfontsize=labelfontsize,
            tickformatter_x=tickformatter_x,
            tickformatter_y=tickformatter_y,
        )

        self.data_to_plot = []
        # print(self.axionDB.get_rows())

        # Plotting Data
        print("\n")
        self.plot_data(experiments)
        if excludedRegion:
            self.plot_excluded_region(**excludedRegionOptions)
        print("\n")
        self.plot_labels(labels)
        print("\n")

        if showplot:
            self.show_plot()

        if type(saveplotname) == str:
            if len(saveplotname) > 0:
                self.save_plot(self.saveplotname)

    def plot_data(self, data: list):
        print("Plotting data:")
        for name, info in data.items():
            kwargs = {}
            draw_options = info.get("drawOptions", {})
            if type(draw_options) == str:
                kwargs = extract_kwargs(draw_options)
            elif type(draw_options) == dict:
                kwargs = draw_options

            if "projection" in kwargs:
                is_projection = kwargs["projection"]  # not use for excluding region
                del kwargs["projection"]
            else:
                is_projection = info.get("projection", False)

            if is_projection:
                # use '--' as default linestyle for projections
                if ("linestyle" not in kwargs) and ("ls" not in kwargs):
                    kwargs["ls"] = "--"

            pltItem = ExPltItem(
                name,
                info.get('type', ''),
                info.get('path', ''),
                **kwargs
            )
            pltItem.draw_item(self)
            if not is_projection:
                self.data_to_plot.append(pltItem)

    def plot_excluded_region(self, **kwargs):
        # if kwargs does not contain one of the following, use the default values
        if "color" not in kwargs:
            kwargs["color"] = "#aaffc3"
        if "alpha" not in kwargs:
            kwargs["alpha"] = 0.5
        if ("lw" not in kwargs) and ("linewidth" not in kwargs):
            kwargs["lw"] = 0
        if "zorder" not in kwargs:
            kwargs["zorder"] = -101

        (x_excluded, y_excluded) = self.get_excluded_region()
        if len(y_excluded) > 0:
            print("Plotting excluded region.")
            self.plot.fill_between(
                x_excluded,
                y_excluded,
                self.plot.get_ylim()[1] * 10,
                **kwargs,
            )

    ## -------- CALCULATE THE EXCLUDED PARAMETER SPACE --------
    def get_excluded_region(self):
        if len(self.data_to_plot) <= 0:
            print("Error: no available data for computing the excluded region.")
            return ([], [])

        xlim = self.plot.get_xlim()
        x_val_arr = np.logspace(
            start=np.log10(xlim[0]), stop=np.log10(xlim[1]), num=1000
        )

        interp_array = []
        for item in self.data_to_plot:
            if item.typeitem != "line":  # use only curves
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
        )  # minimum value of all curves for each mass
        return (x_val_arr, exp_upper_lim)
