#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sqlite3


class DataBase:
    def __init__(self, db_name):
        base = "../data"
        db_path = os.path.join(base, db_name)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def hinsert(self, table, table_headers, *args):
        print("INSERT OR IGNORE INTO {0}({1}) "
              "VALUES{2}".format(table, table_headers, args))
        self.cur.execute("INSERT OR IGNORE INTO {0}({1}) "
                         "VALUES{2}".format(table, table_headers, args))
        self.conn.commit()
        return self.cur.lastrowid

    def hselect(self, operation, table, condition1, condition2):
        try:
            self.cur.execute("SELECT {0} FROM {1}  {2} {3}".format(operation, table,
                                                                   condition1, condition2))
            return self.cur.fetchall()
        except sqlite3.OperationalError:
            return []

    def hcreate(self, table, sql):
        try:
            self.cur.execute("CREATE TABLE IF NOT EXISTS '{0}'({1})".format(table, sql))
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def hupdate(self, table, field, condition):
        print("UPDATE  {0} SET {1} WHERE {2}".format(table, field, condition))
        self.cur.execute("UPDATE  {0} SET {1} WHERE {2}".format(table, field, condition))
        self.conn.commit()

    def hdelete(self, table, condition):
        try:
            self.cur.execute("DELETE FROM {0} WHERE {1}".format(table, condition))
            self.conn.commit()
            return 1
        except sqlite3.OperationalError as e:
            print("failed to excecute delete:", e)
            return 0

    def __del__(self):
        self.conn.close()
