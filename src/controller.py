#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.dips import *
from src.inventory import *
from src.libaccounting import accounting
from src.notebook import NoteBook
from src.settings import Settings
from src.utils import calculator

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ControllerWindow(Gtk.ApplicationWindow):
    date_range = None

    def __init__(self, branch_id, y, *args, **kwargs):
        super(ControllerWindow, self).__init__(*args, **kwargs)
        self.definitions = Definitions()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.maximize()
        self.notebook = NoteBook(branch_id, y)
        self.set_border_width(10)
        self.menubar = Gtk.MenuBar()
        self.file = Gtk.MenuItem("File")
        self.file_menu = Gtk.Menu()
        self.print = Gtk.MenuItem("Print")
        self.file_menu.append(self.print)
        self.page = Gtk.MenuItem("Page Setup")
        self.file_menu.append(self.page)
        self.backup = Gtk.MenuItem("Backup Database")
        self.file_menu.append(self.backup)
        self.file.set_submenu(self.file_menu)
        self.menubar.append(self.file)

        self.inventory_menu = Gtk.Menu()
        self.inventory = Gtk.MenuItem("Inventory")
        self.inventory.set_submenu(self.inventory_menu)
        self.purchase = Gtk.MenuItem("Purchases")
        self.purchase.connect("activate", self.top_menu_caller, branch_id, "purchase")
        self.add_inventory_item = Gtk.MenuItem("Add Inventory")
        self.add_inventory_item.connect("activate", self.top_menu_caller, branch_id, "add_item")
        self.inventory_menu.append(self.add_inventory_item)
        self.inventory_menu.append(self.purchase)
        self.menubar.append(self.inventory)

        self.reports_menu = Gtk.Menu()
        self.reports_menu_d = Gtk.MenuItem("Reports")
        self.reports_menu_d.set_submenu(self.reports_menu)
        cash = Gtk.MenuItem("CashBook")
        cash.connect("activate", self.top_menu_caller, branch_id, "cash")
        trial_balance = Gtk.MenuItem("Trial Balance")
        trial_balance.connect("activate", self.top_menu_caller, branch_id, "trial")
        self.reports_menu.append(cash)
        self.reports_menu.append(trial_balance)
        self.reports_menu.append(Gtk.MenuItem("Trading Profit and Loss"))
        self.reports_menu.append(Gtk.MenuItem("Balance sheet"))
        self.menubar.append(self.reports_menu_d)

        self.stock = Gtk.MenuItem("Stock")
        self.stock_menu = Gtk.Menu()
        self.stock.set_submenu(self.stock_menu)
        self.dips = Gtk.MenuItem("Dips")
        self.stock_menu.append(self.dips)
        self.dips.connect("activate", self.top_menu_caller, branch_id, "dips")
        self.menubar.append(self.stock)

        self.settings_button = Gtk.MenuItem("Settings")
        self.settings_button.set_use_underline(True)
        self.settings_button.connect("activate", self.top_menu_caller, branch_id, "settings")
        self.menubar.append(self.settings_button)

        self.utilities = Gtk.MenuItem("Utilities")
        self.utilities.connect("activate", self.top_menu_caller, branch_id, "calc")
        self.menubar.append(self.utilities)
        self.add(self.box)
        self.box.pack_start(self.menubar, False, False, 0)
        self.box.pack_start(self.notebook, True, True, 0)

    def top_menu_caller(self, widget, branch_id, name):
        if name == "cash":
            cash = accounting.ThreeColumn(branch_id, self.notebook.accounts, self)
            cash.show_all()
        if name == "trial":
            cash = accounting.TrialBalance(branch_id, self.notebook.accounts, self)
            cash.show_all()
        if name == "calc":
            calculator.Calc("Calculator", self)

        if name == "settings":
            Settings(branch_id,
                     self.definitions.get_date(), "Settings", self, Gtk.DialogFlags.MODAL,
                     (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                      Gtk.STOCK_OK, Gtk.ResponseType.OK))

        if name == "purchase":
            Purchases(branch_id,
                      self.notebook.sales, "Purchases", self, Gtk.DialogFlags.MODAL,
                      (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                       Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        if name == "dips":
            FuelDips(branch_id, self.definitions.get_date(), "Fuel Dips", self,
                     Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        if name == "add_item":
            Item(branch_id, "Add item", self, Gtk.DialogFlags.MODAL,
                 (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                  Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
