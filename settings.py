#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from definitions import *


def replace_widget(old, new):
    parent = old.get_parent()
    props = {}
    for key in Gtk.ContainerClass.list_child_properties(type(parent)):
        props[key.name] = parent.child_get_property(old, key.name)
        parent.remove(old)
        parent.add(new)


class Settings(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        self.pms = Gtk.Entry()
        self.pms.set_placeholder_text("Pms Price")
        self.ago = Gtk.Entry()
        self.label = Gtk.Label()
        self.ago.set_placeholder_text("Ago price")
        self.bik = Gtk.Entry()
        self.bik.set_placeholder_text("Bik Price")
        self.save_price = Gtk.Button("Save")
        self.save_price.connect("clicked", self.set_price)
        self.remove(self.get_content_area())
        self.set_default_size(900, 600)
        self.vp = Gtk.Paned()
        tree = Gtk.TreeView()
        languages = Gtk.TreeViewColumn()
        languages.set_title("Settings")
        cell = Gtk.CellRendererText()
        languages.pack_start(cell, True)
        languages.add_attribute(cell, "text", 0)
        treestore = Gtk.TreeStore(str)
        it = treestore.append(None, ["Prices"])
        treestore.append(it, ["Fuel"])

        it = treestore.append(None, ["Appearence"])
        treestore.append(it, ["Theme"])
        treestore.append(it, ["Font"])

        tree.append_column(languages)
        tree.set_model(treestore)
        self.vp.add1(tree)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.set_border_width(150)
        self.grid = Gtk.Grid(column_spacing=30, row_spacing=60)
        self.vp.add2(self.box)
        self.vp.set_position(300)
        self.add(self.vp)
        tree.connect("row-activated", self.on_activated)
        self.show_all()

    def on_activated(self, widget, row, col):
        model = widget.get_model()
        text = model[row][0]
        if text == "Fuel":
            self.box.pack_start(self.grid, True, True, 0)
            self.grid.attach(Gtk.Label("PMS"), 2, 2, 1, 1)
            self.grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
            self.grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)

            self.grid.attach(self.pms, 4, 2, 2, 1)
            self.grid.attach(self.ago, 4, 4, 2, 1)
            self.grid.attach(self.bik, 4, 6, 2, 1)
            self.grid.attach(self.save_price, 4, 8, 2, 1)
            self.grid.attach(self.label, 4, 12, 2, 1)
            self.show_all()

    def set_price(self, widget):
        new = make_date(2090, 2, 2)
        try:
            start_id = hselect("id", "prices", "WHERE start_date='{0}'".format(sales_date[0]), "")[0][0]
            hupdate("prices", "pms={0}, ago={1}, bik={2}".format(self.pms.get_text(),
                                                                 self.ago.get_text(), self.bik.get_text()),
                    "id={0}".format(start_id))
            self.label.set_markup("<span color='green'>Price has been updated successfully</span>")
        except:
            try:
                condition = hselect("Max(id)", "prices", "WHERE branchid={0}".format(branch_id[0]), "")[0][0]
                hupdate("prices", "stop_date='{0}'".format(sales_date[0]), "id={0}".format(condition))
            except:
                pass
            id = hinsert("prices", "branchid, start_date, stop_date,"
                                   " pms, ago, bik", branch_id[0], sales_date[0],
                         new, self.pms.get_text(), self.ago.get_text(), self.bik.get_text())
            if id:
                self.label.set_markup("<span color='green'>Price set successfully</span>")
            else:
                self.label.set_markup("<span color='red'>Failed to set price</span>")
