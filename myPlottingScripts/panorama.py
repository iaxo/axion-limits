from __future__ import annotations

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
    "HBalpbound_l",
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
]
exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    showplot=False,  # set to false to add the labels later
    figx=6.5,
    figy=6,
    ymin=1e-17,
    ymax=1e-6,
    xmin=1e-9,
    xmax=10,
    ticksopt_x="normal",
    ticksopt_y="normal",
)

# --- ADD THE LABELS ---
plt.text(1e-5, 2e-10, r"{\bf Helioscopes (CAST)}", color="black", size=11)
plt.text(1e-7, 2e-7, r"{\bf Laboratory}", color="white", size=11)
plt.text(2e-9, 6e-12, r"HE $\gamma \textrm{-rays}$", color="black", size=10)
plt.text(5e-6, 1e-13, r"{\bf Haloscopes}", color="black", size=11, ha="center")
plt.text(3e-4, 2e-13, "KSVZ", color="green", size=9, rotation=40)
# plt.text(0.5e-3,4e-14,'Axion models',color="black",size=9,rotation=40)
plt.text(0.5e-3, 1e-13, "DSFZ", color="green", size=9, rotation=40)
plt.text(5, 3e-13, "Telescopes", color="black", size=8, rotation=90)
plt.text(1, 0.9e-10, "HB", color="black", size=9)
plt.text(3, 1.3e-9, "Sun", color="black", size=9, ha="center")
# plt.text(1e2,2e-9,r'{\bf Sun}',color="white",size=10)

# projections
plt.text(
    2e-3,
    2.5e-11,
    r"BabyIAXO",
    color="black",
    size=10,
    ha="center",
    va="center",
)
plt.text(
    2e-3,
    7e-12,
    r"{\bf IAXO}",
    color="black",
    size=11,
    ha="center",
    va="center",
)
# plt.text(1e-5,1e-12,r'{\bf IAXO+}',color="black",size=9,ha='center',va='center')
plt.text(
    5e-7,
    3e-11,
    r"{\bf ALPS-II}",
    color="black",
    size=10,
    ha="center",
    va="center",
)
# plt.text(5e-7,1.5e-12,r'{\bf JURA}',color="black",size=9,ha='center',va='center')

# --- SHOW AND SAVE THE PLOT ---
axionplot.baseplot.ShowPlot()
axionplot.baseplot.SavePlot("panorama.pdf")
