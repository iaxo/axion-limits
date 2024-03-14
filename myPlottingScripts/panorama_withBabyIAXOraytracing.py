from __future__ import annotations

import myPath  # add the path to the project
import DataBaseClass as db
from AxionPlot import *

# --- LOAD THE DATABASE ---

database = db.DataBaseGag(
    "databases/Axions.db", "AxionsGag"
)  # the second parameter is the table name inside the database, see DataBaseClass.py for more info

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
    "admx_hf_2016",
    "ADMX2018",
    "ADMX2019",
    "ADMX2021",
    "ADMX_sidecar",
    "CAPP-8TB",
    "CAPP2021",
    "HAYSTAC",
    "HAYSTAC2020",
    "ORGAN",
    "QUAX",
    "QUAX2021",
    "old_haloscopes",
    "admx",
    "RADES2021",
    "ADMX_SLIC",
    "hess",
    "mrk421",
    "sn1987a_photon",
    "FERMI_NG1275",
    "endlist2_gamma_projimprov",
    "telescopes",
    "telescopes_new",
    #"HBalpbound_l", # bug in the database, data file was moved to data/axion/cosmoalp folder
    "solar_nu",
    "CAST",


    # projections
    "ABRA1",
    "KLASH",
    "IAXODM",
    "ORGANprosp",
    "castcapp2",
    "CAPP4",
    "ADMXprosp_2GHz",
    "ADMXprosp_10GHz",
    "MADMAX",
    "ADMXprosp_2GHz_l",
    "ADMXprosp_10GHz_l",
    "MADMAX_l",
    "ALPSII_l",
    "BabyIAXO",
    "IAXO",
    "IAXOplus",
    "BabyIAXO_l",
    "IAXO_l",
    "IAXOplus_l",
    "BabyIAXO_raytracing_l",
]
exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

labels = [
    (r"{\bf Helioscopes (CAST)}", 1e-5, 2e-10, dict( color="black", size=11)),
    (r"{\bf Laboratory}", 1e-7, 2e-7, dict( color="white", size=11)),
    (r"HE $\gamma \textrm{-rays}$", 2e-9, 6e-12, dict( color="black", size=10)),
    (r"{\bf Haloscopes}", 5e-6, 1e-13, dict( color="black", size=11, ha="center")),
    ("KSVZ", 3e-4, 2e-13, dict( color="green", size=9, rotation=40)),
    # ('Axion models', 0.5e-3, 4e-14, dict(color="black",size=9,rotation=40)),
    ("DSFZ", 0.5e-3, 1e-13, dict( color="green", size=9, rotation=40)),
    ("Telescopes", 5, 3e-13, dict( color="black", size=8, rotation=90)),
    #("HB", 1, 0.9e-10, dict( color="black", size=9)), # bug in the database, data file was moved to data/axion/cosmoalp folder
    ("Sun", 3, 1.3e-9, dict( color="black", size=9, ha="center")),
    # (r'{\bf Sun}', 1e2, 2e-9, dict(color="white",size=10)),

    # projections
    (r"BabyIAXO", 2e-3, 2.5e-11, dict( color="black", size=10, ha="center", va="center",)),
    (r"{\bf IAXO}", 2e-3, 7e-12, dict( color="black", size=11, ha="center", va="center",)),
    # (r'{\bf IAXO+}', 1e-5, 1e-12, dict(color="black",size=9,ha='center',va='center')),
    (r"{\bf ALPS-II}", 5e-7, 3e-11, dict( color="black", size=10, ha="center", va="center",)),
    # (r'{\bf JURA}', 5e-7, 1.5e-12, dict(color="black",size=9,ha='center',va='center')),
    (r"BabyIAXO ray tracing", 0.00267177, 1.05635e-12, dict( color="black", size=10, ha="center", va="center",)),
]

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    showplot=True,  # set to false to add the labels later
    saveplotname="panorama_withBabyIAXOraytracing",
    figx = 6.5,
    figy = 6,
    ymin = 1e-17,
    ymax = 1e-6,
    xmin = 1e-9,
    xmax = 10,
    ticksopt_x = "normal",
    ticksopt_y = "normal",
)

