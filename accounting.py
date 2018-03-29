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

        self.sales_list = Gtk.ListStore(str, str, str, str, str, str, str, str)
        for i in range(0, len(sales_details), 1):
            self.sales_list.append([sales_details[i][0], sales_details[i][1],
                                    thousand_separator(sales_details[i][2]),
                                    thousand_separator(sales_details[i][3]),
                                    sales_details[i][4], sales_details[i][5],
                                    thousand_separator(sales_details[i][6]),
                                    thousand_separator(sales_details[i][7])])
        self.current_filter_sales = None
        self.sales_filter = self.sales_list.filter_new()
        self.sales_filter.set_visible_func(self.sales_filter_func)

        self.treeview = Gtk.TreeView.new_with_model(self.sales_filter)
        for i, column_title in enumerate(["Details", "Folio", "Cash", "Bank",
                                          "Details", "Folio", "Cash", "Bank"]):
            renderer = Gtk.CellRendererText()
            renderer.set_fixed_size(100, 20)
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
        self.trial_store = Gtk.ListStore(str, str, str)
        for t in range(0, len(trial_details), 1):
            self.trial_store.append([trial_details[t][0],
                                     thousand_separator(trial_details[t][1]),
                                     thousand_separator(trial_details[t][2])])
            if trial_details[t][1]:
                self.debit.append(eval(trial_details[t][1]))
            elif trial_details[t][2]:
                self.credit.append(eval(trial_details[t][2]))
        total_debit = add_array(self.debit)
        total_credit = add_array(self.credit)
        if total_debit > total_credit:
            difference = total_debit - total_credit
            total_credit = total_credit + difference
            self.trial_store.append(["Imbalance", None,
                                     thousand_separator(difference)])
        elif total_debit < total_credit:
            difference = total_credit - total_debit
            total_debit = total_debit + difference
            self.trial_store.append(["Imbalance",
                                     thousand_separator(difference), None])

        self.button = Gtk.Button(label="Total debit:{0}   "
                                       " Total Credit:{1}".format(thousand_separator(total_debit),
                                                                  thousand_separator(total_credit)))

        self.current_filter_trial = None
        self.trial_filter = self.trial_store.filter_new()

        self.treeview = Gtk.TreeView.new_with_model(self.trial_filter)
        for i, column_title in enumerate(["Account Name", "Dr", "Cr"]):
            renderer = Gtk.CellRendererText()
            renderer.set_fixed_size(250, 22)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.box.pack_start(self.scrollable_treelist, True, True, 0)
        self.box.pack_start(self.button, False, False, 0)
        self.scrollable_treelist.add(self.treeview)
