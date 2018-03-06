#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "julaw.db")
with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()


def hinsert(table, *args):
    cur.execute("INSERT OR IGNORE INTO {0} VALUES{1}".format(table, args))
    conn.commit()


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
    print("DELETE FROM {0} WHERE {1}".format(table, condition))
    cur.execute("DELETE FROM {0} WHERE {1}".format(table, condition))
    conn.commit()


def hdrop(table):
    print("DROP TABLE '{0}'".format(table))
    cur.execute("DROP TABLE '{0}'".format(table))
    conn.commit()
