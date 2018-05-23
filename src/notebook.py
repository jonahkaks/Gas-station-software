#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

from src.Sales import Sales
from src.libaccounting import accounts

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class NoteBook(Gtk.Notebook):
    def __init__(self, branch_id, *args, **kwargs):
        super(NoteBook, self).__init__(*args, **kwargs)
        self.accounts = accounts.Accounts(branch_id)
        self.sales = Sales(branch_id)

        self.create_tab(self.sales, "Sales", 0, False)
        self.create_tab(self.accounts, "Accounts", 1)

    def create_tab(self, widget, title, pos, a=True):
        hbox = Gtk.Box(False, 0)
        label = Gtk.Label(title)
        hbox.pack_start(label, True, True, 0)
        close_image = Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        btn = Gtk.Button()
        btn.set_relief(Gtk.ReliefStyle.NONE)
        btn.set_focus_on_click(False)
        if a:
            btn.add(close_image)
        else:
            pass
        hbox.pack_start(btn, False, False, 0)
        hbox.show_all()
        self.insert_page(widget, hbox, pos)
        self.set_tab_reorderable(widget, True)
        btn.connect('clicked', self.on_closetab_button_clicked, widget)

    def on_closetab_button_clicked(self, sender, widget):
        pagenum = self.page_num(widget)
        self.remove_page(pagenum)
