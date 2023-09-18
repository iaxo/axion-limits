from AxionPlot import AxionGagPlottest


for plot_type in AxionGagPlottest.ListOfPlotTypes:
    AxionGagPlottest(plot_type,
                 projections=False,
                 showplot=False,
                 saveplot=True)

