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
            renderer.set_fixed_size(400, 25)
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
        self.button = Gtk.Button()
        self.set_border_width(10)
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2.pack_start(self.calender, False, False, 0)
        box2.pack_start(self.grid, False, True, 0)
        box2.pack_start(self.scrollable_tree_list, True, True, 0)
        box2.pack_start(self.button, False, False, 0)

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
            self.product_label[n].set_size_request(10, 10)
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
            self.grid.attach(self.litres[n], 8, 3 + n, 1, 1)
            self.price.append(Gtk.Entry())
            self.price[n].set_placeholder_text("price")
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
                len(self.rtt[choice].get_text()) and \
                len(self.price[choice].get_text()) > 0:
            result = sales_litres(self.product_id[choice], choice,
                                  self.product_label[choice].get_label(),
                                  self.opening_meter[choice].get_text(),
                                  self.closing_meter[choice].get_text(),
                                  self.rtt[choice].get_text(),
                                  self.price[choice].get_text())
            self.litres[choice].set_text(result[0])
            real_insert(self.product_id, choice, result[1])
            self.amount[choice].set_text(thousand_separator(str(result[2])))
            self.total_amount.set_text(thousand_separator(str(result[3])))
            self.changed_day("button")

    def menu_caller(self, widget, row, col):
        model = widget.get_model()
        name = model[row][0]
        self.account_list.clear()
        DoubleEntry(name, self, Gtk.DialogFlags.MODAL,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.accounts(None, "top")

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
                hdelete("accounts", "name='{0}'".format(row))
                hdrop(row)
                hdrop()
            except:
                pass
            self.accounts(None, "top")
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

            dialog.show_all()

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                subaccount = subac.get_text().replace(",", " ")
                description = desc.get_text().replace(",", " ")
                hinsert("accounts", "branchid, level, name, description", branch_id[0], row,
                        subaccount,
                        description)
                hcreate(row, "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'date' TEXT, " +
                        "'branchid' INTEGER,'uuid' TEXT,'details' TEXT,'debit' REAL,'credit' REAL")
                hcreate(subaccount, "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'date' TEXT, " +
                        "'branchid' INTEGER, 'uuid' TEXT,'details' TEXT, 'debit' REAL,'credit' REAL")
                insert_trigger(subaccount, row)

            elif response == Gtk.ResponseType.CANCEL:
                print("canceled")
            self.accounts(None, "top")
            dialog.close()

    def accounts(self, t, a):
        accounts = hselect("name, description", "accounts",
                           "WHERE level='{0}'".format(a), "")
        for account in accounts:
            try:
                its = self.account_list.append(t, [account[0], account[1],
                                                   "{0}".format(
                                                       thousand_separator(hselect("SUM(debit-credit)", account[0],
                                                                                  "WHERE date='{0}'".format(
                                                                                      sales_date[0]),
                                                                                  "AND branchid = '{0}'".format(
                                                                                      branch_id[0]))[0][0]))])
            except:
                its = self.account_list.append(t, [account[0], account[1], "0"])
            self.accounts(its, account[0])

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
            self.changed_day("button")

        if name == "fuel":
            FuelPurchase("Fuel Purchase", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
            self.changed_day("button")

        if name == "dips":
            FuelDips("Fuel Dips", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                                Gtk.STOCK_OK, Gtk.ResponseType.OK))

    def changed_day(self, widget):
        year, month, day = self.calender.get_date()
        real_insert(sales_date, 0, make_date(year, month, day))
        sales_results = get_data("fuel")
        price = []
        try:
            prices = get_price()[0]
            for m in range(0, len(self.product_label), 1):
                b = self.product_label[m].get_label()

                if b[0:3] == "PMS":
                    real_insert(price, m, prices[0])
                elif b[0:3] == "AGO":
                    real_insert(price, m, prices[1])
                elif b[0:3] == "BIK":
                    real_insert(price, m, prices[2])
        except IndexError:
            pass

        if len(sales_results) > 0:
            for hs in range(0, len(sales_results), 1):
                real_insert(self.product_id, hs, sales_results[hs][0])
                self.opening_meter[hs].set_text(str(sales_results[hs][4]))
                self.closing_meter[hs].set_text(str(sales_results[hs][5]))
                self.rtt[hs].set_text(str(sales_results[hs][6]))
                self.price[hs].set_text(str(price[hs]))

        elif len(sales_results) == 0:
            for i in range(0, len(self.opening_meter), 1):
                real_insert(self.product_id, i, "")
                self.opening_meter[i].set_text("")
                self.closing_meter[i].set_text("")
                self.rtt[i].set_text("0.0")
                self.litres[i].set_text("")
                try:
                    self.price[i].set_text(str(price[i]))
                except IndexError:
                    pass
        self.account_list.clear()
        self.accounts(None, "top")
        self.show_all()

    def subtraction(self, widget, choice):
        try:
            opening_stock = float(self.opening_meter[choice].get_text())
            closing_stock = float(self.closing_meter[choice].get_text())
            rtt = float(self.rtt[choice].get_text())
            result = str(closing_stock - (opening_stock + rtt))
            self.litres[choice].set_text(result)
            price = int(self.price[choice].get_text())
            litres = float(self.litres[choice].get_text())
            real_insert(pr, choice, price)

            real_insert(amount_array, choice, litres * price)
            self.amount.set_text(str(amount_array[choice]))
            self.total_amount.set_text(str(add_array(amount_array, choice)))

        except:
            pass
