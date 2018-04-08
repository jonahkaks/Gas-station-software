import sqlite3

import gi

from database_handler import DataBase

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import locale


class Definitions(object):
    def __init__(self):
        self.pro = []
        self.op = []
        self.cl = []
        self.rt = []
        self.pr = []
        self.al = []
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

    def sales_litres(self, product_id=0, product="product", opening_stock=0, closing_stock=0, rtt=0, price=0):
        opening_stock = float(opening_stock)
        closing_stock = float(closing_stock)
        rtt = float(rtt)
        price = int(price)
        litres = closing_stock - (opening_stock + rtt)

        if product_id:
            field = "product='{0}', opening_meter={1},closing_meter={2}," \
                    "rtt={3}, price={4}".format(product, opening_stock, closing_stock, rtt, price)
            self.database.hupdate("fuel", field, "id={0}".format(product_id))
            insert_id = product_id
        else:
            insert_id = self.database.hinsert("fuel", "branchid, date, product, opening_meter,"
                                                      " closing_meter, rtt, price",
                                              self.get_id(), str(self.get_date()), product, opening_stock,
                                              closing_stock, rtt, price)
        return str(locale.format("%05.2f", litres, grouping=False)), insert_id

    def dips(self, dips_id, pms_od=0, pms_cd=0, ago_od=0, ago_cd=0, bik_od=0, bik_cd=0):
        pms_od = float(pms_od)
        pms_cd = float(pms_cd)
        ago_od = float(ago_od)
        ago_cd = float(ago_cd)
        bik_od = float(bik_od)
        bik_cd = float(bik_cd)

        try:
            field = "pms_od={0},pms_cd={1},ago_od={2}," \
                    "ago_cd={3},bik_od={4}," \
                    "bik_cd={5}".format(pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd)

            self.database.hupdate("dips", field, "id={0}".format(dips_id))
            insert_id = dips_id
        except sqlite3.OperationalError:
            insert_id = self.database.hinsert("dips", "branchid, date, pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd",
                                              self.get_id(), str(self.get_date()),
                                              pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd)
        return str(pms_od - pms_cd), str(ago_od - ago_cd), str(bik_od - bik_cd), insert_id

    def insertion(self, table, date, operation, affected, position, details, folio, debit, credit):
        debit = float(debit)
        credit = float(credit)
        if position is not None:
            insert_id = position
            pass
        else:
            insert_id = self.database.hinsert(table, "date, transfered, branchid, details, folio, debit, credit",
                                              date, operation + " " + affected, self.get_id(),
                                              details, folio, debit, credit)
            if operation == "Debit":
                if credit == 0.0:
                    self.database.hinsert(affected, "date, uuid, transfered, branchid, details, folio, debit, credit",
                                          date, table.lower() + str(insert_id), "Credit " + table,
                                          self.get_id(), details, folio, debit, credit)

                elif debit == 0.0:
                    self.database.hinsert(affected, "date, uuid, transfered, branchid, details, folio, debit, credit",
                                          date, table.lower() + str(insert_id), "Credit " + table,
                                          self.get_id(), details, folio, credit, debit)

            elif operation == "Credit":
                if credit == 0.0:
                    self.database.hinsert(affected, "date, uuid, transfered, branchid, details, folio, debit, credit",
                                          date, table.lower() + str(insert_id), "Debit " + table,
                                          self.get_id(), details, folio, credit, debit)

                elif debit == 0.0:
                    self.database.hinsert(affected, "date, uuid, transfered, branchid,"
                                                    " details, folio, debit, credit",
                                          date, table.lower() + str(insert_id), "Debit " + table,
                                          self.get_id(), details, folio, debit, credit)
            elif operation == "":
                pass

        return insert_id

    def login(self, user, password):
        result = None
        try:
            result = self.database.hselect("id, username, pumps",
                                           "users",
                                           " WHERE username='{0}' AND password='{1}'".format(user, password), "")[0]
        except IndexError:
            pass
        if result:
            return result[0], result[1], result[2]
        else:
            return 0

    def get_data(self, table):
        result = self.database.hselect("*", table,
                                       " WHERE branchid={0} AND date='{1}'".format(self.get_id(),
                                                                                   self.get_date()), "")
        return result

    def sales_shs(self, index=0, litres=0, price=0):
        price = int(price)
        litres = float(litres)

        real_insert(self.pr, index, price)

        real_insert(self.amount_array, index, litres * price)
        return self.amount_array[index], add_array(self.amount_array)

    def purchase(self, index, invoice, inventory, quantity, price):
        quantity = float(quantity)
        price = float(price)
        try:
            field = "Invoice_id={0}, Inventory_id={1}," \
                    " quantity={2}, unit_price={3}".format(invoice,
                                                           inventory, quantity, price)
            self.database.hupdate("Purchases", field, "id={0}".format(index))

            insert_id = index
        except sqlite3.OperationalError:
            insert_id = self.database.hinsert("Purchases", "date, branchid, Invoice_id,"
                                                           " Inventory_id, quantity, unit_price",
                                              str(self.get_date()), self.get_id(),
                                              invoice, inventory, quantity, price)
        return insert_id

    def cashbook(self):
        debit = []
        credit = []
        cash = self.database.hselect("details, folio, debit, credit", "Cash",
                                     " WHERE branchid={0}".format(str(self.get_id())),
                                     "AND date='{0}'".format(self.get_date()))
        bank = self.database.hselect("details, folio, debit, credit", "Bank",
                                     " WHERE branchid={0}".format(str(self.get_id())),
                                     "AND date='{0}'".format(self.get_date()))

        for i, n in enumerate(bank):
            if n[2] > 0:
                debit.append((str(n[0]), n[1], None, str(thousand_separator(n[2]))))
            elif n[2] == 0.0:
                credit.append((str(n[0]), n[1], None, str(thousand_separator(n[3]))))

        for i, n in enumerate(cash):
            if n[2] > 0:
                debit.append((str(n[0]), n[1], str(thousand_separator(n[2])), None))
            elif n[2] == 0.0:
                credit.append((str(n[0]), n[1], str(thousand_separator(n[3])), None))
        return debit, credit

    def trial(self):
        levels = []
        names = []
        type = []
        result = []
        tables = self.database.hselect("name, level, account_type", "accounts",
                                       " WHERE branchid={0}".format(str(self.get_id())), "")

        for name, level, account_type in tables:
            names.append(name)
            levels.append(level)
            type.append(account_type)

        for i, x in enumerate(names):
            if x in levels:
                pass
            else:
                try:
                    res = self.database.hselect("SUM(debit-credit)", x,
                                                " WHERE branchid={0}".format(str(self.get_id())),
                                                " AND date='{0}'".format(str(self.get_date())))[0][0]
                except IndexError:
                    res = 0
                if res and res > 0:
                    result.append((x, str(res), None))
                elif res and res < 0:
                    result.append((x, None, str(res * -1)))
                else:
                    result.append((x, None, None))
        return result

    def get_price(self):
        id = self.get_id()
        date = self.get_date()
        pms = ""
        ago = ""
        bik = ""
        try:
            pms = self.database.hselect("price", "Prices",
                                        "WHERE branchid={0} AND "
                                        "start_date<='{1}' AND stop_date>'{1}'"
                                        " AND Inventory_code={2}".format(id,
                                                                         date,
                                                                         self.database.hselect("Inventory_code",
                                                                                               "Inventory",
                                                                                               "WHERE Inventory_name"
                                                                                               "='PMS'",
                                                                                               "AND branchid={0}".format(
                                                                                                   id))[
                                                                             0][0]), "")[0][0]
        except IndexError:
            pass

        try:
            ago = self.database.hselect("price", "Prices",
                                        "WHERE branchid={0} AND "
                                        "start_date<='{1}' AND stop_date>'{1}'"
                                        " AND Inventory_code={2}".format(id,
                                                                         date,
                                                                         self.database.hselect("Inventory_code",
                                                                                               "Inventory",
                                                                                               "WHERE Inventory_name"
                                                                                               "='AGO'",
                                                                                               "AND branchid={0}".format(
                                                                                                   id))[
                                                                             0][0]), "")[0][0]
        except IndexError:
            pass
        try:
            bik = self.database.hselect("price", "Prices",
                                        "WHERE branchid={0} AND "
                                        "start_date<='{1}' AND stop_date>'{1}'"
                                        " AND Inventory_code={2}".format(id, date,
                                                                         self.database.hselect("Inventory_code",
                                                                                               "Inventory",
                                                                                               "WHERE Inventory_name"
                                                                                               "='BIK'",
                                                                                               "AND branchid={0}".format(
                                                                                                   id))[0][
                                                                             0]),
                                        "")[0][0]
        except IndexError:
            pass
        return pms, ago, bik

    def get_cash_profit(self):
        cash_hand = 0
        try:
            cash_hand = self.database.hselect("SUM(debit-credit)", "Cash",
                                              "WHERE branchid={0} AND date='{1}'".format(self.get_id(),
                                                                                         self.get_date()), "")[0][0]
        except:
            pass

        return cash_hand

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
