#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .dialog_account import DialogAccount
from .double_entry import *
from ..utils import Datetime

try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ImportError as e:
    print("failed to import gtk", e)


class Accounts(Gtk.ScrolledWindow):
    def __init__(self, branch_id, *args, **kwargs):
        super(Accounts, self).__init__(*args, **kwargs)
        self.database = DataBase("julaw.db")
        self.branch_no = branch_id
        self.date_range = None
        self.balance = None
        self.start_date = Datetime.CalendarEntry()
        self.start_date.entry.connect("changed", self.fetch_data)
        self.stop_date = Datetime.CalendarEntry()
        self.stop_date.entry.connect("changed", self.fetch_data)

        self.account_codes = {}
        self.account_types = {}
        self.code_types = {}
        self.account_placeholder = {}
        self.account_children = {}
        self.account_value = {'root': ['Assets', 'Expenses', 'Liabilities', 'Incomes', 'Equity']}
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.set_margin_top(20)
        self.hbox.set_margin_bottom(10)
        self.hbox.pack_start(self.start_date, False, False, 0)
        self.hbox.pack_end(self.stop_date, False, True, 0)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.pack_start(self.hbox, False, True, 0)

        self.account_list = Gtk.TreeStore(str, str, str, str, str)
        self.tree = Gtk.TreeView.new_with_model(self.account_list)
        self.tree_view_columns()
        self.scrollable_tree_list = Gtk.ScrolledWindow()
        self.scrollable_tree_list.add(self.tree)
        self.box.pack_start(self.scrollable_tree_list, True, True, 0)
        self.add(self.box)
        self.__connect_signals()
        self.accounts = self.get_account_data()
        self.make_accounts(None, "root")
        self.fetch_data()
        self.show_all()

    def get_account_data(self):
        accounts = self.database.hselect("code, name, value , description, type, placeholder, parent", "accounts",
                                         "", "")
        return accounts

    def __connect_signals(self):
        self.start_date.entry.connect("changed", self.fetch_data)
        self.stop_date.entry.connect("changed", self.fetch_data)
        self.tree.connect("row-activated", self.menu_caller)
        self.tree.connect("button-press-event", self.right_clicked)
        self.scrollable_tree_list.connect("button-press-event", self.right_clicked)
        self.connect("destroy", Gtk.main_quit)

    def tree_view_columns(self):
        renderer = Gtk.CellRendererText()
        render_pix = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("Account Name")
        renderer.set_fixed_size(400, 25)
        column.pack_start(render_pix, False)
        column.add_attribute(render_pix, 'icon_name', 0)
        column.pack_end(renderer, False)
        column.add_attribute(renderer, 'text', 1)
        column.set_sort_column_id(1)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(400, 25)
        column = Gtk.TreeViewColumn("Description", renderer, text=2)
        renderer.connect("edited", self.edit_data)
        column.set_sort_column_id(2)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_fixed_size(400, 25)
        column = Gtk.TreeViewColumn("Balance(UGX)", renderer, text=3, foreground=4)
        column.set_sort_column_id(3)
        self.tree.append_column(column)

    def menu_caller(self, widget, row, col):
        model = widget.get_model()
        name = model[row][1]

        if self.account_placeholder[name]:
            pass
        else:
            DoubleEntry(self.branch_no,
                        self.date_range, self.account_codes[name], self.account_types[name],
                        name, self.get_ancestor(Gtk.ApplicationWindow), Gtk.DialogFlags.MODAL,
                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
            self.fetch_data()

    def right_clicked(self, widget, event):
        if event.button == 3:
            pop = Gtk.Menu.new()
            model = widget.get_model()
            row = 0
            try:
                row, column, posx, posy = widget.get_path_at_pos(int(event.x), int(event.y))
                account = model[row][1]
            except TypeError:
                account = "root"
            add_account = Gtk.MenuItem("New Account")
            add_account.connect("activate", self.account_methods, 0, row, account)
            pop.insert(add_account, 0)
            remove_account = Gtk.MenuItem("Delete Account")
            pop.insert(remove_account, 1)
            remove_account.connect("activate", self.account_methods, 1, row, account)
            pop.popup(None, None, None, None, event.button, Gtk.get_current_event_time())
            pop.show_all()

    def account_methods(self, widget, operation, row, account):
        iterator = self.account_list.get_iter(row)
        if operation:
            i = self.database.hdelete("accounts", "code={0}".format(self.account_codes[account]))
            if i:
                self.account_list.remove(iterator)
                self.fetch_data()
            else:
                error_handler(self.get_ancestor(Gtk.ApplicationWindow), "Failed to delete account")
        else:
            DialogAccount(self.account_list, self.database, iterator, account, self.account_value,
                          self.account_codes, self.account_types, self.code_types, self.account_placeholder)

    def make_accounts(self, t, a):
        for i, account in enumerate(self.accounts):
            if account[6] == a:
                self.account_codes[account[1]] = account[0]
                self.account_types[account[1]] = account[4]
                self.code_types[account[0]] = account[4]
                self.account_value[account[1]] = account[2]
                self.account_placeholder[account[1]] = account[5]
                its = self.account_list.append(t, ["document-new", account[1], account[3], None, None])
                try:
                    self.account_children[a] += [account[1]]
                except KeyError:
                    self.account_children[a] = [account[1]]
                self.make_accounts(its, account[1])

    def update_balances(self, *args):
        store, path, iterator = args
        color = "black"
        balance = self.get_balance(store[path][1], True)
        account_type = self.account_types[store[path][1]]
        if account_type in [1, 2]:
            color = "blue"
        elif account_type in [3, 4, 5]:
            color = "green"

        if balance < 0:
            color = "red"

        store[path][3] = "Ush" + str(thousand_separator(balance))
        store[path][4] = color

    def edit_data(self, widget, row, value):
        path, column = self.tree.get_cursor()
        header = column.get_title().lower()
        columns = [c for c in self.tree.get_columns() if c.get_visible()]
        colnum = columns.index(column) + 1
        name = self.account_list[path][colnum]
        ids = None
        try:
            ids = self.account_codes[name]
        except KeyError:
            pass
        tree_iter = self.account_list.get_iter(row)
        self.account_list.set_value(tree_iter, colnum, value)

        if ids:
            self.database.hupdate("accounts", "{0}='{1}'".format(header, value), "code={0}".format(ids))
        else:
            pass

    def fetch_data(self, *args):
        date_one = self.start_date.get_date()
        date_two = self.stop_date.get_date()
        self.date_range = "date>='{0}' AND date<='{1}'".format(date_one, date_two)
        self.balance = self.database.hselect("account_id, debit, credit", "transactions",
                                             "WHERE {0} AND branchid ={1}".format(self.date_range,
                                                                                  self.branch_no), "")
        self.account_list.foreach(self.update_balances)
        imb = self.get_imbalance()

        if imb:
            if imb > 0:
                self.account_list.append(None, ["document-new", "Imbalance", "Assets or Expenses",
                                                thousand_separator(imb), "red"])
            elif imb < 0:
                self.account_list.append(None, ["document-new", "Imbalance",
                                                "Incomes/Equity/Liablities",
                                                thousand_separator(imb), "red"])
        else:
            pass

    def get_imbalance(self):
        data = self.database.hselect("*", "transactions",
                                     "WHERE branchid={0} AND {1}".format(self.branch_no,
                                                                         self.date_range), "")
        right = 0
        left = 0
        for d in data:
            if self.code_types[d[2]] in [1, 2]:
                right += d[7] - d[8]
            elif self.code_types[d[2]] in [3, 4, 5]:
                left += d[8] - d[7]

        if right == left:
            return
        else:
            return right - left

    def get_balance(self, account, recurse=True):
        account_type = self.account_types[account]
        account_code = self.account_codes[account]
        balance = sum([n[1] - n[2] for n in self.balance if n[0] == account_code])
        if account_type in [1, 2]:
            pass
        elif account_type in [3, 4, 5]:
            balance *= -1
        try:
            if recurse:
                balance += sum(self.get_balance(acc, recurse=recurse) for acc in self.account_children[account])
        except KeyError:
            pass

        return balance
