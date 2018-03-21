#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

gi.require_version('Gtk', '3.0')
from definitions import *


class ThreeColumn(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        sales_details = cashbook()
        self.box = self.get_content_area()
        self.set_default_size(900, 600)
        self.horizontal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.horizontal.pack_start(Gtk.Label("Dr"), False, False, 0)
        self.horizontal.pack_end(Gtk.Label("Cr"), False, False, 0)
        self.box.pack_start(self.horizontal, False, False, 0)

        self.sales_liststore = Gtk.ListStore(str, str, str, int, int, str, str, str, int, int)
        for i in range(0, len(sales_details), 1):
            self.sales_liststore.append(sales_details[i])
        self.current_filter_sales = None
        self.sales_filter = self.sales_liststore.filter_new()
        self.sales_filter.set_visible_func(self.sales_filter_func)

        self.treeview = Gtk.TreeView.new_with_model(self.sales_filter)
        for i, column_title in enumerate(["Date", "Details", "Folio", "Cash", "Bank",
                                          "Date", "Details", "Folio", "Cash", "Bank"]):
            renderer = Gtk.CellRendererText()
            renderer.set_fixed_size(83, 20)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.box.pack_start(self.scrollable_treelist, True, True, 0)
        self.scrollable_treelist.add(self.treeview)

    def sales_filter_func(self, model, iter, data):
        if self.current_filter_sales is None or self.current_filter_sales == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_sales


class TrialBalance(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        trial_details = trial()
        self.debit = []
        self.credit = []

        self.box = self.get_content_area()
        self.set_default_size(700, 600)
        self.trial_store = Gtk.ListStore(str, int, int)
        for t in range(0, len(trial_details), 1):
            self.trial_store.append(trial_details[t])
            self.debit.append(trial_details[t][1])
            self.credit.append(trial_details[t][2])
        self.button = Gtk.Button(label="Total debit:{0}   "
                                       " Total Credit:{1}".format(add_array(self.debit, -1),
                                                                  add_array(self.credit, -1)))


        self.current_filter_trial = None
        self.trial_filter = self.trial_store.filter_new()

        self.treeview = Gtk.TreeView.new_with_model(self.trial_filter)
        for i, column_title in enumerate(["Account Name", "Dr", "Cr"]):
            renderer = Gtk.CellRendererText()
            renderer.set_fixed_size(200, 22)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.box.pack_start(self.scrollable_treelist, True, True, 0)
        self.box.pack_start(self.button, False, False, 0)
        self.scrollable_treelist.add(self.treeview)
