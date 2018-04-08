#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

from Sales import Sales
from accounts import Accounts

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class NoteBook(Gtk.Notebook):
    def __init__(self, branch_id, y, *args, **kwargs):
        super(NoteBook, self).__init__(*args, **kwargs)
        self.accounts = Accounts(branch_id)
        self.sales = Sales(branch_id, y)
        self.set_tab_pos(Gtk.PositionType.TOP)
        self.append_page(self.sales)
        self.append_page(self.accounts)
        self.set_tab_label_text(self.sales, "Sales")
        self.set_tab_label_text(self.accounts, "Accounts")
