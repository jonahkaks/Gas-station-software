#!/usr/bin/python3
# -*- coding: utf-8 -*-

from accounting import *
from calculator import Calc
from dips import *
from double_entry import *
from purchases import *
from settings import Settings

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Sales(Gtk.ApplicationWindow):
    def __init__(self, y, *args, **kwargs):
        super(Sales, self).__init__(*args, **kwargs)
        self.maximize()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.calender = Gtk.Calendar()
        self.account_list = Gtk.TreeStore(str, str, str)
        self.totals = []
        self.current_filter_sales = None
        self.account_filter = self.account_list.filter_new()

        self.tree = Gtk.TreeView.new_with_model(self.account_filter)
        for i, column_title in enumerate(["Account Name", "Description", "Total"]):
            renderer = Gtk.CellRendererText()
            renderer.set_fixed_size(300, 20)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tree.append_column(column)
        self.scrollable_tree_list = Gtk.ScrolledWindow()
        self.scrollable_tree_list.set_vexpand(True)
        self.scrollable_tree_list.set_hexpand(True)
        self.scrollable_tree_list.add(self.tree)
        self.tree.connect("row-activated", self.menu_caller)
        self.tree.connect("button-press-event", self.right_clicked)
        self.opening_meter = []
        self.closing_meter = []
        self.rtt = []
        self.litres = []
        self.price = []
        self.amount = []
        self.expense_total = Gtk.Entry()
        self.product_label = []
        self.product_id = []
        self.set_border_width(10)
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.grid.set_hexpand(True)
        box2.pack_start(self.calender, False, False, 0)
        box2.pack_start(self.grid, False, False, 0)
        box2.pack_start(self.scrollable_tree_list, True, True, 0)
        self.scrolled.add(box2)
        self.add(self.box)

        self.menubar = Gtk.MenuBar()

        self.file_menu_d = Gtk.MenuItem("Purchases")
        self.file_menu = Gtk.Menu()
        self.file_menu_d.set_submenu(self.file_menu)
        self.fuel = Gtk.MenuItem("Fuel")
        self.fuel.connect("activate", self.top_menu_caller, "fuel")
        self.file_menu.append(self.fuel)
        self.lubricants = Gtk.MenuItem("Lubricants")
        self.file_menu.append(self.lubricants)
        self.menubar.append(self.file_menu_d)

        self.reports_menu = Gtk.Menu()
        self.reports_menu_d = Gtk.MenuItem("Reports")
        self.reports_menu_d.set_submenu(self.reports_menu)
        cash = Gtk.MenuItem("CashBook")
        cash.connect("activate", self.menu_caller, "cash")
        trial_balance = Gtk.MenuItem("TrialBalance")
        trial_balance.connect("activate", self.top_menu_caller, "trial")
        self.reports_menu.append(cash)
        self.reports_menu.append(trial_balance)
        self.reports_menu.append(Gtk.MenuItem("Trading Profit and Loss"))
        self.reports_menu.append(Gtk.MenuItem("Balance sheet"))
        self.menubar.append(self.reports_menu_d)

        self.dips = Gtk.MenuItem("Dips")
        self.dips.connect("activate", self.top_menu_caller, "dips")
        self.menubar.append(self.dips)

        self.utilities = Gtk.MenuItem("Utilities")
        self.utilities.connect("activate", self.top_menu_caller, "calc")
        self.menubar.append(self.utilities)

        self.settings_button = Gtk.MenuItem("Settings")
        self.settings_button.set_use_underline(True)
        self.settings_button.connect("activate", self.top_menu_caller, "settings")
        self.menubar.append(self.settings_button)
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        self.notebook.append_page(self.scrolled)
        self.notebook.set_tab_label_text(self.scrolled, "DayBook")
        self.box.pack_start(self.menubar, False, False, 0)
        self.box.pack_start(self.notebook, True, True, 0)

        self.calender.connect("day-selected", self.changed_day)
        self.grid.attach(Gtk.Label('Product'), 0, 2, 2, 1)
        self.grid.attach(Gtk.Label('OpeningMeter'), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label('ClosingMeter'), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label('Rtt'), 6, 2, 1, 1)
        self.grid.attach(Gtk.Label('Litres'), 8, 2, 1, 1)
        self.grid.attach(Gtk.Label('Price'), 10, 2, 1, 1)
        self.grid.attach(Gtk.Label('Amount'), 12, 2, 1, 1)

        for n in range(0, len(y), 1):
            self.product_id.append("")
            self.product_label.append(Gtk.Button(label=y[n]))
            self.grid.attach(self.product_label[n], 0, 3 + n, 2, 1)

            self.opening_meter.append(Gtk.Entry())
            self.opening_meter[n].set_placeholder_text('opening meter')
            self.opening_meter[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.opening_meter[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.opening_meter[n], 2, 3 + n, 1, 1)

            self.closing_meter.append(Gtk.Entry())
            self.closing_meter[n].set_placeholder_text('closing meter')
            self.closing_meter[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.closing_meter[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.closing_meter[n], 4, 3 + n, 1, 1)

            self.rtt.append(Gtk.Entry())
            self.rtt[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.rtt[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.rtt[n], 6, 3 + n, 1, 1)

            self.litres.append(Gtk.Entry())
            self.litres[n].set_placeholder_text('litres')
            self.litres[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.litres[n], 8, 3 + n, 1, 1)
            self.price.append(Gtk.Entry())
            self.price[n].set_placeholder_text("price")
            self.price[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.price[n], 10, 3 + n, 1, 1)

            self.amount.append(Gtk.Entry())
            self.amount[n].set_placeholder_text("shs")
            self.grid.attach(self.amount[n], 12, 3 + n, 1, 1)

        self.total_amount = Gtk.Entry()
        self.total_amount.set_placeholder_text("total")
        self.grid.attach(self.total_amount, 12, len(y) + 4, 1, 1)

        self.changed_day("calender")

    def sales_litres_caller(self, event, widget, choice):

        if len(self.product_label[choice].get_label()) and len(
                self.opening_meter[choice].get_text()) and \
                len(self.closing_meter[choice].get_text()) and \
                len(self.rtt[choice].get_text()) > 0:
            result = sales_litres(self.product_id[choice],
                                  self.product_label[choice].get_label(),
                                  self.opening_meter[choice].get_text(),
                                  self.closing_meter[choice].get_text(),
                                  self.rtt[choice].get_text())
            self.litres[choice].set_text(result[0])
            real_insert(self.product_id, choice, result[1])

    def sales_shs_caller(self, widget, choice):
        if len(self.litres[choice].get_text()) and len(
                self.price[choice].get_text()) > 0:
            result = sales_shs(choice, self.litres[choice].get_text(),
                               self.price[choice].get_text())
            self.amount[choice].set_text(thousand_separator(str(result[0])))
            self.total_amount.set_text(thousand_separator(str(result[1])))

    def menu_caller(self, widget, row, col):
        model = widget.get_model()
        name = model[row][0]
        self.account_list.clear()
        DoubleEntry(name, self, Gtk.DialogFlags.MODAL,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.accounts()

    def right_clicked(self, widget, event):
        if event.button == 3:
            pop = Gtk.Menu.new()
            model = widget.get_model()
            row, column, posx, posy = widget.get_path_at_pos(int(event.x), int(event.y))
            add_account = Gtk.MenuItem("Add " + model[row][0])
            add_account.connect("activate", self.account_methods, "a", model[row][0])
            pop.insert(add_account, 0)
            remove_account = Gtk.MenuItem("Remove " + model[row][0])
            pop.insert(remove_account, 1)
            remove_account.connect("activate", self.account_methods, "r", model[row][0])
            pop.popup(None, None, None, None, event.button, Gtk.get_current_event_time())
            pop.show_all()

    def account_methods(self, widget, method, row):
        self.account_list.clear()
        if method == "r":
            try:
                hdelete("subaccounts", "name='{0}'".format(row))
                hdrop(row)
                hdrop(hselect("name", "accounts", "WHERE id={0}".format(hselect("account_id",
                                                                                "subaccounts",
                                                                                "WHERE name='{0}".format(row),
                                                                                "")[0][0]), "")[0][0])
            except sqlite3.OperationalError:
                hdelete("sub_subaccounts", "name='{0}'".format(row))
                print("row")
            self.accounts()
        elif method == "a":
            subac = Gtk.Entry()
            subac.set_placeholder_text("child account")
            desc = Gtk.Entry()
            desc.set_placeholder_text("description")
            dialog = Gtk.Dialog("Enter field", self,
                                Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK,
                                                        Gtk.ResponseType.OK,
                                                        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

            box = dialog.get_content_area()

            dialog.set_default_size(300, 300)
            dialog.set_border_width(50)
            box.pack_start(subac, True, True, 0)
            box.pack_start(desc, True, True, 0)
            account = hselect("name", "accounts", "", "")
            subaccount = hselect("name", "subaccounts", "", "")
            accounts = []
            subaccounts = []
            for b in range(0, len(account), 1):
                accounts.append(account[b][0])
            for b in range(0, len(subaccount), 1):
                subaccounts.append(subaccount[b][0])

            dialog.show_all()

            response = dialog.run()
            if response == Gtk.ResponseType.OK and row in accounts:
                category = hselect("id", "accounts",
                                   "WHERE name='{0}'".format(row), "")[0][0]
                hinsert("subaccounts", "branchid, account_id, name, description", branch_id[0], category,
                        subac.get_text(),
                        desc.get_text())
                hcreate(row, "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'date' TEXT, " +
                        "'branchid' INTEGER,'details' TEXT,'debit' REAL,'credit' REAL")
                hcreate(subac.get_text(), "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'date' TEXT, " +
                        "'branchid' INTEGER,'details' TEXT, 'debit' REAL,'credit' REAL")
                insert_trigger(subac.get_text(), row)

                self.accounts()
            elif response == Gtk.ResponseType.OK and row in subaccounts:
                category = hselect("id", "subaccounts",
                                   "WHERE name='{0}'".format(row), "")[0][0]
                hinsert("sub_subaccounts", "branchid,subaccount_id, name, description",
                        branch_id[0], category, subac.get_text(),
                        desc.get_text())
                hcreate(subac.get_text(), "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'date' TEXT, " +
                        "'branchid' INTEGER,'details' TEXT, 'debit' REAL,'credit' REAL")
                self.accounts()
                insert_trigger(subac.get_text(), row)

            elif response == Gtk.ResponseType.CANCEL:
                print("canceled")
                self.accounts()
            dialog.close()

    def accounts(self):
        account = hselect("id, name", "accounts", "", "")
        for ids, account in account:
            try:
                it = self.account_list.append(None,
                                              [account, account,
                                               "{0}".format(thousand_separator(hselect("SUM(debit-credit)", account,
                                                                                       "WHERE date='{0}'".format(
                                                                                           sales_date[0]),
                                                                                       "AND branchid = '{0}'".format(
                                                                                           branch_id[0]))[0][0]))])
                n = hselect("id, name, description", "subaccounts", "WHERE account_id={0}".format(ids),
                            "AND branchid={0}".format(branch_id[0]))
                arr = []
                for i in range(0, len(n), 1):
                    total = hselect("SUM(debit-credit)", n[i][1], "WHERE date='{0}'".format(sales_date[0]),
                                    "AND branchid = '{0}'".format(branch_id[0]))
                    arr.append((n[i][0], n[i][1], n[i][2], thousand_separator(str(total[0][0]))))

                for i in range(0, len(arr), 1):
                    its = self.account_list.append(it, arr[i][1:])
                    k = hselect("name, description", "sub_subaccounts",
                                "WHERE subaccount_id={0}".format(arr[i][0]),
                                "AND branchid={0}".format(branch_id[0]))
                    sub_accounts = []
                    for j in range(0, len(k), 1):
                        tot = hselect("SUM(debit-credit)", k[j][0], "WHERE date='{0}'".format(sales_date[0]),
                                      "AND branchid = {0}".format(branch_id[0]))
                        sub_accounts.append((k[j][0], k[j][1], thousand_separator(str(tot[0][0]))))
                    for n in range(0, len(sub_accounts), 1):
                        self.account_list.append(its, sub_accounts[n])
            except:
                it = self.account_list.append(None, [account, account, '0'])

    def top_menu_caller(self, widget, name):
        if name == "cash":
            cash = ThreeColumn("Cash Book", self)
            cash.show_all()
        if name == "trial":
            cash = TrialBalance("Trial Balance As At {0}".format(str(sales_date[0])), self)
            cash.show_all()
        if name == "calc":
            Calc("Calculator", self)

        if name == "settings":
            Settings("Settings", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                               Gtk.STOCK_OK, Gtk.ResponseType.OK))

        if name == "fuel":
            FuelPurchase("Fuel Purchase", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                                        Gtk.STOCK_OK, Gtk.ResponseType.OK))

        if name == "dips":
            FuelDips("Fuel Dips", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                                Gtk.STOCK_OK, Gtk.ResponseType.OK))

    def changed_day(self, widget):
        year, month, day = self.calender.get_date()
        real_insert(sales_date, 0, '{0:04d}-{1:02d}-{2:02d}'.format(year, month + 1, day))
        sales_results = get_data("fuel")

        if len(sales_results) > 0:
            for hs in range(0, len(sales_results), 1):
                real_insert(self.product_id, hs, sales_results[hs][0])
                self.opening_meter[hs].set_text(str(sales_results[hs][4]))
                self.closing_meter[hs].set_text(str(sales_results[hs][5]))
                self.rtt[hs].set_text(str(sales_results[hs][6]))

        elif len(sales_results) == 0:
            for i in range(0, len(self.opening_meter), 1):
                real_insert(self.product_id, i, "")
                self.opening_meter[i].set_text("")
                self.closing_meter[i].set_text("")
                self.rtt[i].set_text("0.0")
                self.litres[i].set_text("")
                self.price[i].set_text("")
        self.account_list.clear()
        self.accounts()
        self.show_all()

    def subtraction(self, widget, choice):
        try:
            opening_stock = float(self.opening_meter[choice].get_text())
            closing_stock = float(self.closing_meter[choice].get_text())
            rtt = float(self.rtt[choice].get_text())
            result = str(closing_stock - (opening_stock + rtt))
            self.litres[choice].set_text(result)
        except ValueError:
            pass
