from __future__ import annotations

import sqlite3 as sql
from .utils import resolve_relative_path, get_absolute_path
import pandas as pd

# DataBase class is the generic database class that can be used to load an already existing database.
class DataBase:
    def __init__(
        self, file_database: str, name: str, commit: bool = False
    ):  
        try:
            absolute_path = get_absolute_path(file_database)
        except FileNotFoundError:
            print(f"WARNING: The file '{file_database}' does not exist. Creating a new database.")
            absolute_path = file_database
        self.FILE_DATABASE = absolute_path

        self.conn = sql.connect(self.FILE_DATABASE)
        self.cursor = self.conn.cursor()
        self.name = name
        self.commit = commit  # If commit is True, the database file will be updated

    def set_commit(self, commit: bool):
        self.commit = commit

    def get_table_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        try:
            table_names = [table[0] for table in tables]
        except:
            table_names = tables
        return table_names

    def get_columns(self):
        self.cursor.execute(f"PRAGMA table_info({self.name})")
        columns = self.cursor.fetchall()
        return columns

    def get_columns_names(self):
        columns = self.get_columns()
        return [col[1] for col in columns]

    def get_columns_types(self):
        columns = self.get_columns()
        return [col[2] for col in columns]

    def get_columns_names_types(self):
        columns = self.get_columns()
        return [(col[1], col[2]) for col in columns]
    
    def get_pandas_dataframe(self):
        return pd.read_sql_query(f"SELECT * FROM {self.name}", self.conn)

    def get_rows_where(self, selection: str = ""):
        instruction = f"SELECT * FROM {self.name}"
        if selection != "":
            instruction += f" WHERE {selection}"

        self.cursor.execute(instruction)
        rows = self.cursor.fetchall()

        # convert list of rows to dictionary
        rows_dict = {}
        column_names = self.get_columns_names()
        for row in rows:
            rows_dict[row[0]] = dict(zip(column_names[1:], row[1:]))

        return rows_dict


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
        
        # convert list of rows to dictionary
        rows_dict = {}
        column_names = self.get_columns_names()
        for row in rows:
            rows_dict[row[0]] = dict(zip(column_names[1:], row[1:]))

        return rows_dict

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
        super().__init__(file_database, name, commit)

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
        super().__init__(file_database, name, commit)

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
        self, file_database="Wimps.db", name: str = "Wimps_SI", commit: bool = False
    ):
        super().__init__(file_database, name, commit)

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
