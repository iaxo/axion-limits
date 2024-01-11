# iaxo-axion-limits
IAXO Axion Limits

The purpose of this website is to document a summer internship at the University of Zaragoza in the field of nuclear and particle physics, specifically within the axions group. During the internship, improvements were made to the code for plotting experiments, and an interactive application was created to label the graphs.

The graphs presented here are the results of the code, featuring the Axion Photon Coupling without its projections.

**Creator: Daniel Martinez Miravete**
**Modified: Alvaro Ezquerro**

# Files description
The main files where the code is written are
1. XPlotter.py : the matplotlib.pyplot objects creation and configuration are handled within the two classes (BasePlot and ExPltItem) defined in this file
2. AxionPlot.py : the creation of the BasePlot for the two cases (AxionGagPlot and AxionGaePlot), the plotting of the data and labels are handled within this classes. The plotting of the data and labes is done through the DataBase classes defined in the following file.
3. DataBaseClass.py : Here the DataBase classes are defined to interface with the SQLite .db files. It has the following classes:
   - DataBase : is not intended to be used, just serve to be inherited by the other classes.
   - DataBaseGag for the database table of AxionGag experiments.
   - DataBaseGae for the database table of AxionGae experiments.
   - DataBaseLabels for the database table of labels (for both AxionGag and AxionGae plots).
This files are not intended to be modified by the user.

The files that are meant to be modified and used by the user are the following:
1. buildDataBase.py : this is an example of the building of the database .db files. It also serves as backup to be able to recreate the Axions.db in case this one is lost or edited unintentionally.
2. example.py : this is the main file to be handled by the user to make the desired plot. Here load (and edit if you want) the database tables and call the corresponding AxionPlot constructor to make the plot.

# Directorys description
TBD

# Basic Plot
---
[<img align="right" height="250" src="Javatrain/plots/Labeled/AxionPhoton_large_panorama.svg">](https://github.com/DanielMartinezMiravete/Axion-limts/blob/main/Javatrain/plots/Labeled/AxionPhoton_large_panorama.svg)

## Basic plot without proyections

### [Download (.pdf)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_large_panoramalabeled.pdf)
### [Download (.png)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_large_panorama.png)
### [Download (.svg)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_large_panorama.svg)

### &nbsp;

# Close up General Plot
---
[<img align="right" height="250" src="Javatrain/plots/Labeled/AxionPhoton_panorama.svg">](https://github.com/DanielMartinezMiravete/Axion-limts/blob/main/Javatrain/plots/Labeled/AxionPhoton_panorama.svg)

## Close up General plot without proyections

### [Download (.pdf)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_panoramalabeled.pdf)
### [Download (.png)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_panorama.png)
### [Download (.svg)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_panorama.svg)

### &nbsp;

# Close up Helioscopes Plot
---
[<img align="right" height="250" src="Javatrain/plots/Labeled/AxionPhoton_helioscopes.svg">](https://github.com/DanielMartinezMiravete/Axion-limts/blob/main/Javatrain/plots/Labeled/AxionPhoton_helioscopes.svg)

## Close up Helioscopes plot without proyections

### [Download (.pdf)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_helioscopeslabeled.pdf)
### [Download (.png)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_helioscopes.png)
### [Download (.svg)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_helioscopes.svg)

### &nbsp;
# Close up Halocopes Plot
---
[<img align="right" height="250" src="Javatrain/plots/Labeled/AxionPhoton_haloscopes.svg">](https://github.com/DanielMartinezMiravete/Axion-limts/blob/main/Javatrain/plots/Labeled/AxionPhoton_haloscopes.svg)

## Close up Haloscopes plot without proyections

### [Download (.pdf)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_haloscopeslabeled.pdf)
### [Download (.png)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_haloscopes.png)
### [Download (.svg)](https://github.com/DanielMartinezMiravete/Axion-limts/raw/main/Javatrain/plots/Labeled/AxionPhoton_haloscopes.svg)

### &nbsp;

---

To recreate these images, we need to execute the Python program called "PlotAxionPhoton.py" as follows:
```
python3 example.py    #To plot all the plots from Axion Photon 
```
This will plot all types of graphs listed without their projections. To include the projections, we should modify the "Projections" parameter in PlotAxionPhoton.py and set it to True.


These graphs are generated directly without labels since we have a web application capable of adding them interactively.

[Label's APP](https://danielmartinezmiravete.github.io/Labels-App/)

This is only a preview of the app. To interact with it, you must download the repository. The app is located in the 'Java' folder, and you will also find another folder called 'plot' where the different plots are stored to verify the correct functioning of the app.

This application is only capable of modifying SVG files, which are generated automatically along with the PDFs when running the Python script. Instructions for the webpage are provided within the webpage itself.

There are known bugs such as the app cannot interpret LaTeX. If you have several labels on it and if you want to move a label other than the last label, the coordinates will replace the coordinates of the last label written

As additional information, to interact with the database, you need to use different functions implemented in the script called 'DataBaseGag.py'.
This repository contains Python scripts for interacting with the AxionsGag database. The database is used to manage information about various experiments related to axion research. Below, you'll find instructions on how to use the provided functions to work with the database.

## Getting Started

To interact with the database, follow these steps:

1. Download the repository and navigate to the appropriate directory.
2. Make sure you have SQLite installed or install it if necessary.
3. Modify the file paths in the script to match your directory structure.
4. Uncomment the function calls at the end of the script to execute them and interact with the database.

Please refer to the script for specific usage examples of each function.

## Known Issues

- The application cannot interpret LaTeX.
- When working with multiple labels, moving a label other than the last label will replace the coordinates of the last label written.

