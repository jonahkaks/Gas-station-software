import time

import gi

from src.database_handler import DataBase

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import locale


class Definitions(object):
    def __init__(self):
        self.amount_array = []
        self._sales_date = None
        self._branch_id = None
        self.database = DataBase("julaw.db")

    def set_date(self, value):
        self._sales_date = value

    def get_date(self):
        return self._sales_date

    def get_id(self):
        return self._branch_id

    def set_id(self, value):
        self._branch_id = value

    def insertion(self, array):
        for k in array:
            account_id = array[k][0]
            contra_id = array[k][1]
            date = array[k][2]
            details = array[k][3]
            folio = array[k][4]
            debit = array[k][5]
            credit = array[k][6]
            uuid = time.time()
            self.database.hinsert("transactions", "branchid, account_id, contra_id,"
                                                  " date, details, folio, debit, credit, uuid", self._branch_id,
                                  account_id, contra_id, date, details, folio, debit, credit, uuid)
        return 0

    def login(self, user, password):
        result = self.database.hselect("users.branchid, branch.name",
                                       "users, branch",
                                       " WHERE username='{0}' AND password='{1}'".format(user, password),
                                       "AND users.branchid = branch.branchid")
        if result:
            return result[0][0], result[0][1]
        else:
            return 0


    def trial(self, date_range):
        result = []
        code_names = {}
        tables = self.database.hselect("code, name", "accounts", "where placeholder=0", "")
        res = self.database.hselect("account_id, debit, credit", "transactions",
                                    " WHERE branchid={0} AND {1}".format(self.get_id(), date_range), "")

        for n in tables:
            code_names[n[0]] = n[1]
        for i in code_names:
            balance = 0
            for n in res:
                if n[0] == i:
                    balance += n[1] - n[2]
                else:
                    continue
            if balance and balance > 0:
                result.append((code_names[i], str(balance), None))
            elif balance and balance < 0:
                result.append((code_names[i], None, str(balance * -1)))
            else:
                result.append((code_names[i], None, None))
        return result

    def __del__(self):
        self.database.__del__()


def real_insert(arr, index, value):
    try:
        arr[index] = value
    except IndexError:
        arr.insert(index, value)


def add_array(args=[], index=0):
    total = 0
    if index:
        for a in args[: index]:
            total += a
    else:
        for a in args:
            total += a
    return total


def thousand_separator(data):
    if data is not None:
        try:
            d = float(data)
            return locale.format("%05.2f", d, grouping=True)
        except ValueError:
            return str(0)


def make_date(year, month, day):
    return '{0:04d}-{1:02d}-{2:02d}'.format(year, month + 1, day)


def error_handler(parent, error):
    dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, error)
    dialog.run()

    dialog.destroy()
