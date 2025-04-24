import axionlimits.databases as db
from axionlimits.axion_plot import AxionGagPlot

# --- LOAD THE DATABASE ---

database = db.DataBaseGag()
"""
# Here you can edit the database if you want.
# For example, change the drawOptions of a row:
database.update_row("exp_name", "drawOptions", "color='blue', linewidth=1")
# Or delete a row:
database.delete_rows("name='exp_name'", confirm=True)
"""


# List of the names of the experiments to plot. The names must match the name column in the database
# To see the names of the experiments in the database, you can use the following command:
# print([row[0] for row in database.get_rows_where("1 ORDER BY name")])


experimentsToPlot = [
    "qcdband",
    "ksvz",
    "dfsz",

    "CombinedAstro2024",

    "admx_hf_2016",
    "ADMX2018",
    "ADMX2019",
    "ADMX2021",
    "ADMX_sidecar",
    "CAPP-8TB",
    "HAYSTAC",
    "HAYSTAC2020",
    "ORGAN",
    "QUAX",
    "QUAX2021",
    "RADES2021",
    "ADMX_SLIC",
    "old_haloscopes",
    "admx",
    "CAST2021",

    #"SHAFT", "ABRA_2021", 
    "BASE_2021",
    "OSCAR2015", "PVLAS2015", "ALPSI",

    # projections
    "ALPSII_l",
    "BabyIAXO",
    "IAXO",
    "IAXOplus",
    "BabyIAXO_l",
    "IAXO_l",
    "IAXOplus_l"
]

exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

# style
exps["CombinedAstro2024"]["drawOptions"] = "facecolor='mediumturquoise', edgecolor='darkgreen', linewidth=0.5, alpha=0.8"
exps["CAST2021"]["drawOptions"] = "facecolor='deepskyblue', edgecolor='blue', linewidth=0.5"
exps["ALPSII_l"]["drawOptions"] = "color='black', linewidth=0.8, linestyle='-'"
exps["BabyIAXO_l"]["drawOptions"] = "color='black', linewidth=0.8, linestyle='-'"
exps["IAXO_l"]["drawOptions"] = "color='black', linewidth=0.8, linestyle='--'"
exps["IAXOplus_l"]["drawOptions"] = "color='black', linewidth=0.8, linestyle='--'"

labels=[
    (r"{\bf CAST}", 2e-8, 8.6e-11, dict(color="blue", size=16,picker=True)),
    (r'{\bf Laboratory}', 1e-7, 2e-7, dict(color="white",size=12,picker=True)),
    (r"{Astrophysical bounds}", 2.4e-10, 6.8e-12, dict(color="black",size=14,ha="left",picker=True)),
    (r"{\bf Haloscopes}", 5.4e-6, 1e-12, dict(color="black", size=14,ha="center",picker=True)),
    ("KSVZ", 1.15e-3, 0.75e-12, dict( color="green", size=11, rotation=57,picker=True)),
    ("DSFZ", 4.7e-3, 5e-13, dict( color="green", size=11, rotation=57,picker=True)),

    #projections
    (r"{\bf BabyIAXO}", 0.00113, 2e-11, dict(color="black", size=12,ha="center", va="center",picker=True)),
    (r"{\bf IAXO}", 0.000544, 5.8e-12, dict(color="black", size=13,ha="center", va="center",picker=True)),
    (r"{\bf IAXO+}", 0.000544, 3.2e-12, dict(color="black", size=10, ha="center", va="center",picker=True)),
    (r"{ ALPS II}", 1.6e-6, 2.7e-11, dict(color="black", size=12, picker=True)),
]

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    showplot=True,  # set to false to add the labels later
    saveplotname="helioscopes_combinedAstro_2024.pdf",
    figx = 8,
    figy = 6,
    ymin = 1e-13,
    ymax = 1e-8,
    xmin = 1e-11,
    xmax = 1,
    ticksopt_x = "normal",
    ticksopt_y = "normal",
)