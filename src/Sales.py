#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.OtherSales import OtherSales
from src.definitions import *
from src.dips import Dips

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk


class Sales(Gtk.ScrolledWindow):
    def __init__(self, branch_id, *args, **kwargs):
        super(Sales, self).__init__(*args, **kwargs)
        self.database = DataBase("julaw.db")
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        self.branch_id = branch_id
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.calender = Gtk.Calendar()
        year, month, day = self.calender.get_date()
        value = make_date(year, month, day)
        self.date = value
        self.calender.connect("day-selected", self.changed_day)
        self.profit_label = Gtk.Label()
        self.inventory_code = {}
        self.code_name = {}
        self.row_id = {}
        self.inventory_price = {}
        self.frame = Gtk.Frame()
        self.frame1 = Gtk.Frame()
        self.frame2 = Gtk.Frame()

        self.product_label = []
        self.product_id = []
        self.button = Gtk.Button()
        self.scrolled = Gtk.ScrolledWindow()
        self.lub = OtherSales(branch_id, self.database)
        self.dip = Dips(branch_id, self.database)
        self.frame.add(self.scrolled)
        self.frame1.add(self.lub)
        self.frame2.add(self.dip)
        self.frame.set_label("Fuel")
        self.frame1.set_label("OtherSales")
        self.frame2.set_label("Dips")
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.pack_start(self.frame1, True, True, 10)
        self.hbox.pack_start(self.frame2, True, True, 10)
        self.add(self.box)
        self.box.pack_start(self.calender, False, False, 0)
        self.box.pack_start(self.frame, True, True, 0)
        self.box.pack_start(self.hbox, True, True, 0)
        self.box.pack_end(self.button, False, True, 0)
        self.button.add(self.profit_label)
        self.account_list = Gtk.ListStore(int, str, str, str, str, str, str, str)
        self.tree = Gtk.TreeView.new_with_model(self.account_list)
        self.scrolled.add(self.tree)
        self.store = Gtk.ListStore(str)
        self.__connect_signals()
        self.make_list()
        self.update_inventory()
        self.changed_day("calender")

    def update_inventory(self):
        self.store.clear()
        self.inventory_code.clear()
        inventory = self.database.hselect("inventory.code, inventory.name, prices.price",
                                          "inventory, prices", "where inventory.code=prices.code",
                                          "AND inventory.type='Fuel'")
        for n in inventory:
            self.store.append([n[1]])
            self.inventory_code[n[1]] = n[0]
            self.code_name[n[0]] = n[1]
            self.inventory_price[n[1]] = n[2]

    def make_list(self):
        renderer = Gtk.CellRendererText()
        renderer.set_fixed_size(20, 25)
        column = Gtk.TreeViewColumn("#", renderer, text=0)
        self.tree.append_column(column)

        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", self.store)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        renderer_combo.connect("edited", self.edit_data)
        renderer_combo.set_fixed_size(400, 25)
        column = Gtk.TreeViewColumn("Product", renderer_combo, text=1)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(120, 25)
        renderer.connect("edited", self.edit_data)
        column = Gtk.TreeViewColumn("OpeningMeter", renderer, text=2)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(120, 25)
        column = Gtk.TreeViewColumn("ClosingMeter", renderer, text=3)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(120, 25)
        column = Gtk.TreeViewColumn("Rtt", renderer, text=4)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Litres", renderer, text=5)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Price", renderer, text=6)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Amount", renderer, text=7)
        self.tree.append_column(column)

    def __connect_signals(self):
        self.tree.connect("key-press-event", self.key_tree_tab)
        self.connect("destroy", Gtk.main_quit)

    def set_date(self, value):
        self.date = value

    def get_date(self):
        return self.date

    def changed_day(self, widget):
        year, month, day = self.calender.get_date()
        value = make_date(year, month, day)
        self.definitions.set_date(value)
        self.lub.set_date(value)
        self.dip.set_date(value)
        self.date = value
        self.update_display()
        self.profit_label.set_markup("<span color='blue'><b>Cash at hand:</b>{0}       </span>"
                                     "<span color='green'>Gross profit:{1}</span>".format(thousand_separator(67000),
                                                                                          30000))
        self.show_all()

    def edit_data(self, widget, row, value):
        path, col = self.tree.get_cursor()
        header = col.get_title().split(" ")[0].lower()
        columns = [c for c in self.tree.get_columns() if c.get_visible()]
        col_num = columns.index(col)
        try:
            ids = self.row_id[int(str(row)) + 1]
        except KeyError:
            pass
        treeiter = self.account_list.get_iter(path)
        self.account_list.set_value(treeiter, col_num, value)
        if header == "product":
            header = "product_id"
            self.account_list[path][col_num + 5] = str(self.inventory_price[value])
            value = self.inventory_code[value]

        if ids:
            header = header.lower()
            self.database.hupdate("fuel", "{0}='{1}'".format(header, value), "id={0}".format(ids))
        else:
            pass
        self.calculate_balance(row)

    def calculate_balance(self, row):
        product = self.account_list[row][1]
        opening = self.account_list[row][2]
        closing = self.account_list[row][3]
        rtt = self.account_list[row][4]
        price = self.account_list[row][6]
        if not opening:
            opening = 0
        if not closing:
            closing = 0
        if not rtt:
            rtt = 0
        if not price:
            price = 0
        litres = float(closing) - (float(opening) + float(rtt))
        self.account_list[row][5] = str(litres)
        amount = litres * int(price)
        self.account_list[row][7] = str(amount)
        self.dip.update_sales_meter(product, litres, int(str(row)))

    def insert_data(self, row):
        rid = int(str(row)) + 1
        product = self.account_list[row][1]
        opening = self.account_list[row][2]
        closing = self.account_list[row][3]
        rtt = self.account_list[row][4]
        price = self.account_list[row][5]
        self.calculate_balance(row)
        insert_id = self.database.hinsert("fuel", "branchid, date, product_id, openingmeter, closingmeter, rtt, price",
                                          self.branch_id, self.date, self.inventory_code[product], float(opening),
                                          float(closing), float(rtt), price)
        self.row_id[rid] = insert_id
        self.append_rows(int(rid) + 1)

    def update_display(self):
        self.account_list.clear()
        data = self.database.hselect("id, product_id, openingmeter, closingmeter, rtt, price",
                                     "fuel", " WHERE branchid={0} AND "
                                             "date ='{1}'".format(self.branch_id, self.date), "")
        if data:
            for i, n in enumerate(data):
                self.row_id[i + 1] = n[0]
                litres = n[3] - (n[4] + n[2])
                product = self.code_name[int(n[1])]
                self.account_list.append([i + 1, product, str(n[2]), str(n[3]),
                                          str(n[4]), str(litres), str(n[5]), str(n[5] * litres)])
                self.dip.update_sales_meter(product, litres, i)
            self.row_id[len(data) + 1] = None
            self.append_rows(len(data) + 1)
        else:
            self.append_rows(1)

    def append_rows(self, index):
        self.row_id[index] = None
        self.account_list.append([index, None, None, None, None, None, None, None])

    def key_tree_tab(self, treeview, event):
        keyname = Gdk.keyval_name(event.keyval)
        path, col = treeview.get_cursor()
        columns = [c for c in treeview.get_columns() if c.get_visible()]
        colnum = columns.index(col)

        if keyname == "Tab" or keyname == "Esc" or keyname == "Enter":

            if colnum + 1 <= 7:
                next_column = columns[colnum + 1]
            else:
                tmodel = treeview.get_model()
                titer = tmodel.iter_next(tmodel.get_iter(path))
                opening = self.account_list[path][1]
                closing = self.account_list[path][2]
                rtt = self.account_list[path][3]
                price = self.account_list[path][5]
                if titer is None and opening and closing and rtt and price:
                    self.insert_data(path)
                    titer = tmodel.iter_next(tmodel.get_iter(path))
                path = tmodel.get_path(titer)
                next_column = columns[0]

            if keyname in ['Tab', 'Enter']:
                GLib.timeout_add(50, treeview.set_cursor, path, next_column, True)
            elif keyname == 'Escape':
                pass
