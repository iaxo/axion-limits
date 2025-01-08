import axionlimits.databases as db
from axionlimits.axion_plot import AxionGagPlot

# --- LOAD THE DATABASE ---

database = db.DataBaseGag()  # the second parameter is the table name inside the database, see DataBaseClass.py for more info

# List of the names of the experiments to plot. The names must match the name column in the database
# To see the names of the experiments in the database, you can use the following command:
# print([row[0] for row in database.get_rows_where("1 ORDER BY name")])
experimentsToPlot = [
    "qcdband",
    "ksvz",
    #"CAST",
    "CAST2021",
]
exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

# --- EDIT THE ITEMS PROPERTIES ---
# If you want to edit the properties of an item you have selected from the database,
# you can do it here. For example, change the drawOptions of the element "NuFloorXe":
exps["qcdband"]["type"] = "region"
exps["qcdband"]["drawOptions"] += ", cmap=('YlOrBr', 0, 0.45, 20)"
exps["ksvz"]["drawOptions"] += ", color='#a35c2f'"
#exps["CAST2021"]["drawOptions"] += ", cmap=('Blues', 0, 1, 100)"

# --- ADD THE LABELS ---
labels = [
    (r"{\bf Helioscopes (CAST)}", 1e-8, 2e-10, dict( color="black", size=10)),
    ("KSVZ", 3e-4, 21e-14, dict( color="black", size=6, rotation=47)),
]

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    showplot=True,  # set to false to add the labels later
    #saveplotname="test.pdf",
)

