from __future__ import annotations

from XPlotter import BasePlot, ExPltItem


def extract_kwargs(arguments_str):
    """Extracts kwargs from a string of arguments.
    Example: extract_kwargs("a=1, b=2, c=3") returns {'a':1, 'b':2, 'c':3}
             extract_kwargs("a=1, b="red", c=3,") returns {'a':1, 'b':'red', 'c':3}"""
    kwargs = {}
    for arg in arguments_str.split(","):
        if arg.strip() != "":
            key, value = arg.split("=")
            kwargs[key.strip()] = eval(value.strip())
    return kwargs


# ==============================================================================#
# renormalize data, to plot C_ag instead of g_ag
#
def RenormItem(item: ExPltItem):
    for i in range(len(item.data)):
        # print(item.name)
        item.data[i, 1] = item.data[i, 1] / item.data[i, 0] * 5.172e9
        # print(item.data[i,0],item.data[i,1])
        # C_ag = g_ag / m_a * 5.172e9


class AxionGagPlot:
    def __init__(
        self,
        experiments=[],
        labels=[],
        plotCag=False,
        showplot=True,
        saveplotname=None,
        figx=6.5,
        figy=5,
        xmin=1e-11,
        xmax=1e9,
        ymin=1e-18,
        ymax=1e-4,
        ticksopt_x="dense",
        ticksopt_y="normal",
        labelx="$m_a$ (eV)",
        labely=r"$|g_{a\gamma}|$ (GeV$^{-1}$)",
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

        self.axionDB = []
        self.plotCag = plotCag
        # print(self.axionDB.get_rows())

        # Plotting Data
        print("\n")
        self.PlotData(experiments)
        print("\n")
        self.PlotLabels(labels)
        print("\n")

        if showplot:
            self.baseplot.ShowPlot()

        if type(saveplotname) == str:
            if len(saveplotname) > 0:
                self.baseplot.SavePlot(saveplotname)

    def PlotData(self, data):
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
            if self.plotCag:
                RenormItem(pltItem)
            pltItem.DrawItem(self.baseplot)
            self.axionDB.append(pltItem)

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


"""
class AxionGaePlot:
    ListOfPlotTypes = {}  # No plottypes for Gae yet

    def __init__(
        self,
        database: db.DataBaseGae,
        labels: db.DataBaseLabels,
        plottype="",
        projections=False,
        showplot=True,
        saveplotname=None,
        figx=6,
        figy=5,
        xmin=1.0e-4,
        xmax=1.0,
        ymin=1.0e-13,
        ymax=1.0e-10,
        labelfontsize=13,
        labelx="$m_a$ (eV)",
        labely=r"$|g_{ae}g_{a\gamma}|^{1/2}$ (GeV$^{-1/2}$)",
    ):
        self.baseplot = BasePlot(
            xlab=labelx,
            ylab=labely,
            figsizex=figx,
            figsizey=figy,
            y_min=ymin,
            y_max=ymax,
            x_min=xmin,
            x_max=xmax,
            labelfontsize=labelfontsize,
        )

        self.axionDB = database
        self.labelsDB = labels
        # print(self.axionDB.get_rows())

        self.PlotData(plottype, projections)
        self.PlotLabels(projections)
        if showplot:
            self.baseplot.ShowPlot()

        if type(saveplotname) == str:
            if len(saveplotname) > 0:
                print("saving...")
                self.baseplot.SavePlot(saveplotname)
                print("done")

    def PlotData(self, plottype, projections=False):
        print("projections = ", projections)
        if plottype not in self.ListOfPlotTypes:
            plottype = "wildType"

        data = self.axionDB.get_rows(f"{plottype}==1")
        if projections:
            data = data + self.axionDB.get_rows(
                f"projection==1 AND {plottype}==0"
            )  # get projections not already included
        for row in data:
            pltItem = ExPltItem(row[0], row[1], row[2], **extract_kwargs(row[3]))
            pltItem.DrawItem(self.baseplot)

    def PlotLabels(self, projections=False):
        labels = self.labelsDB.get_rows(f"onoff==1 AND projection==0")
        if projections:
            labels = labels + self.labelsDB.get_rows(f"onoff==1 AND projection==1")

        for row in labels:
            plt.text(row[1], row[2], row[0], **extract_kwargs(row[3]))
"""
