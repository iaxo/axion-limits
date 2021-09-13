from axionPlot import  AxionGagPlot, AxionGaePlot
#from wimpPlot import WimpPlot

ListOfPlotTypes = {'large_panorama', 'panorama','LSWexps','haloscopes','haloscopes_zoom','helioscopes'}


axplot = AxionGagPlot('haloscopes_radeszoom',
    projections=False,
    showplot=True,
    saveplot=True)

# axplot = AxionGaePlot('helioscopes',
#     projections=True,
#     showplot=True,
#     saveplot=True)


# wimpplot = WimpPlot('lowmass',
#     projections=True,
#     showplot=True,
#     saveplot=True)
