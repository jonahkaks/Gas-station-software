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


class ControllerWindow:
    date_range = None

    def __init__(self, branch_id, title, y, application):
        self.definitions = Definitions()
        self.notebook = NoteBook(branch_id, y)
        builder = Gtk.Builder()
        builder.add_from_file("../data/controller.glade")
        self.window = builder.get_object("controllerwindow")
        self.window.set_application(application)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = title
        self.window.set_titlebar(hb)
        self.window.maximize()
        self.box = builder.get_object("controllerbox")
        self.print = builder.get_object("print")
        self.print.connect("activate", self.top_menu_caller, branch_id, "print")
        self.printwindow = builder.get_object("printwindow")
        self.box.pack_start(self.notebook, True, True, 0)
        self.window.show_all()

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

        if name == "print":
            response = self.printwindow.run()
            if response == Gtk.ResponseType.OK:
                print("printing")
            elif response == Gtk.ResponseType.CANCEL:
                pass
            self.printwindow.hide()
