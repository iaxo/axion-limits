# IAXO axion-limits
Project to generate the sensitivity plots of different experiments of dark matter searches. For now, it includes axion (coupling to photon and electrons) and WIMPs (spin independent interaction only) experiments although its called 'axion-limits'.

Some examples of this generated plots can be found in the plots folder.

In the case of axions:

![large_panorama](plots/large_panorama.pdf)

In the case of WIMPs:

![large_panorama](plots/WIMPs_SI.pdf)

## Getting Started
The files generateAxionPlot.py and generateWimpPlot.py are given as examples on how to generate this sensitivity plots. You can do this by executing any of this scripts (let´s take the axion case)

```
python3 generateAxionPlot.py
```

Inside this script you can find how to use this package. The different dark matter detection experiment are organize in SQL databases. For now, we have one database for [axion](databases/Axions.db) experiments (which contains one table named AxionsGag for photon coupling and another one called AxionGae for electron coupling) and for [WIMPs](databases/Wimps.db) experiments (which contains one table named WIMPs_SI for spin independent interaction). In order to load the desired database you may use the correspondent DataBase class defined in [DataBaseClass.py](DataBaseClass.py). In this case,

```
import DataBaseClass as db

# The first parameter is the path to the .db file and second parameter is the name of the database table inside that .db file.
database = db.DataBaseGag("databases/Axions.db", "AxionsGag")
```
Then, write a list with the experiments name (matching the name column of the database) you want to include in the plot.
```
experimentsToPlot = [
    "qcdband",
    "ksvz",
    "CAST",
]
```
Now, extract this rows from the database as follows:
```
exps = database.get_rows("name", experimentsToPlot)
```
You may now include some labels. In order to do that, you could build a list where each element will be a label to plot. Each os these elements (labels) should be a tuple (or list) containing at least a string with the text of the label (LaTeX formatting is available), the x position and y position. Optionally a 4th element can be given containing a dictionary with the matplotlib.pyplot.text() keyword arguments to customize the text label as you want. For example,
```
labels = [
    (r"{\bf Helioscopes (CAST)}", 1e-8, 2e-10, dict(color="black", size=10)),
    ("KSVZ", 3e-4, 21e-14, dict( color="black", size=6, rotation=47)),
]
```
Finally, call the AxionPlot constructor to generate the plot.
```
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    showplot=True,  # set to false to add the labels later
    saveplotname="test.pdf",
)
```
Use the parameter `experiments` and `labels` to pass the previously defined data and labels. If a string is given to the `saveplotname`, it will save the plot in a file with that name (default extension will be pdf if none is given within the filename). You can check other useful customization arguments at [AxionPlot.py](AxionPlot.py).

### More complex examples
Inside [myPlottingScripts](myPlottingScripts) folder you can find real examples of scripts used to generate the figure inside [plots](plots) folder.

To be able to reproduce them (without moving them to the parent directory), first go to [myPath](myPlottingScripts/myPath.py) file and change the variable PATH_TO_PROJECT with the absolute path of the repository in your local system. This is needed to be able to load the modules defined in the parent directory of this project (TODO: wrap all this code into a proper python package). Now you can run any of those scripts, such as

```
python3 myPlottingScripts/haloscopes.py
```

You can add in this folder any meaningful plotting script used to make a plot you may want to reproduce in the future. If you do so, remember to add
`import myPath` at the beginning of the script.

## Project contents
### Files description
The main files where the code is written are

1. XPlotter.py : the matplotlib.pyplot objects creation and configuration are
   handled within the two classes (BasePlot and ExPltItem) defined in this file
2. AxionPlot.py : the creation of the BasePlot for the two cases (AxionGagPlot
   and AxionGaePlot), the plotting of the data and labels are handled within
   this classes.
