#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


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
        self.pms.set_placeholder_text("pms_price")
        self.ago = Gtk.Entry()
        self.ago.set_placeholder_text("ago_price")
        self.bik = Gtk.Entry()
        self.bik.set_placeholder_text("bik_price")
        self.save_price = Gtk.Button("Save")
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
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_activated(self, widget, row, col):
        model = widget.get_model()
        text = model[row][0]
        print(text)
        if text == "Fuel":
            self.box.pack_start(self.grid, True, True, 0)
            self.grid.attach(Gtk.Label("PMS"), 2, 2, 1, 1)
            self.grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
            self.grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)

            self.grid.attach(self.pms, 4, 2, 2, 1)
            self.grid.attach(self.ago, 4, 4, 2, 1)
            self.grid.attach(self.bik, 4, 6, 2, 1)
            self.grid.attach(self.save_price, 4, 8, 2, 1)
            self.show_all()
