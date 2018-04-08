#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sqlite3


class DataBase:
    def __init__(self, db_name):
        base = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base, db_name)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def hinsert(self, table, table_headers, *args):
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
            print("failed")
        if table == "Purchases":
            try:
                self.cur.execute("CREATE TRIGGER {0}_stock_log AFTER INSERT ON {1} BEGIN "
                                 "INSERT INTO Stock(date, branchid, uuid, transfered,"
                                 " details, debit, credit) VALUES(NEW.date,"
                                 " NEW.branchid, '{0}' || NEW.id, 'Credit Purchases',(SELECT inventory_name "
                                 "FROM Inventory WHERE Inventory_code = New.Inventory_id) ,"
                                 "New.quantity*New.unit_price"
                                 " , 0);END;".format(table.lower(), table))
                self.cur.execute("CREATE TRIGGER {0}_stock_update_log AFTER UPDATE ON {1} BEGIN "
                                 "UPDATE Stock SET  debit=New.quantity*New.unit_price "
                                 "WHERE uuid='{0}' || NEW.id"
                                 ";END;".format(table.lower(), table))
                self.cur.execute("CREATE TRIGGER {0}_stock_delete_log AFTER DELETE ON {1} BEGIN "
                                 "DELETE FROM Stock WHERE uuid='{0}' || OLD.id"
                                 ";END;".format(table.lower(), table))
                self.conn.commit()
            except sqlite3.OperationalError:
                pass
        if table == "fuel":
            try:
                self.cur.execute("CREATE TRIGGER {0}_stock_log AFTER INSERT ON {1} BEGIN "
                                 "INSERT INTO Stock(date, branchid, uuid, transfered,"
                                 " details, debit, credit) VALUES(NEW.date,"
                                 " NEW.branchid, '{0}' || NEW.id, 'Credit Sales',"
                                 "New.product , 0 ,(New.closing_meter-(New.opening_meter+New.rtt))*New.price);"
                                 "END;".format(
                    table.lower(), table))
                self.cur.execute("CREATE TRIGGER {0}_stock_update_log AFTER UPDATE ON {1} BEGIN "
                                 "UPDATE Stock SET debit=0, credit=(New.closing_meter-("
                                 "New.opening_meter+New.rtt))*New.price "
                                 "WHERE uuid='{0}' || NEW.id"
                                 ";END;".format(table.lower(), table))
                self.cur.execute("CREATE TRIGGER {0}_stock_delete_log AFTER DELETE ON {1} BEGIN "
                                 "DELETE FROM Stock WHERE uuid='{0}' || OLD.id"
                                 ";END;".format(table.lower(), table))
                self.cur.execute("CREATE TRIGGER {0}_cash_log AFTER INSERT ON {1} BEGIN "
                                 "INSERT INTO Cash(date, branchid, uuid, transfered,"
                                 " details, credit, debit) VALUES(NEW.date,"
                                 " NEW.branchid, '{0}' || NEW.id, 'None',"
                                 "New.product , 0 ,(New.closing_meter-(New.opening_meter+New.rtt))*New.price);"
                                 "END;".format(
                    table.lower(), table))
                self.cur.execute("CREATE TRIGGER {0}_cash_update_log AFTER UPDATE ON {1} BEGIN "
                                 "UPDATE Cash SET credit = 0, debit=New.closing_meter-("
                                 "New.opening_meter+New.rtt))*New.price "
                                 "WHERE uuid='{0}' || NEW.id"
                                 ";END;".format(table.lower(), table))
                self.cur.execute("CREATE TRIGGER {0}_cash_delete_log AFTER DELETE ON {1} BEGIN "
                                 "DELETE FROM Cash WHERE uuid='{0}' || OLD.id"
                                 ";END;".format(table.lower(), table))
                self.conn.commit()
            except sqlite3.OperationalError:
                pass

    def hupdate(self, table, field, condition):
        self.cur.execute("UPDATE  {0} SET {1} WHERE {2}".format(table, field, condition))
        self.conn.commit()

    def hdelete(self, table, condition):
        self.cur.execute("DELETE FROM {0} WHERE {1}".format(table, condition))
        self.conn.commit()

    def hdrop(self, table):
        self.cur.execute("DROP TABLE '{0}'".format(table))
        self.conn.commit()

    def insert_trigger(self, table, super_table, account_type):
        if account_type == "NewTopLevelAccount":
            pass
        else:
            try:
                self.cur.execute("CREATE TRIGGER {0}_log AFTER INSERT ON {1} BEGIN "
                                 "INSERT INTO {2}(date, branchid, uuid, transfered,"
                                 " details, debit, credit) VALUES(NEW.date,"
                                 " NEW.branchid, '{0}' || NEW.id, '{1}:' || NEW.details, NEW.transfered,"
                                 "NEW.debit, "
                                 "NEW.credit);END;".format(table.lower(), table, super_table))
                self.cur.execute("CREATE TRIGGER {0}_update_log AFTER UPDATE ON {1} BEGIN "
                                 "UPDATE {2} SET details='{1}:' || NEW.details, transfered=New.transfered,"
                                 " debit=NEW.debit, "
                                 "credit=NEW.credit WHERE uuid='{0}' || NEW.id"
                                 ";END;".format(table.lower(), table, super_table))
                self.cur.execute("CREATE TRIGGER {0}_delete_log AFTER DELETE ON {1} BEGIN "
                                 "DELETE FROM '{2}' WHERE uuid='{0}' || OLD.id"
                                 ";END;".format(table.lower(), table, super_table))
                self.conn.commit()
            except sqlite3.OperationalError:
                pass

    def __del__(self):
        self.conn.close()
