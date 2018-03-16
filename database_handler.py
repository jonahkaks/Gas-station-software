#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "julaw.db")
with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()


def hinsert(table, table_headers, *args):
    cur.execute("INSERT OR IGNORE INTO {0}({1}) VALUES{2}".format(table, table_headers, args))
    conn.commit()
    return cur.lastrowid


def hselect(operation, table, condition1, condition2):
    try:
        cur.execute("SELECT {0} FROM {1}  {2} {3}".format(operation, table, condition1, condition2))
        return cur.fetchall()
    except IndexError:
        print("failed to fetch data" + "\n")


def hcreate(table, sql):
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS '{0}'({1})".format(table, sql))
        conn.commit()
    except sqlite3.OperationalError:
        print("failed")


def hupdate(table, field, condition):
    cur.execute("UPDATE  {0} SET {1} WHERE {2}".format(table, field, condition))
    conn.commit()


def hdelete(table, condition):
    cur.execute("DELETE FROM {0} WHERE {1}".format(table, condition))
    conn.commit()


def hdrop(table):
    cur.execute("DROP TABLE '{0}'".format(table))
    conn.commit()


def insert_trigger(table, super_table):
    cur.execute("CREATE TRIGGER {0}_log AFTER INSERT ON {1} BEGIN "
                "INSERT INTO {2}(date, uuid, branchid, debit, credit, details)"
                " SELECT date, id, branchid, debit, credit, '{1}'"
                " FROM {1} WHERE id=(SELECT MAX(id) "
                "FROM {1});END;".format(table.lower(), table, super_table))
    conn.commit()

    cur.execute("CREATE TRIGGER {0}_update_log AFTER UPDATE ON {1} BEGIN "
                "UPDATE {2} SET debit=(SELECT debit FROM {1}), "
                "credit=(SELECT credit FROM {1}) WHERE uuid={0}+(SELECT MAX(id) FROM {1});END;"
                "".format(table.lower(), table, super_table))
    conn.commit()
