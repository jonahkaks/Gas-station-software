#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018 jonahk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Calc(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        self.box = self.get_content_area()
        self.store = []
        self.ans = 0
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.answer)
        self.entry.connect("delete-from-cursor", self.empty)
        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_end(self.grid, False, True, 0)
        self.set_default_size(300, 300)
        self.button1 = Gtk.Button(label="1")
        self.button1.set_size_request(100, 10)
        self.button1.connect("clicked", self.get_label)
        self.grid.attach(self.button1, 0, 0, 1, 1)
        self.button2 = Gtk.Button(label="2")
        self.button2.set_size_request(100, 10)
        self.button2.connect("clicked", self.get_label)
        self.grid.attach(self.button2, 2, 0, 1, 1)
        self.button3 = Gtk.Button(label="3")
        self.button3.set_size_request(100, 10)
        self.button3.connect("clicked", self.get_label)
        self.grid.attach(self.button3, 4, 0, 1, 1)
        self.button4 = Gtk.Button(label="4")
        self.button4.connect("clicked", self.get_label)
        self.grid.attach(self.button4, 0, 1, 1, 1)
        self.button5 = Gtk.Button(label="5")
        self.button5.connect("clicked", self.get_label)
        self.grid.attach(self.button5, 2, 1, 1, 1)
        self.button6 = Gtk.Button(label="6")
        self.button6.connect("clicked", self.get_label)
        self.grid.attach(self.button6, 4, 1, 1, 1)
        self.button7 = Gtk.Button(label="7")
        self.button7.connect("clicked", self.get_label)
        self.grid.attach(self.button7, 0, 2, 1, 1)
        self.button8 = Gtk.Button(label="8")
        self.button8.connect("clicked", self.get_label)
        self.grid.attach(self.button8, 2, 2, 1, 1)
        self.button9 = Gtk.Button(label="9")
        self.button9.connect("clicked", self.get_label)
        self.grid.attach(self.button9, 4, 2, 1, 1)
        self.button10 = Gtk.Button(label="0")
        self.button10.connect("clicked", self.get_label)
        self.grid.attach(self.button10, 0, 3, 1, 1)
        self.button11 = Gtk.Button(label="*")
        self.button11.connect("clicked", self.get_label)
        self.grid.attach(self.button11, 2, 3, 1, 1)
        self.button12 = Gtk.Button(label="+")
        self.button12.connect("clicked", self.get_label)
        self.grid.attach(self.button12, 4, 3, 1, 1)
        self.button13 = Gtk.Button(label="/")
        self.button13.connect("clicked", self.get_label)
        self.grid.attach(self.button13, 0, 4, 1, 1)
        self.button14 = Gtk.Button(label="-")
        self.button14.connect("clicked", self.get_label)
        self.grid.attach(self.button14, 2, 4, 1, 1)
        self.button15 = Gtk.Button(label="^")
        self.button15.connect("clicked", self.get_label)
        self.grid.attach(self.button15, 4, 4, 1, 1)
        self.button16 = Gtk.Button(label="%")
        self.button16.connect("clicked", self.get_label)
        self.grid.attach(self.button16, 0, 5, 1, 1)
        self.button17 = Gtk.Button(label="=")
        self.button17.connect("clicked", self.answer)
        self.grid.attach(self.button17, 2, 5, 1, 1)
        self.button18 = Gtk.Button(label="Del")
        self.button18.connect("clicked", self.empty)
        self.grid.attach(self.button18, 4, 5, 1, 1)
        self.show_all()

    def get_label(self, widget):
        self.store.append(widget.get_label())
        statement = ""
        for i in range(0, len(self.store), 1):
            statement += eval(self.store[i])
        self.entry.set_text(statement)

    def answer(self, widget):
        result = self.entry.get_text()
        self.store = []
        try:
            self.ans = str(eval(result))
            self.store.append(self.ans)
            self.entry.set_text(result + "=" + self.store[0])

        except ArithmeticError:
            self.entry.set_text("Error")
            return 0

    def empty(self, widget):
        self.store = []
        self.entry.set_text("")

