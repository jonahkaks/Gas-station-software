#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from src.definitions import *


class ThreeColumn(Gtk.Dialog):
    def __init__(self, branch_id, accounts, *args):
        Gtk.Dialog.__init__(self, *args)
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        start_date = accounts.start_date.get_text()
        stop_date = accounts.stop_date.get_text()
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "CashBook As At {0}".format(stop_date)
        self.set_titlebar(hb)

        debit, credit = self.definitions.cashbook(start_date, stop_date)

        self.box = self.get_content_area()
        self.set_default_size(1000, 600)
        self.horizontal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.horizontal.pack_start(Gtk.Label("Dr"), False, False, 0)
        self.horizontal.pack_end(Gtk.Label("Cr"), False, False, 0)
        self.box.pack_start(self.horizontal, False, False, 0)
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.debit_list = Gtk.ListStore(str, str, str, str)
        self.credit_list = Gtk.ListStore(str, str, str, str)
        for k, v in enumerate(debit):
            self.debit_list.append(v)
        for k, v in enumerate(credit):
            self.credit_list.append(v)

        self.debit_tree = Gtk.TreeView.new_with_model(self.debit_list)
        for i, column_title in enumerate(["Details", "Folio", "Cash", "Bank"]):
            renderer = Gtk.CellRendererText()
            renderer.set_fixed_size(120, 20)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.debit_tree.append_column(column)
        self.credit_tree = Gtk.TreeView.new_with_model(self.credit_list)
        for i, column_title in enumerate(["Details", "Folio", "Cash", "Bank"]):
            renderer = Gtk.CellRendererText()
            renderer.set_fixed_size(120, 20)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.credit_tree.append_column(column)
        self.hbox.pack_start(self.debit_tree, True, True, 0)
        self.hbox.pack_end(self.credit_tree, True, True, 0)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.box.pack_start(self.scrollable_treelist, True, True, 0)
        self.scrollable_treelist.add(self.hbox)


class TrialBalance(Gtk.Dialog):
    def __init__(self, branch_id, accounts, *args):
        Gtk.Dialog.__init__(self, *args)
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        start_date = accounts.start_date.get_text()
        stop_date = accounts.stop_date.get_text()
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Trial balance As At {0}".format(stop_date)
        self.set_titlebar(hb)
        date = "date>='{0}' AND date<='{1}'".format(start_date, stop_date)
        trial_details = self.definitions.trial(date_range=date)
        print(trial_details)
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
