import sqlite3 as sql

"""
# Example of usage:
import DataBaseClass as db
database = db.DataBaseGag("Axions.db")
AxionsGag = [
    ['qcdband', 'band', PATH_DATA + 'QCD_band.dat', "facecolor='yellow'", 1, 1, 1, 1, 1, 1, 0],
    ['old_haloscopes', 'band', PATH_DATA + 'MicrowaveCavities.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['ABRA3', 'line', PATH_DATA + 'ABRAres_3.dat', "color='green', linewidth=0.1, linestyle='-'", 1, 1, 1, 1, 1, 1, 0],
    ['ADMX2018', 'band', PATH_DATA + 'ADMX2018.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, 0, 0, 0, 0, 0, 0],
    ['BabyIAXO', 'band', PATH_DATA + 'miniIAXO.dat', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, 1, 1, 0, 1, 0, 1],
    ['IAXO', 'band', PATH_DATA + 'IAXO_nominal.txt', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, 1, 1, 0, 1, 0, 1],
    ['CAST', 'band', PATH_DATA + 'cast_env_2016.dat', "facecolor='deepskyblue', edgecolor='blue', linewidth=0.5", 1, 1, 1, 0, 1, 0, 1],
]
database.insert_rows(AxionsGag)
data = database.read_rows()
print(data)
"""

"""
# Example of usage:
import DataBaseClass as db
database = db.DataBaseGae("Axions.db")
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
"""

"""
# Example of usage:
import DataBaseClass as db
database = db.DataBaseLabels("Axions.db")
labels = [
    ["CAST", 1.0e-6, 1.0e-6, "color='blue', fontsize=10", 1, 0],
    ["IAXO", 1.0e-6, 1.0e-6, "color='blue', fontsize=10", 1, 1],
]
database.insert_rows(labels)
data = database.read_rows()
print(data)
"""


# DataBase class is not intended to be used directly, but to be inherited by DataBaseGag and DataBaseGae
class DataBase:
    def __init__(self, file_database="Axions.db", name: str = "Axions"):
        self.FILE_DATABASE = file_database
        try:
            self.conn = sql.connect(self.FILE_DATABASE)
        except Error as e:
            print(e)
            exit()

        self.cursor = self.conn.cursor()
        self.name = name

    def get_rows(self, selection: str = ""):
        instruction = f"SELECT * FROM {self.name}"
        if selection != "":
            instruction += f" WHERE {selection}"

        self.cursor.execute(instruction)
        rows = self.cursor.fetchall()
        return rows

    def update_row(self, name, field, value):
        instruction = (
            f"UPDATE {self.name} SET {field} = '{value}' WHERE name = '{name}'"
        )
        self.cursor.execute(instruction)
        self.conn.commit()

    def delete_rows(self, selection: str = "", confirm: bool = False):
        instruction = f"DELETE FROM {self.name}"
        if selection != "":
            instruction += f" WHERE {selection}"

        if not confirm:
            print(
                "WARNING: You are trying to delete all rows "
                + ("WHERE '" + selection + "' " if selection != "" else "")
                + "from the table"
            )
            ans = input("Are you sure? (y/n)\n")
            if ans not in ["y", "yes", "Y", "YES"]:
                print("Aborting")
                return

        self.cursor.execute(instruction)
        self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()


class DataBaseGag(DataBase):
    def __init__(self, file_database="Axions.db", name: str = "AxionsGag"):
        DataBase.__init__(self, file_database, name)

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name} (
            name TEXT,
            type TEXT,
            path TEXT,
            drawOptions TEXT,
            wildType INTEGER,
            large_panorama INTEGER,
            panorama INTEGER,
            helioscopes INTEGER,
            haloscopes INTEGER,
            lswexps INTEGER,
            projection INTEGER
            )"""
        )
        self.conn.commit()

    def insert_row(
        self,
        name,
        type,
        path,
        drawOptions="",
        noPT=1,
        LP=0,
        P=0,
        Helios=0,
        Halos=0,
        LSW=0,
        projection=0,
    ):
        instruction = f"INSERT INTO {self.name}  VALUES ('{name}', '{type}','{path}','{drawOptions}','{noPT}','{LP}','{P}','{Helios}','{Halos}',{LSW},{projection})"
        self.cursor.execute(instruction)
        self.conn.commit()

    def insert_rows(self, rows):
        instruction = f"INSERT INTO {self.name} VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        self.cursor.executemany(instruction, rows)
        self.conn.commit()


class DataBaseGae(DataBase):
    def __init__(self, file_database="Axions.db", name: str = "AxionsGae"):
        DataBase.__init__(self, file_database, name)

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name} (
            name TEXT,
            type TEXT,
            path TEXT,
            drawOptions TEXT,
            wildType INTEGER,
            projection INTEGER
            )"""
        )
        self.conn.commit()

    def insert_row(self, name, type, path, drawOptions="", noPT=1, projection=0):
        instruction = f"INSERT INTO {self.name}  VALUES ('{name}', '{type}','{path}','{drawOptions}',{noPT},{projection})"
        self.cursor.execute(instruction)
        self.conn.commit()

    def insert_rows(self, rows):
        instruction = f"INSERT INTO {self.name} VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(instruction, rows)
        self.conn.commit()


class DataBaseLabels(DataBase):
    def __init__(self, file_database="Axions.db", name: str = "Labels"):
        DataBase.__init__(self, file_database, name)

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name} (
            label TEXT,
            x_position REAL,
            y_position REAL,
            drawOptions TEXT,
            onoff INTEGER,
            projection INTEGER
            )"""
        )
        self.conn.commit()

    def insert_row(
        self, label, x_position, y_position, drawOptions="", on=1, projection=0
    ):
        instruction = f"INSERT INTO {self.name}  VALUES ('{label}', '{x_position}', '{y_position}', '{drawOptions}', {on}, {projection})"
        self.cursor.execute(instruction)
        self.conn.commit()

    def insert_rows(self, rows):
        instruction = f"INSERT INTO {self.name} VALUES (?, ?, ?, ?, ?, ?)"

        self.cursor.executemany(instruction, rows)
        self.conn.commit()
