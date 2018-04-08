#!/usr/bin/python3
# -*- coding: utf-8 -*-

from double_entry import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Accounts(Gtk.ScrolledWindow):
    def __init__(self, branch_id, *args, **kwargs):
        super(Accounts, self).__init__(*args, **kwargs)
        self.database = DataBase("julaw.db")
        self.branch_no = branch_id
        self.date_range = None
        self.start_date = Gtk.Entry()
        self.start_button = Gtk.Button(label=".")
        self.start_button.connect("clicked", self.date_popup, 1)
        self.stop_button = Gtk.Button(label=".")
        self.stop_button.connect("clicked", self.date_popup, 2)

        self.calender = Gtk.Calendar()
        year, month, day = self.calender.get_date()
        self.stop_date = Gtk.Entry()
        self.start_date.set_text(make_date(year, month, day))
        self.stop_date.set_text(make_date(year, month, day))
        self.start_date.set_has_frame(False)
        self.stop_date.set_has_frame(False)

        self.fetch = Gtk.Button(label="Fetch Data")
        self.fetch.connect("clicked", self.fetch_data)
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.set_margin_top(20)
        self.hbox.set_margin_bottom(10)
        self.hbox.pack_start(Gtk.Label("Start Date"), True, False, 0)
        self.hbox.pack_start(self.start_date, False, True, 0)
        self.hbox.pack_start(self.start_button, False, False, 0)
        self.hbox.pack_start(Gtk.Label("Stop Date"), True, False, 0)
        self.hbox.pack_start(self.stop_date, False, True, 0)
        self.hbox.pack_start(self.stop_button, False, False, 0)
        self.hbox.pack_start(self.fetch, True, False, 0)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.pack_start(self.hbox, False, True, 0)

        self.account_list = Gtk.TreeStore(str, str, str, str, str)
        self.tree = Gtk.TreeView.new_with_model(self.account_list)
        renderer = Gtk.CellRendererText()
        render_pix = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("Account Name")
        renderer.set_fixed_size(400, 25)
        column.pack_start(render_pix, False)
        column.add_attribute(render_pix, 'icon_name', 0)
        column.pack_end(renderer, False)
        column.add_attribute(renderer, 'text', 1)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(400, 25)
        column = Gtk.TreeViewColumn("Description", renderer, text=2)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_fixed_size(400, 25)
        column = Gtk.TreeViewColumn("Balance(UGX)", renderer, text=3, foreground=4)
        self.tree.append_column(column)

        self.scrollable_tree_list = Gtk.ScrolledWindow()
        self.scrollable_tree_list.connect("button-press-event", self.right_clicked)

        self.scrollable_tree_list.add(self.tree)
        self.tree.connect("row-activated", self.menu_caller)
        self.tree.connect("button-press-event", self.right_clicked)

        self.box.pack_start(self.scrollable_tree_list, True, True, 0)
        self.add(self.box)
        self.connect("destroy", Gtk.main_quit)
        self.fetch_data("button")
        self.show_all()

    def menu_caller(self, widget, row, col):
        model = widget.get_model()
        name = model[row][1]
        DoubleEntry(self.branch_no,
                    self.date_range,
                    name, self.get_ancestor(Gtk.ApplicationWindow), Gtk.DialogFlags.MODAL,
                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                     Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        self.account_list.clear()
        self.fetch_data("button")

    def right_clicked(self, widget, event):
        category = None
        if event.button == 3:
            pop = Gtk.Menu.new()
            model = widget.get_model()
            try:
                row, column, posx, posy = widget.get_path_at_pos(int(event.x), int(event.y))
                rows = model[row][1]
            except:
                rows = "New TopLevel Account"
            try:
                category = self.database.hselect("account_type", "accounts",
                                                 "WHERE name='{0}'".format(rows), "")[0][0]
            except IndexError:
                pass
            add_account = Gtk.MenuItem("Add " + rows)
            add_account.connect("activate", self.account_methods, "add", rows, category)
            pop.insert(add_account, 0)
            remove_account = Gtk.MenuItem("Remove " + rows)
            pop.insert(remove_account, 1)

            remove_account.connect("activate", self.account_methods, "remove", rows, category)
            pop.popup(None, None, None, None, event.button, Gtk.get_current_event_time())
            pop.show_all()

    def account_methods(self, widget, method, row, category):
        row = row.replace(" ", "")
        if method == "remove":
            try:
                self.database.hdelete("accounts", "name='{0}'".format(row))
                self.database.hdelete(row, "branchid={0}".format(self.branch_no))
            except:
                pass
            self.account_list.clear()
            self.accounts(None, "NewTopLevelAccount")
        elif method == "add":
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

            if category == "Assets":
                button1.set_active(0)
            elif category == "Expenses":
                button2.set_active(1)
            elif category == "Incomes":
                button3.set_active(2)
            elif category == "Liabilities":
                button4.set_active(3)
            elif category == "Equity":
                button5.set_active(4)
            else:
                button1.set_active(0)

            desc.set_placeholder_text("description")
            dialog = Gtk.Dialog("Enter Account", self.get_ancestor(Gtk.ApplicationWindow),
                                Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK,
                                                        Gtk.ResponseType.OK,
                                                        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

            box = dialog.get_content_area()

            dialog.set_default_size(300, 300)
            dialog.set_border_width(50)
            box.pack_start(Gtk.Label("Account Name"), True, False, 0)
            box.pack_start(subac, True, False, 1)
            box.pack_start(Gtk.Label("Account Description"), True, False, 0)
            box.pack_start(desc, True, False, 1)
            box.pack_start(Gtk.Label("Account Type"), True, False, 0)
            box.pack_start(button1, False, False, 0)
            box.pack_start(button2, False, False, 0)
            box.pack_start(button3, False, False, 0)
            box.pack_start(button4, False, False, 0)
            box.pack_start(button5, False, False, 0)
            box.pack_start(button6, False, False, 0)
            box.pack_start(Gtk.Label("Account Subcategory"), True, False, 0)
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

                self.database.hinsert("accounts", "branchid, level, name, description, account_type",
                                      self.branch_no, row, subaccount, description, top_account)
                if row == "NewTopLevelAccount":
                    pass
                else:
                    self.database.hcreate(row, "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                                               "'date' DATE NOT NULL, "
                                               "'branchid' INTEGER,'uuid' TEXT,'transfered' TEXT,"
                                               "'details' TEXT,'debit' REAL,"
                                               "'credit' REAL")
                self.database.hcreate(subaccount, "'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                                                  "'date' DATE NOT NULL, " +
                                      "'branchid' INTEGER, 'uuid' TEXT, 'transfered' TEXT,"
                                      " 'details' TEXT, 'folio' TEXT, 'debit' REAL,'credit' REAL")
                self.database.insert_trigger(subaccount, row, account_type)

            elif response == Gtk.ResponseType.CANCEL:
                print("canceled")
            self.account_list.clear()
            self.accounts(None, "NewTopLevelAccount")
            dialog.close()

    def accounts(self, t, a):
        accounts = self.database.hselect("name, description, account_type", "accounts",
                                         "WHERE level='{0}'".format(a), "")
        for account in accounts:
            try:
                if account[2] in ["Assets", "Expenses"]:
                    balance = self.database.hselect("SUM(debit-credit)", account[0],
                                                    "WHERE {0} AND branchid ={1}".format(
                                                        self.date_range,
                                                        self.branch_no), "")[0][0]

                    its = self.account_list.append(t, ["document-new", account[0], account[1],
                                                       thousand_separator(balance), "blue"])
                elif account[2] in ["Incomes", "Liabilities", "Equity"]:
                    balance = self.database.hselect("SUM(credit-debit)", account[0],
                                                    "WHERE {0} AND branchid ={1}".format(
                                                        self.date_range,
                                                        self.branch_no), "")[0][0]

                    its = self.account_list.append(t, ["document-new", account[0], account[1],
                                                       thousand_separator(balance), "green"])

            except:
                its = self.account_list.append(t, ["document-new", account[0], account[1],
                                                   "0", None])
            self.accounts(its, account[0])

    def fetch_data(self, widget):
        self.account_list.clear()

        date_one = self.start_date.get_text()
        date_two = self.stop_date.get_text()
        self.date_range = "date>='{0}' AND date<='{1}'".format(date_one, date_two)
        self.accounts(None, "NewTopLevelAccount")

        imb = self.get_imbalance()
        if not imb:
            pass
        else:
            if imb > 0:
                self.account_list.append(None, ["document-new", "Imbalance", "Assets or Expenses",
                                                thousand_separator(imb), "blue"])
            elif imb < 0:
                self.account_list.append(None, ["document-new", "Imbalance",
                                                "Incomes/Equity/Liablities",
                                                thousand_separator(imb), "red"])

        self.show_all()

    def date_popup(self, widget, choice):
        dialog = Gtk.Dialog("Calender", self.get_ancestor(Gtk.ApplicationWindow),
                            Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK,
                                                    Gtk.ResponseType.OK,
                                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        box = dialog.get_content_area()
        dialog.set_default_size(300, 300)
        calender = Gtk.Calendar()
        box.pack_start(calender, True, True, 0)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK and choice == 1:
            year, month, date = calender.get_date()
            self.start_date.set_text(make_date(year, month, date))
        elif response == Gtk.ResponseType.OK and choice == 2:
            year, month, date = calender.get_date()
            self.stop_date.set_text(make_date(year, month, date))
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.close()

    def get_imbalance(self):
        try:
            assets = self.database.hselect("SUM(debit-credit)", "Assets",
                                           "WHERE branchid={0} AND {1}".format(self.branch_no,
                                                                               self.date_range), "")[0][0]
        except IndexError:
            assets = 0
        try:
            expenses = self.database.hselect("SUM(debit-credit)", "Expenses",
                                             "WHERE branchid={0} AND {1}".format(self.branch_no,
                                                                                 self.date_range), "")[0][0]
        except IndexError:
            expenses = 0
        try:
            incomes = self.database.hselect("SUM(credit-debit)", "Incomes",
                                            "WHERE branchid={0} AND {1}".format(self.branch_no,
                                                                                self.date_range), "")[0][0]
        except IndexError:
            incomes = 0
        try:
            equity = self.database.hselect("SUM(credit-debit)", "Equity",
                                           "WHERE branchid={0} AND  {1}".format(self.branch_no,
                                                                                self.date_range), "")[0][0]
        except IndexError:
            equity = 0
        try:

            liabilities = self.database.hselect("SUM(credit-debit)", "Liabilities",
                                                "WHERE branchid={0} AND {1}".format(self.branch_no,
                                                                                    self.date_range), "")[0][
                0]
        except IndexError:
            liabilities = 0

        result = accounting_equation(assets, liabilities, equity, incomes, expenses)

        return result
