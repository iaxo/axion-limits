from __future__ import annotations

import DataBaseClass as db
import matplotlib.pyplot as plt
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
    "admx_hf_2016",
    "hess",
    "mrk421",
    "sn1987a_photon",
    "FERMI_NG1275",
    "SN1987energyloss",
    "Xray",
    "Deut2016",
    "OpticalDepthTerm",
    "gEBL1",
    "EBL2",
    "cmb_mu",  # 'CMB_DEsuE',
    "Overduin",
    "Ressell",
    "endlist2_gamma_projimprov",
    "telescopes",
    "telescopes_new",
    "HBalpbound",
    "solar_nu",
    "CAST",
    "OSCAR2015",
    "PVLAS2015",
    "BeamDump",
    # projections
    "ABRA1",
    "ABRA1_l",  # 'KLASH',
    "ADMXprosp_2GHz",
    "ADMXprosp_2GHz_l",
    "ADMXprosp_10GHz",
    "ADMXprosp_10GHz_l",
    "CAPP4_l",
    "MADMAX_l",  # 'BRASS'
    "ORGANprosp",
    "ALPSII_l",
    "BabyIAXO_l",
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
)

# --- ADD THE LABELS ---
plt.text(1e-8, 2e-10, r"{\bf Helioscopes (CAST)}", color="black", size=10)
plt.text(1e-7, 2e-7, r"{\bf Laboratory}", color="white", size=10)
plt.text(1e-9, 5e-12, r"$\gamma \textrm{-rays}$", color="black", size=10, ha="center")
# plt.text(1e-8,1e-13,'Haloscopes',color="black",size=9)
plt.text(
    5e7, 4e-8, "SN1987A", color="black", size=6, rotation=-90, ha="center", va="center"
)
plt.text(3e-4, 21e-14, "KSVZ", color="black", size=6, rotation=47)
plt.text(5, 1e-13, "Telescopes", color="black", size=6, rotation=90)
plt.text(
    2e2,
    1.6e-10,
    "Horizontal \n Branch Stars",
    color="black",
    size=7,
    va="center",
    ha="center",
)
plt.text(1e2, 2e-9, r"{\bf Sun}", color="white", size=10)
plt.text(
    1.5e7,
    5e-6,
    r"{\bf Beam dump}",
    color="white",
    size=8,
    rotation=-45,
    ha="center",
    va="center",
)
plt.text(
    1e4, 3e-17, "X rays", color="white", size=10, rotation=-57, ha="center", va="center"
)
# plt.text(1e5,1e-14,r'{\bf EBL}',color="black",size=10,rotation=-57,ha='center',va='center')
plt.text(
    1e5,
    1e-14,
    "Extra-galactic \n Background Light",
    color="black",
    size=9,
    rotation=-57,
    ha="center",
    va="center",
)
plt.text(
    2e8,
    1e-14,
    r"{\bf CMB}",
    color="white",
    size=9,
    rotation=-57,
    ha="center",
    va="center",
)
plt.text(
    3e7,
    1e-10,
    "Big-Bang \n Nucleosynthesis",
    color="black",
    size=10,
    rotation=-57,
    ha="center",
    va="center",
)
plt.text(
    1e2,
    1e-13,
    "H$_2$ ionization \n fraction",
    color="black",
    size=8,
    ha="center",
    va="center",
    rotation=90,
)

# added for Gaia's plot
plt.text(
    2.9e-6, 3e-13, "ADMX", color="black", size=6, ha="center", va="center", rotation=90
)
plt.text(
    8.3e-6,
    3.5e-12,
    "BNL\n+UF",
    color="black",
    size=5,
    ha="center",
    va="center",
    rotation=90,
)
plt.text(
    1.3e-5,
    2.5e-14,
    "HAYSTAC",
    color="black",
    size=4,
    ha="center",
    va="center",
    rotation=90,
)
# plt.text(1.1e-5,2.5e-14,'KLASH',color="black",size=5,ha='center',va='center',rotation=90)


plt.text(1e-3, 3e-11, r"{ BabyIAXO}", color="black", size=8, ha="center", va="center")
plt.text(1e-3, 5e-12, r"{ IAXO}", color="black", size=8, ha="center", va="center")
plt.text(1e-6, 3e-11, r"{ ALPS-II}", color="black", size=8, ha="center", va="center")
# plt.text(1e-6,5e-12,r'{\bf JURA}',color="black",size=8,ha='center',va='center')

# added for Gaia's plot
plt.text(
    8e-6,
    2e-16,
    "ADMX+CAPP",
    color="black",
    size=5,
    ha="center",
    va="center",
    rotation=47,
)
plt.text(
    2e-4, 8e-15, "MADMAX", color="black", size=5, ha="center", va="center", rotation=47
)
plt.text(
    1.2e-4, 6e-13, "ORGAN", color="black", size=5, ha="center", va="center", rotation=90
)
plt.text(7e-9, 4e-15, '"DM-\n Radios"', color="black", size=6, ha="center", va="center")

# --- SHOW AND SAVE THE PLOT ---
axionplot.baseplot.ShowPlot()
axionplot.baseplot.SavePlot("testing.pdf")
