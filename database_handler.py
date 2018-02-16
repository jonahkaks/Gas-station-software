#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "julaw.db")
with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()


def insert(table, *args):
    cur.execute("INSERT OR IGNORE INTO " + table + " VALUES" + str(args))
    conn.commit()


def select(operation, table, condition1, condition2):
    try:
        cur.execute("SELECT " + operation + " FROM " + table + condition1 + condition2)
        return cur.fetchall()
    except IndexError:
        print("failed to fetch data" + "\n")


def update(table, field, condition):
    cur.execute("UPDATE  " + table + " SET " + field + " WHERE " + condition)
    conn.commit()


def delete(table, date):
    cur.execute("DELETE FROM " + table + " WHERE date='" + date + "'")
    conn.commit()
