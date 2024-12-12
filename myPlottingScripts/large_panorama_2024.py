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
    "CAST2021",
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

labels = [
    (r"{\bf Helioscopes (CAST)}", 1e-8, 2e-10, dict( color="black", size=10)),
    (r"{\bf Laboratory}", 1e-7, 2e-7, dict( color="white", size=10)),
    (r"$\gamma \textrm{-rays}$", 1e-9, 5e-12, dict( color="black", size=10, ha="center")),
    ("SN1987A", 5e7, 4e-8, dict( color="black", size=6, rotation=-90, ha="center", va="center")),
    ("KSVZ", 3e-4, 21e-14, dict( color="black", size=6, rotation=47)),
    ("Telescopes", 5, 1e-13, dict( color="black", size=6, rotation=90)),
    ("Horizontal \n Branch Stars", 2e2, 1.6e-10, dict( color="black", size=7, va="center", ha="center")),
    (r"{\bf Sun}", 1e2, 2e-9, dict( color="white", size=10)),
    (r"{\bf Beam dump}", 1.5e7, 5e-6, dict( color="white", size=8, rotation=-45, ha="center", va="center")),
    ("X rays", 1e4, 3e-17, dict( color="white", size=10, rotation=-57, ha="center", va="center")),
    ("Extra-galactic \n Background Light", 1e5, 1e-14, dict( color="black", size=9, rotation=-57, ha="center", va="center")),
    (r"{\bf CMB}", 2e8, 1e-14, dict( color="white", size=9, rotation=-57, ha="center", va="center")),
    ("Big-Bang \n Nucleosynthesis", 3e7, 1e-10, dict( color="black", size=10, rotation=-57, ha="center", va="center")),
    ("H$_2$ ionization \n fraction", 1e2, 1e-13, dict( color="black", size=8, ha="center", va="center", rotation=90)),
    ("ADMX", 2.9e-6, 3e-13, dict( color="black", size=6, ha="center", va="center", rotation=90)),
    ("BNL\n+UF", 8.3e-6, 3.5e-12, dict( color="black", size=5, ha="center", va="center", rotation=90)),
    ("HAYSTAC", 1.3e-5, 2.5e-14, dict( color="black", size=4, ha="center", va="center", rotation=90)),
    (r"{ BabyIAXO}", 1e-3, 3e-11, dict( color="black", size=8, ha="center", va="center")),
    (r"{ IAXO}", 1e-3, 5e-12, dict( color="black", size=8, ha="center", va="center")),
    (r"{ ALPS-II}", 1e-6, 3e-11, dict( color="black", size=8, ha="center", va="center")),
    ("ADMX+CAPP", 8e-6, 2e-16, dict( color="black", size=5, ha="center", va="center", rotation=47)),
    ("MADMAX", 2e-4, 8e-15, dict( color="black", size=5, ha="center", va="center", rotation=47)),
    ("ORGAN", 1.2e-4, 6e-13, dict( color="black", size=5, ha="center", va="center", rotation=90)),
    ('"DM-\n Radios"', 7e-9, 4e-15, dict( color="black", size=6, ha="center", va="center")),
]

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    showplot=True,  # set to false to add the labels later
    saveplotname="large_panorama_2024.pdf",
)
