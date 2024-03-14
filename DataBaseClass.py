from __future__ import annotations

import sqlite3 as sql

"""
# Example of usage:
import DataBaseClass as db
database = db.DataBaseGag("databases/NewAxions.db", commit=True) # this will create (if it doesn't already exists) a table named AxionsGag (default) at databases/NewAxions.db
path = "data/axion/"
AxionsGag = [
    ['qcdband', 'band', path + 'QCD_band.dat', "facecolor='yellow'", 0, '', '', 1, 1, 0, 0, 0, 0, 0, 0],
    ['CMB_DEsuE', 'band', path + 'cosmoalp/CMB_DEsuE.txt', "facecolor='forestgreen', edgecolor='darkgreen', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    ['old_haloscopes', 'band', path + 'MicrowaveCavities.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['RADES2021', 'band', path + 'RADES2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2104.13798', '2021', 0, 0, 1, 1, 0, 0, 0, 0],
    ['CAST', 'band', path + 'cast_env_2016.dat', "facecolor='deepskyblue', edgecolor='blue', linewidth=0.5", 0, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['BabyIAXO', 'band', path + 'miniIAXO.dat', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['IAXO', 'band', path + 'IAXO_nominal.txt', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
]
database.insert_rows(AxionsGag)
data = database.get_rows_where("1")
print(data)
"""

"""
# Example of usage:
import DataBaseClass as db
database = db.DataBaseGae("databases/NewAxions.db", commit=True)  # this will create (if it doesn't already exists) a table named AxionsGae (default) at databases/NewAxions.db
path1 = 'data/axion/hints/'
path2 = 'data/axion/gaegag/'
AxionsGae= [
    ["DFSZ1_starhint", "region", path1 + "DFSZ1_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='springgreen', edgecolor='darkgreen', alpha=0.2", 0, '', ''],
    ["AJ83_starhint", "region", path1 + "AJ83_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='red', edgecolor='red', alpha=0.2", 0, '', ''],
    ["QCDband", "band", path2 + "DFSZband_gaegag.dat", "facecolor='lemonchiffon', edgecolor='none', linewidth=1", 0, '', ''],
    ["CAST_gae", "band", path2 + "CAST_gae_gagg.dat", "facecolor='steelblue', edgecolor='darkblue', linewidth=0.5", 0, '', ''],

    ["IAXO_gae", "band", path2 + "sqrtgaagae_sc2.dat", "facecolor='skyblue', edgecolor='black', linewidth=0.5, alpha=0.3", 1, '', ''],
    ["IAXO_gae_l", "line", path2 + "sqrtgaagae_sc2.dat", "color='black', linewidth=0.5, linestyle='--'", 1, '', ''],
]
database.insert_rows(AxionsGae)
data = database.get_rows_where("1")
print(data)
"""


# DataBase class is the generic database class that can be used to load an already existing database.
class DataBase:
    def __init__(
        self, file_database="Axions.db", name: str = "Axions", commit: bool = False
    ):
        self.FILE_DATABASE = file_database
        try:
            self.conn = sql.connect(self.FILE_DATABASE)
        except Error as e:
            print(e)
            exit()

        self.cursor = self.conn.cursor()
        self.name = name
        self.commit = commit  # If commit is True, the database file will be updated

    def set_commit(self, commit: bool):
        self.commit = commit

    def get_rows_where(self, selection: str = ""):
        instruction = f"SELECT * FROM {self.name}"
        if selection != "":
            instruction += f" WHERE {selection}"

        self.cursor.execute(instruction)
        rows = self.cursor.fetchall()
        return rows

    def get_rows(self, field: str, values: list):
        if type(values) not in [list, tuple]:
            values = [values]

        instruction = f"SELECT * FROM {self.name}"
        instruction += f" WHERE {field} IN ("
        instruction += ", ".join([f"'{value}'" for value in values])
        instruction += ")"

        # order the rows in the same order as the values
        instruction += " ORDER BY CASE "
        order = 1
        for value in values:
            instruction += f" WHEN {field} = '{value}' THEN {order}"
            order += 1
        instruction += f" ELSE {order} END"
        # print(instruction)

        self.cursor.execute(instruction)
        rows = self.cursor.fetchall()

        # check if all values are in the rows
        # only available for field = "name"
        if field == "name":
            rows_values = [row[0] for row in rows]
            for value in values:
                if value not in rows_values:
                    print(f"WARNING: {value} not found in the database")
                    # try to find LIKE values
                    instruction = (
                        f"SELECT * FROM {self.name} WHERE {field} LIKE '%{value}%'"
                    )
                    self.cursor.execute(instruction)
                    candidates = self.cursor.fetchall()
                    candidates = [cand[0] for cand in candidates]  # extract the names
                    if len(candidates) > 0:
                        print(f"Did you mean any of these? {candidates}")
                    else:
                        print("No candidates found")

        return rows

    def update_row(self, name, field, value):
        instruction = (
            f"UPDATE {self.name} SET {field} = '{value}' WHERE name = '{name}'"
        )
        self.cursor.execute(instruction)
        if self.commit:
            self.conn.commit()

    def delete_rows(self, selection: str = "", confirm: bool = False):
        instruction = f"DELETE FROM {self.name}"
        if selection != "":
            instruction += f" WHERE {selection}"
        self.cursor.execute(instruction)

        if self.commit:
            if not confirm:
                print(
                    "WARNING: You are trying to delete all rows "
                    + ("WHERE '" + selection + "' " if selection != "" else "")
                    + "from the table"
                )
                if input("Are you sure? (y/n)\n") not in ["y", "yes", "Y", "YES"]:
                    print("Aborting")
                    return

            self.conn.commit()

    def __del__(self):
        if self.commit:
            self.conn.commit()
        self.conn.close()


