#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

gi.require_version('Gtk', '3.0')
from definitions import *
from database_handler import DataBase


def replace_widget(old, new):
    parent = old.get_parent()
    props = {}
    for key in Gtk.ContainerClass.list_child_properties(type(parent)):
        props[key.name] = parent.child_get_property(old, key.name)
        parent.remove(old)
        parent.add(new)


class Settings(Gtk.Dialog):
    def __init__(self, branch_id, date, *args):
        Gtk.Dialog.__init__(self, *args)
        self.database = DataBase("julaw.db")
        self.definitions = Definitions()
        self.definitions.set_date(date)
        self.definitions.set_id(branch_id)
        self.database.hcreate("Prices", "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                                        "`branchid` INTEGER NOT NULL, `start_date` DATE NOT NULL,"
                                        " `stop_date` DATE NOT NULL,"
                                        " `Inventory_code` INTEGER NOT NULL, `price` INTEGER NOT NULL")

        self.save_price = Gtk.Button("Save")
        self.label = Gtk.Label()
        self.price = []
        self.popup = None
        self.inventory = []
        self.row_id = []
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
        treestore.append(it, ["InventoryPrices"])

        it = treestore.append(None, ["Appearence"])
        treestore.append(it, ["Theme"])
        treestore.append(it, ["Font"])

        tree.append_column(languages)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        tree.set_model(treestore)
        self.vp.add1(tree)
        self.box.set_border_width(80)
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.grid.attach(Gtk.Label("Item Code"), 0, 2, 1, 1)
        self.grid.attach(Gtk.Label("Price"), 2, 2, 1, 1)
        self.vp.add2(self.box)
        self.vp.set_position(300)
        self.add(self.vp)
        tree.connect("row-activated", self.on_activated)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_activated(self, widget, row, col):
        model = widget.get_model()
        text = model[row][0]
        if text == "InventoryPrices":
            self.box.pack_start(self.grid, True, True, 0)
            self.add_row("button", 1)
            self.show_all()

    def add_row(self, widget, y):
        z = 0
        z += y
        if len(self.inventory) > 0:
            for n in range(0, len(self.inventory), 1):
                self.grid.remove(self.inventory[n])
                self.grid.remove(self.price[n])
            self.grid.remove(self.label)
            self.grid.remove(self.save_price)
        for i in range(0, z, 1):
            self.row_id.append(None)
            self.inventory.append(Gtk.Entry())
            self.inventory[i].set_margin_left(20)
            self.inventory[i].set_placeholder_text("Inventory_code")
            self.inventory[i].set_has_frame(False)
            self.inventory[i].connect("activate", self.add_row, z + 1)
            self.inventory[i].connect("focus-out-event", self.insert_price, i)
            self.inventory[i].connect("button-press-event", self.popover, i)
            self.grid.attach(self.inventory[i], 0, 4 + 2 * i, 1, 1)

            self.price.append(Gtk.Entry())
            self.price[i].set_has_frame(False)
            self.price[i].connect("activate", self.add_row, z + 1)
            self.price[i].connect("focus-out-event", self.insert_price, i)
            self.price[i].set_placeholder_text("Price")
            self.grid.attach(self.price[i], 2, 4 + 2 * i, 1, 1)
        self.grid.attach(self.save_price, 2, 4 + 2 * (y + 1), 1, 1)
        self.grid.attach(self.label, 0, 6 + 2 * (y + 1), 2, 1)

        self.show_all()

    def popover(self, widget, event, choice):
        self.popup = Gtk.Menu.new()
        product = []
        inventory = self.database.hselect("Inventory_code, Inventory_name", "Inventory",
                                          " WHERE branchid={0}".format(self.definitions.get_id()), "")
        if len(inventory) == 0:
            self.inventory[choice].set_editable(False)
            error_handler(self, "pliz add inventory items first")
            return

        for x in range(0, len(inventory), 1):
            product.append([inventory[x][0], Gtk.MenuItem(inventory[x][1])])
            product[x][1].connect("activate", lambda widget, m: self.inventory[choice].set_text(str(product[m][0])),
                                  x)
            self.popup.insert(product[x][1], x)
        self.popup.popup(None, None, None, None, event.button, Gtk.get_current_event_time())
        self.popup.show_all()

    def insert_price(self, widget, event, choice):
        inventory = self.inventory[choice].get_text()
        prices = self.price[choice].get_text()
        if len(inventory) and len(prices) > 0:
            if self.row_id[choice]:
                fields = "Inventory_code={0}, price={1}".format(inventory, prices)
                self.database.hupdate("Prices", fields, "id={0}".format(self.row_id[choice]))
                self.label.set_markup("<span color='green'>Price updates successfully</span>")
            else:
                insert_id = self.database.hinsert("Prices", "branchid, start_date,"
                                                            "stop_date, Inventory_code, price",
                                                  self.definitions.get_id(), self.definitions
                                                  .get_date(), "2090-01-01", inventory, prices)
                real_insert(self.row_id, choice, insert_id)
                self.label.set_markup("<span color='blue'>Price set successfully</span>")
        self.show_all()