3. WimpPlot.py : the creation of the BasePlot, the plotting of the data and labels are handled within this class.
4. DataBaseClass.py : Here the DataBase classes are defined to interface with
   the SQLite .db files. It has the following classes:
   - DataBase : is not intended to be used, just serve to be inherited by the
     other classes.
   - DataBaseGag for the database table of AxionGag experiments.
   - DataBaseGae for the database table of AxionGae experiments.
   - DataBaseWimps for the database table of WIMps experiments.
   - DataBaseLabels for the database table of labels (to be deprecated...).

All these files are not intended to be modified by the user.

The files that are meant to be modified and used by the user are the following:

1. buildDataBase.py : this is an example of the building of the database .db
   files. It also serves as backup to be able to recreate the Axions.db in case
   this one is lost or edited unintentionally.
2. generateAxionPlot.py : this is the main file to be handled by the user to
   make the desired plot. Here load (and edit if you want) the database tables
   and call the corresponding AxionPlot constructor to make the plot.
3. generateWimpPlot.py : same for WIMPs.
### Subdirectories description

1. Javat : all needed files (html and java) for the labels app.
2. data : here the .txt or .dat files with the exclusion lines of the different
   experiments should be stored.
3. databases : here the .db files with the databases of the experiments data and
   labels should be stored. Include here any new database you build to make a
   new plot you may want to reproduce in the future.
4. plots : here the saved plots should be stored. The relative path to this
   directory is added automatically to the plotname specified by the user.
5. myPlottingScripts : this folder is meant to serve as the warehouse of the
   scripts used to generate a plot you may want to reproduce in the future. Here
   you can found some examples as large_panorama.py, panorama.py,
   helioscopes.py, haloscopes.py and lsw.py. As a quick solution to be able to
   import the modules from the parent directory, the file myPath.py is used.
   Please, set the variable PATH_TO_PROJECT with the absolute path of the
   repository in your local system (to be improved soon).

## Handling the databases
The different dark matter detection experiment are organize in SQL databases. For now, we have one database for [axion](databases/Axions.db) experiments (which contains one table named AxionsGag for photon coupling and another one called AxionGae for electron coupling) and for [WIMPs](databases/Wimps.db) experiments (which contains one table named WIMPs_SI for spin independent interaction). In order to load the desired database you may use the correspondent DataBase class defined in [DataBaseClass.py](DataBaseClass.py).
### Loading a database

To load the desired database use the constructor of the classes DataBaseGag (for
AxionGag experiments), DataBaseGae (for AxionGae experiments) or DataBaseWimps as follows:

```
import DataBaseClass as db

# Load the desired database. The first parameter is the path to the .db file and second parameter is the name of the database table inside that .db file.
database = db.DataBaseGag("databases/Axions.db", "AxionsGag") # load table AxionsGag of Gag experiments from the database file databases/Axions.db
```

Once loaded, you can edit the database if you want. By default, the database
file will not be edited. To commit the changes to the db file, set parameter
commit=True at the constructor or use the DataBase.set_commit(True) method. For
example, you can add a new row with the following command:

```
database.set_commit(True) # to commit the changes to the .db file
database.insert_row("exp_name", "line", "path_to_datafile", "color='red', linewidth=2", 1, 0, 0, 0, 0, 0, 0)
database.set_commit(False) # go back to default mode (not committing changes to the .db file)
```

Or change the drawOptions of a row:

```
database.update_row("exp_name", "drawOptions", "color='blue', linewidth=1")
```

Or delete a row:

```
database.delete_rows("name='exp_name'") # set parameter confirm=True to avoid the security check
```

### Creating a new database

To create a new database for a new plot you may follow this examples. Keep in
mind that the order in which the experiments are added to the database will be
the order in which they are plotted, so the last experiments added will be drawn
o top of the firsts experiments added to the database. Note the parameter
commit=True at the constructor of the databases to commit the changes to the db
file. For a Gag exclusion plot:

