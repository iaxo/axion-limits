from AxionPlot import *
import DataBaseClass as db

plottype = "" # plottype not in AxionGagPlot.ListOfPlotTypes will be interpreted as 'wildType' in the database

# Load the desired database (the second parameter is the table name inside the database, see DataBaseClass.py for more info)
database = db.DataBaseGag("databases/Axions.db", "AxionsGag")
labels = db.DataBaseLabels("databases/Axions.db", "large_panorama")
'''
# Here you can edit the database if you want. Note that the database file will be edited too.

# For example, you can add a new row with the following command:
database.insert_row("exp_name", "line", "path_to_datafile", "color='red', linewidth=2", 1, 0, 0, 0, 0, 0, 0)
# Or change the drawOptions of a row:
database.update_row("exp_name", "drawOptions", "color='blue', linewidth=1")
# Or delete a row:
database.delete_rows("name='exp_name'", confirm=True)
'''

AxionGagPlot(database, labels, plottype,
                 projections=False,
                 showplot=True,
                 saveplotname="testingGag.png")


# Load the desired database (the second parameter is the table name inside the database, see DataBaseClass.py for more info)
database = db.DataBaseGag("databases/Axions.db", "AxionsGae")
labels = db.DataBaseLabels("databases/Axions.db", "Gae_labels")

AxionGaePlot(database, labels, "",
                 projections=True,
                 showplot=True,
                 saveplotname="testingGae.png")