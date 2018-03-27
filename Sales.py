#!/usr/bin/python3
# -*- coding: utf-8 -*-
from accounting import *
from calculator import Calc
from dips import *
from double_entry import *
from inventory import *
from settings import Settings

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Sales(Gtk.ApplicationWindow):
    def __init__(self, y, *args, **kwargs):
        super(Sales, self).__init__(*args, **kwargs)
        hcreate("fuel", " `fuelid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                        " `branchid` TEXT, `date` DATE NOT NULL, `product` TEXT,"
                        " `opening_meter` REAL, `closing_meter` REAL, `rtt` REAL ")
        self.maximize()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.calender = Gtk.Calendar()
        self.profit_label = Gtk.Label()
        self.account_list = Gtk.TreeStore(str, str, str, str, str)
        self.totals = []
        self.current_filter_sales = None
        self.account_filter = self.account_list.filter_new()

        self.tree = Gtk.TreeView.new_with_model(self.account_filter)
        renderer = Gtk.CellRendererText()
        render_pix = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("Account Name")
        renderer.set_fixed_size(200, 25)
        column.pack_start(render_pix, False)
        column.add_attribute(render_pix, 'icon_name', 0)
        column.pack_end(renderer, False)
        column.add_attribute(renderer, 'text', 1)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(200, 25)
        column = Gtk.TreeViewColumn("Description", renderer, text=2)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_fixed_size(200, 25)
        column = Gtk.TreeViewColumn("Balance ", renderer, text=3)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_fixed_size(400, 25)
        column = Gtk.TreeViewColumn("Total ", renderer, text=4)
        self.tree.append_column(column)

        self.scrollable_tree_list = Gtk.ScrolledWindow()
        self.scrollable_tree_list.connect("button-press-event", self.right_clicked)

        self.scrollable_tree_list.add(self.tree)
        self.tree.connect("row-activated", self.menu_caller)
        self.tree.connect("button-press-event", self.right_clicked)
        self.opening_meter = []
        self.closing_meter = []
        self.purchases = None
        self.rtt = []
        self.litres = []
        self.price = []
        self.amount = []
        self.expense_total = Gtk.Entry()
        self.product_label = []
        self.product_id = []
        self.button = Gtk.Button()
        self.set_border_width(10)
        self.grid = Gtk.Grid()
        self.grid.set_margin_bottom(20)
        self.grid.set_margin_top(10)
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2.pack_start(self.calender, False, False, 0)
        box2.pack_start(self.grid, False, False, 0)
        box2.pack_start(self.scrollable_tree_list, True, True, 0)
        box2.pack_start(self.button, False, False, 0)
        self.button.add(self.profit_label)
        self.scrolled.add(box2)
        self.add(self.box)

        self.menubar = Gtk.MenuBar()

        self.inventory_menu = Gtk.Menu()
        self.inventory = Gtk.MenuItem("Inventory")
        self.inventory.set_submenu(self.inventory_menu)
        self.purchase = Gtk.MenuItem("Purchases")
        self.purchase.connect("activate", self.top_menu_caller, "purchase")
        self.add_inventory_item = Gtk.MenuItem("Add Inventory")
        self.add_inventory_item.connect("activate", self.top_menu_caller, "add_item")
        self.inventory_menu.append(self.add_inventory_item)
        self.inventory_menu.append(self.purchase)
        self.menubar.append(self.inventory)

        self.reports_menu = Gtk.Menu()
        self.reports_menu_d = Gtk.MenuItem("Reports")
        self.reports_menu_d.set_submenu(self.reports_menu)
        cash = Gtk.MenuItem("CashBook")
        cash.connect("activate", self.top_menu_caller, "cash")
        trial_balance = Gtk.MenuItem("Trial Balance")
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
        self.notebook.set_tab_label_text(self.scrolled, "SalesBook")
        self.box.pack_start(self.menubar, False, False, 0)
        self.box.pack_start(self.notebook, True, True, 0)

        self.calender.connect("day-selected", self.changed_day)
        self.grid.attach(Gtk.Label(label='Product', halign=Gtk.Align.FILL), 0, 2, 2, 1)
        self.grid.attach(Gtk.Label(label='OpeningMeter', halign=Gtk.Align.FILL), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='ClosingMeter', halign=Gtk.Align.FILL), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Rtt', halign=Gtk.Align.FILL), 6, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Litres', halign=Gtk.Align.FILL), 8, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Price', halign=Gtk.Align.FILL), 10, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Amount', halign=Gtk.Align.FILL), 12, 2, 1, 1)

        for n in range(0, len(y), 1):
            self.product_id.append("")
            self.product_label.append(Gtk.Label(label=y[n]))
            self.grid.attach(self.product_label[n], 0, 3 + n, 1, 1)

            self.opening_meter.append(Gtk.Entry())
            self.opening_meter[n].set_has_frame(False)
            self.opening_meter[n].set_placeholder_text('opening meter')
            self.opening_meter[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.opening_meter[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.opening_meter[n], 2, 3 + n, 1, 1)

            self.closing_meter.append(Gtk.Entry())
            self.closing_meter[n].set_has_frame(False)
            self.closing_meter[n].set_placeholder_text('closing meter')
            self.closing_meter[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.closing_meter[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.closing_meter[n], 4, 3 + n, 1, 1)

            self.rtt.append(Gtk.Entry())
            self.rtt[n].set_has_frame(False)
            self.rtt[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.rtt[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.rtt[n], 6, 3 + n, 1, 1)

            self.litres.append(Gtk.Entry())
            self.litres[n].set_has_frame(False)
            self.litres[n].set_placeholder_text('litres')
            self.litres[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.litres[n], 8, 3 + n, 1, 1)

            self.price.append(Gtk.Entry())
            self.price[n].set_has_frame(False)
            self.price[n].set_placeholder_text("price")
            self.price[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.price[n], 10, 3 + n, 1, 1)

            self.amount.append(Gtk.Entry())
            self.amount[n].set_has_frame(False)
            self.amount[n].set_placeholder_text("shs")
            self.grid.attach(self.amount[n], 12, 3 + n, 1, 1)

        self.total_amount = Gtk.Entry()
        self.total_amount.set_has_frame(False)
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
        name = model[row][1]
        DoubleEntry(name, self, Gtk.DialogFlags.MODAL,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.account_list.clear()

        self.accounts(None, "NewTopLevelAccount")

    def right_clicked(self, widget, event):
        if event.button == 3:
            pop = Gtk.Menu.new()
            model = widget.get_model()
            try:
                row, column, posx, posy = widget.get_path_at_pos(int(event.x), int(event.y))
                rows = model[row][1]
            except:
                rows = "New TopLevel Account"
            add_account = Gtk.MenuItem("Add " + rows)
            add_account.connect("activate", self.account_methods, "a", rows)
            pop.insert(add_account, 0)
            remove_account = Gtk.MenuItem("Remove " + rows)
            pop.insert(remove_account, 1)
            remove_account.connect("activate", self.account_methods, "r", rows)
            pop.popup(None, None, None, None, event.button, Gtk.get_current_event_time())
            pop.show_all()

    def account_methods(self, widget, method, row):
        row = row.replace(" ", "")
        if method == "r":
            try:
                hdelete("accounts", "name='{0}'".format(row))
                hdrop(row)
                hdrop()
            except:
                pass
            self.account_list.clear()
            self.accounts(None, "NewTopLevelAccount")
        elif method == "a":
            subac = Gtk.Entry()
            subac.set_placeholder_text("child account")
            store = Gtk.ListStore(str)
            store.append([row])

            combo = Gtk.ComboBox.new_with_model(store)
            renderer_text = Gtk.CellRendererText()
            combo.pack_start(renderer_text, True)
            combo.add_attribute(renderer_text, "text", 0)
            combo.set_active(0)
            desc = Gtk.Entry()
            button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Assets")
            button2 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "Expenses")
            button3 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "Incomes")
            button4 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "Liabilities")
            button5 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "Equity")
            button6 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "None")
            buttons = {button1, button2, button3, button4, button5, button6}

            desc.set_placeholder_text("description")
            dialog = Gtk.Dialog("Enter Account", self,
                                Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK,
                                                        Gtk.ResponseType.OK,
                                                        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

            box = dialog.get_content_area()

            dialog.set_default_size(300, 300)
            dialog.set_border_width(50)
            box.pack_start(subac, True, False, 0)
            box.pack_start(desc, True, False, 0)
            box.pack_start(button1, False, False, 0)
            box.pack_start(button2, False, False, 0)
            box.pack_start(button3, False, False, 0)
            box.pack_start(button4, False, False, 0)
            box.pack_start(button5, False, False, 0)
            box.pack_start(button6, False, False, 0)
            box.pack_start(combo, True, False, 0)

            dialog.show_all()

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                subaccount = subac.get_text().replace(" ", "")
                description = desc.get_text()
                model = combo.get_model()
                tree_iter = combo.get_active_iter()
                account_type = model[tree_iter][0]
                top_account = None

                for button in buttons:
                    if button.get_active():
                        top_account = button.get_label()

                hinsert("accounts", "branchid, level, name, description, account_type",
                        branch_id[0], row, subaccount, description, top_account)
                if row is not "NewTopLevelAccount":
                    hcreate(row, "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'date' DATE NOT NULL, " +
                            "'branchid' INTEGER,'uuid' TEXT,'details' TEXT,'debit' REAL,'credit' REAL")
                hcreate(subaccount, "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'date' DATE NOT NULL, " +
                        "'branchid' INTEGER, 'uuid' TEXT,'details' TEXT, 'debit' REAL,'credit' REAL")
                insert_trigger(subaccount, row, account_type)

            elif response == Gtk.ResponseType.CANCEL:
                print("canceled")
            self.account_list.clear()
            self.accounts(None, "NewTopLevelAccount")
            dialog.close()

    def accounts(self, t, a):
        accounts = hselect("name, description", "accounts",
                           "WHERE level='{0}'".format(a), "")
        for account in accounts:
            try:
                balance = hselect("SUM(debit-credit)", account[0],
                                  "WHERE date='{0}' AND branchid ={1}".format(sales_date[0],
                                                                              branch_id[0]), "")[0][0]

                its = self.account_list.append(t, ["document-new", account[0], account[1],
                                                   thousand_separator(balance), "0"])
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

        if name == "purchase":
            Purchases("Purchases", self, Gtk.DialogFlags.MODAL,
                      (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                       Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        if name == "dips":
            FuelDips("Fuel Dips", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                                Gtk.STOCK_OK, Gtk.ResponseType.OK))
        if name == "add_item":
            Item("Add item", self, Gtk.DialogFlags.MODAL,
                 (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                  Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

    def changed_day(self, widget):
        year, month, day = self.calender.get_date()
        real_insert(sales_date, 0, make_date(year, month, day))
        sales_results = get_data("fuel")
        price.clear()
        prices = []
        cash = get_cash_profit()
        self.profit_label.set_markup("<span color='blue'><b>Cash at hand:</b>{0}       </span>"
                                     "<span color='green'>Gross profit:{1}</span>".format(thousand_separator(cash),
                                                                                          30000))
        try:
            get_price()
            for m in range(0, len(self.product_label), 1):
                b = self.product_label[m].get_label()
                if b[0:3] == "PMS":
                    real_insert(prices, m, price[0])
                elif b[0:3] == "AGO":
                    real_insert(prices, m, price[1])
                elif b[0:3] == "BIK":
                    real_insert(prices, m, price[2])

        except:
            pass

        if len(sales_results) > 0:
            for hs in range(0, len(sales_results), 1):
                real_insert(self.product_id, hs, sales_results[hs][0])
                self.opening_meter[hs].set_text(str(sales_results[hs][4]))
                self.closing_meter[hs].set_text(str(sales_results[hs][5]))
                self.rtt[hs].set_text(str(sales_results[hs][6]))
                self.price[hs].set_text(str(prices[hs]))

        elif len(sales_results) == 0:
            for i in range(0, len(self.opening_meter), 1):
                real_insert(self.product_id, i, "")
                self.opening_meter[i].set_text("")
                self.closing_meter[i].set_text("")
                self.rtt[i].set_text("0.0")
                self.litres[i].set_text("")
                self.amount[i].set_text("")
                try:
                    self.price[i].set_text(str(prices[i]))
                except IndexError:
                    print("okay")
            self.total_amount.set_text("")
        prices.clear()
        self.account_list.clear()
        self.accounts(None, "NewTopLevelAccount")
        self.show_all()

    def subtraction(self, widget, choice):
        try:
            opening_stock = float(self.opening_meter[choice].get_text())
            closing_stock = float(self.closing_meter[choice].get_text())
            rtt = float(self.rtt[choice].get_text())
            result = closing_stock - (opening_stock + rtt)

            self.litres[choice].set_text(locale.format("%05.2f", result, grouping=False))
            price = int(self.price[choice].get_text())

            real_insert(pr, choice, price)

            real_insert(amount_array, choice, result * price)
            self.amount.set_text(str(amount_array[choice]))
            self.total_amount.set_text(str(add_array(amount_array)))


        except:
            pass