class DataBaseGag(DataBase):
    def __init__(
        self, file_database="Axions.db", name: str = "AxionsGag", commit: bool = False
    ):
        DataBase.__init__(self, file_database, name, commit)

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name} (
            name TEXT,
            type TEXT,
            path TEXT,
            drawOptions TEXT,
            projection INTEGER,
            source TEXT,
            year TEXT,
            hint INTEGER,
            model INTEGER,
            cosmology INTEGER,
            haloscope INTEGER,
            stellar INTEGER,
            helioscope INTEGER,
            laboratory INTEGER,
            LSW INTEGER
            )"""
        )
        if self.commit:
            self.conn.commit()

    def insert_row(
        self,
        name,
        type_,
        path,
        drawOptions="",
        projection=0,
        source="",
        year="",
        hint=0,
        model=0,
        cosmology=0,
        haloscope=0,
        stellar=0,
        helioscope=0,
        laboratory=0,
        LSW=0,
    ):
        lst = [
            name,
            type_,
            path,
            drawOptions,
            projection,
            source,
            year,
            hint,
            model,
            cosmology,
            haloscope,
            stellar,
            helioscope,
            laboratory,
            LSW,
        ]
        self.insert_rows([lst])

    def insert_rows(self, rows: list):
        # convert tuple to list
        if type(rows) == tuple:
            rows = [row for row in rows]
        # check if rows is a list
        if type(rows) != list:
            print("ERROR: rows must be a list. Aborting.")
            return
        if len(rows) == 0:
            print("Warning: list of rows to insert is empty.")
            return

        # for a single row, make it a list of list
        if type(rows[0]) not in [list, tuple]:
            if len(rows) == 15:
                rows = [rows]

        instruction = f"INSERT INTO {self.name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(instruction, rows)
        if self.commit:
            self.conn.commit()


class DataBaseGae(DataBase):
    def __init__(
        self, file_database="Axions.db", name: str = "AxionsGae", commit: bool = False
    ):
        DataBase.__init__(self, file_database, name, commit)

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name} (
            name TEXT,
            type TEXT,
            path TEXT,
            drawOptions TEXT,
            projection INTEGER,
            source TEXT,
            year TEXT
            )"""
        )
        if self.commit:
            self.conn.commit()

    def insert_row(
        self, name, type_, path, drawOptions="", projection=0, source="", year=""
    ):
        lst = [name, type_, path, drawOptions, projection, source, year]
        self.insert_rows([lst])

    def insert_rows(self, rows):
        # convert tuple to list
        if type(rows) == tuple:
            rows = [row for row in rows]
        # check if rows is a list
        if type(rows) != list:
            print("ERROR: rows must be a list. Aborting.")
            return
        if len(rows) == 0:
            print("Warning: list of rows to insert is empty.")
            return

        # for a single row, make it a list of list
        if type(rows[0]) not in [list, tuple]:
            if len(rows) == 15:
                rows = [rows]

        instruction = f"INSERT INTO {self.name} VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(instruction, rows)
        if self.commit:
            self.conn.commit()


class DataBaseWimps(DataBase):
    def __init__(
        self, file_database="Axions.db", name: str = "Wimps", commit: bool = False
    ):
        DataBase.__init__(self, file_database, name, commit)

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name} (
            name TEXT,
            type TEXT,
            path TEXT,
            drawOptions TEXT,
            projection INTEGER,
            source TEXT,
            year TEXT,
            label TEXT,
            labelPosX REAL,
            labelPosY REAL,
            labelDrawOptions TEXT
            )"""
        )
        if self.commit:
            self.conn.commit()

    def insert_row(
        self,
        name,
        type_,
        path,
        drawOptions="",
        projection=0,
        source="",
        year="",
        label="",
        labelPosX=None,
        labelPosY=None,
        labelDrawOptions="",
    ):
        lst = [
            name,
            type_,
            path,
            drawOptions,
            projection,
            source,
            year,
            label,
            labelPosX,
            labelPosY,
            labelDrawOptions,
        ]
        self.insert_rows([lst])

    def insert_rows(self, rows):
        # convert tuple to list
        if type(rows) == tuple:
            rows = [row for row in rows]
        # check if rows is a list
        if type(rows) != list:
            print("ERROR: rows must be a list. Aborting.")
            return
        if len(rows) == 0:
            print("Warning: list of rows to insert is empty.")
            return

        # for a single row, make it a list of list
        if type(rows[0]) not in [list, tuple]:
            if len(rows) == 15:
                rows = [rows]

        instruction = (
            f"INSERT INTO {self.name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        self.cursor.executemany(instruction, rows)
        if self.commit:
            self.conn.commit()