```
import DataBaseClass as db
database = db.DataBaseGag("databases/NewAxions.db", commit=True) # this will create (if it doesn't already exists) a table named AxionsGag (default) at databases/NewAxions.db
AxionsGag = [
    ['qcdband', 'band', PATH_DATA + 'QCD_band.dat', "facecolor='yellow'", 1, 0, 0, 0, 0, 0, 0],
    ['old_haloscopes', 'band', PATH_DATA + 'MicrowaveCavities.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 0, 0, 0, 0, 0, 0],
    ['ABRA3', 'line', PATH_DATA + 'ABRAres_3.dat', "color='green', linewidth=0.1, linestyle='-'", 1, 0, 0, 0, 0, 0, 0],
    ['ADMX2018', 'band', PATH_DATA + 'ADMX2018.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 0, 0, 0, 0, 0, 0],
    ['BabyIAXO', 'band', PATH_DATA + 'miniIAXO.dat', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, 0, 0, 0, 0, 0, 0],
    ['IAXO', 'band', PATH_DATA + 'IAXO_nominal.txt', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, 0, 0, 0, 0, 0, 0],
    ['CAST', 'band', PATH_DATA + 'cast_env_2016.dat', "facecolor='deepskyblue', edgecolor='blue', linewidth=0.5", 1, 0, 0, 0, 0, 0, 0],
]
database.insert_rows(AxionsGag)
data = database.read_rows()
print(data)
```

For a Gae exclusion plot:

```
import DataBaseClass as db
database = db.DataBaseGae("databases/NewAxions.db", commit=True)  # this will create (if it doesn't already exists) a table named AxionsGae (default) at databases/NewAxions.db
AxionsGae= [
    ["DFSZ1_starhint", "region", path1 + "DFSZ1_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='springgreen', edgecolor='darkgreen', alpha=0.2", 1, 0],
    ["AJ83_starhint", "region", path1 + "AJ83_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='red', edgecolor='red', alpha=0.2", 1, 0],
    ["QCDband", "band", path2 + "DFSZband_gaegag.dat", "facecolor='lemonchiffon', edgecolor='none', linewidth=1", 1, 0],
    ["CAST_gae", "band", path2 + "CAST_gae_gagg.dat", "facecolor='steelblue', edgecolor='darkblue', linewidth=0.5", 1, 0],

    ["IAXO_gae", "band", path2 + "sqrtgaagae_sc2.dat", "facecolor='skyblue', edgecolor='black', linewidth=0.5, alpha=0.3", 0, 1],
    ["IAXOplus_gae", "band", path2 + "sqrtgaagae_sc3.dat", "facecolor='skyblue', edgecolor='black', linewidth=0.5, alpha=0.3", 0, 1],
]
database.insert_rows(AxionsGae)
data = database.read_rows()
print(data)
```

## Labels web app

To quickly add new labels to the plots in a easy way (although this would not be
saved anywhere to be reproduced) you may use the labels app programmed in the
Javat directory. Or just click on the following link:
[Label's APP](https://danielmartinezmiravete.github.io/Labels-App/)

You can start the app by opening the HTML script called 'index.html'. This
application is only capable of modifying SVG files. Instructions for the webpage
are provided within the webpage itself.

As additional information, to interact with the database, you need to use
different functions implemented in the script called 'DataBaseGag.py'. This
repository contains Python scripts for interacting with the AxionsGag database.
The database is used to manage information about various experiments related to
axion research. Below, you'll find instructions on how to use the provided
functions to work with the database.

## Known Issues

- The labels application cannot interpret LaTeX.
- At labels application, when working with multiple labels, moving a label other
  than the last label will replace the coordinates of the last label written.

## Acknowledgement

The original code is https://github.com/iaxo/axion-limits/

Modified by Daniel Martínez Miravete in his summer internship
(https://github.com/DanielMartinezMiravete/Axion_Limits_Memory) for the Physics
Bachelor within the IAXO group of GIFNA (Unizar). Internship supervised by Juan
Antonio García Pascual and Álvaro Ezquerro Sastre. Also, very helpful insight
was given by David Díez Ibáñez and Luis Obis Aparicio.
