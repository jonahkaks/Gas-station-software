from src.database_handler import DataBase
from src.definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk


class Purchases(Gtk.ScrolledWindow):
    def __init__(self, branch_id, date, *args):
        super(Purchases, self).__init__(*args)
        builder = Gtk.Builder()
        builder.add_from_file("../data/topmenu.glade")
        self.dialog = builder.get_object("purchasedialog")
        self.dialog.set_border_width(10)
        self.dialog.set_size_request(920, 500)
        self.dialog.set_modal(True)
        self.dialog.set_title("Purchases")
        self.box = builder.get_object("purchasebox")
        self.database = DataBase("julaw.db")
        self.branch_id = branch_id
        self.date_range = date
        self.row_id = {}
        self.data = {}
        self.inventory_code = {}
        self.code_name = {}
        self.total_amount = []
        self.account_list = Gtk.ListStore(int, str, str, str, str, str)
        self.store = Gtk.ListStore(str)
        self.tree = Gtk.TreeView.new_with_model(self.account_list)
        self.tree.set_enable_tree_lines(True)
        self.selection = self.tree.get_selection()
        self.make_list()
        self.add(self.tree)
        self.box.pack_start(self, True, True, 0)
        self.update_inventory()
        self.__connect_signals()
        self.update_display()
        self.show_all()
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            self.database.__del__()
        elif response == Gtk.ResponseType.CANCEL:
            self.database.__del__()
        self.dialog.close()

    def __connect_signals(self):
        self.tree.connect("button-press-event", self.button_press_cb)
        self.tree.connect("key-press-event", self.key_tree_tab)
        self.connect("destroy", Gtk.main_quit)

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
        renderer_combo.set_fixed_size(200, 25)
        column = Gtk.TreeViewColumn("ItemCode", renderer_combo, text=1)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Quantity", renderer, text=2)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Price", renderer, text=3)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Amount", renderer, text=4)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Total", renderer, text=5)
        self.tree.append_column(column)

    def edit_data(self, widget, row, value):
        path, col = self.tree.get_cursor()
        header = col.get_title().lower()
        columns = [c for c in self.tree.get_columns() if c.get_visible()]
        col_num = columns.index(col)
        try:
            ids = self.row_id[int(str(row)) + 1]
        except KeyError:
            pass
        treeiter = self.account_list.get_iter(path)
        self.account_list.set_value(treeiter, col_num, value)
        if ids:
            header = header.lower()
            self.database.hupdate("Purchases", "{0}='{1}'".format(header, value), "id={0}".format(ids))
        else:
            pass
        self.calculate_balance(path)

    def update_inventory(self):
        self.store.clear()
        self.inventory_code.clear()
        inventory = self.database.hselect("inventory.code, inventory.name",
                                          "inventory", "", "")
        for n in inventory:
            self.store.append([n[1]])
            self.inventory_code[n[1]] = n[0]
            self.code_name[n[0]] = n[1]

    def calculate_balance(self, row):
        quantity = self.account_list[row][2]
        price = self.account_list[row][3]
        if not quantity:
            quantity = 0
        if not price:
            price = 0
        amount = int(price) * int(quantity)
        real_insert(self.total_amount, int(str(row)), amount)

        self.account_list[row][4] = str(amount)
        self.account_list[row][5] = str(add_array(self.total_amount))

    def insert_data(self, row):
        rid = self.account_list[row][0]
        item_code = self.account_list[row][1]
        quantity = self.account_list[row][2]
        price = self.account_list[row][3]
        self.calculate_balance(row)
        self.data[str(rid)] = [self.branch_id, self.date_range, self.inventory_code[item_code], quantity, price]
        self.append_rows(int(rid) + 1)

    def append_rows(self, index):
        self.row_id[index] = None
        self.account_list.append([index, None, None, None, None, None])

    def update_display(self):
        data = self.database.hselect("id, itemcode, quantity, price",
                                     "Purchases", " WHERE branchid={0} AND "
                                                  "date = '{1}'".format(self.branch_id, self.date_range), "")
        if data:
            for i, n in enumerate(data):
                self.row_id[i + 1] = n[0]
                real_insert(self.total_amount, i, n[2] * n[3])
                self.account_list.append([i + 1, self.code_name[n[1]], str(n[2]), str(n[3]),
                                          str(n[2] * n[3]), str(add_array(self.total_amount))])
            self.row_id[len(data) + 1] = None
            self.append_rows(len(data) + 1)
        else:
            self.row_id[1] = None
            self.append_rows(1)

    def row_right_clicked(self, widget, event):
        pop = Gtk.Menu.new()
        remove_record = Gtk.MenuItem("Remove Record")
        remove_record.connect("activate", self.delete_row)
        pop.insert(remove_record, 0)
        pop.popup(None, None, None, None, event.button, Gtk.get_current_event_time())
        pop.show_all()

    def button_press_cb(self, widget, event):
        if event.button == 3:
            if self.selection.count_selected_rows() >= 1:
                path, column, posx, posy = widget.get_path_at_pos(int(event.x), int(event.y))
                if path:
                    self.selection.unselect_all()
                    self.selection.select_path(path)
                    self.row_right_clicked(widget, event)

    def delete_row(self, *args):
        store, paths = self.selection.get_selected_rows()
        for t in paths:
            rows = int(str(t)) + 1
            record_id = self.row_id[rows]
            if record_id:
                self.database.hdelete("Purchases", "id={0}".format(record_id))
            else:
                record_id = rows
                self.row_id.pop(record_id)
            iterator = self.account_list.get_iter(t)
            if len(self.account_list) < 2:
                self.account_list.remove(iterator)
                self.append_rows(1)
            else:
                self.account_list.remove(iterator)

    def key_tree_tab(self, treeview, event):
        keyname = Gdk.keyval_name(event.keyval)
        path, col = treeview.get_cursor()
        columns = [c for c in treeview.get_columns() if c.get_visible()]
        colnum = columns.index(col)

        if keyname == "Tab" or keyname == "Esc" or keyname == "Enter":

            if colnum + 1 <= 4:
                next_column = columns[colnum + 1]
            else:
                tmodel = treeview.get_model()
                titer = tmodel.iter_next(tmodel.get_iter(path))
                quantity = self.account_list[path][2]
                price = self.account_list[path][4]
                if titer is None and quantity and price:
                    self.insert_data(path)
                    titer = tmodel.iter_next(tmodel.get_iter(path))
                path = tmodel.get_path(titer)
                next_column = columns[0]

            if keyname in ['Tab', 'Enter']:
                GLib.timeout_add(50, treeview.set_cursor, path, next_column, True)
            elif keyname == 'Escape':
                pass


class Item(Gtk.Dialog):

    def __init__(self, branch_id, *args):
        Gtk.Dialog.__init__(self, *args)
        self.database = DataBase("julaw.db")
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        self.item = Gtk.Entry()
        self.item.set_has_frame(False)
        self.item.set_placeholder_text("Item")
        self.description = Gtk.Entry()
        self.description.set_has_frame(False)
        self.description.set_placeholder_text("Description")
        self.item.set_placeholder_text("Inventory name")
        store = Gtk.ListStore(str)
        store.append(["Fuel"])
        store.append(["Lubricants"])

        combo = Gtk.ComboBox.new_with_model(store)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        combo.set_active(0)

        box = self.get_content_area()

        self.set_default_size(300, 300)
        self.set_border_width(50)
        box.pack_start(Gtk.Label("Item Name"), True, False, 1)
        box.pack_start(self.item, True, False, 0)
        box.pack_start(Gtk.Label("Item Description"), True, False, 1)
        box.pack_start(self.description, True, False, 0)
        box.pack_start(Gtk.Label("Item Type"), True, False, 1)
        box.pack_start(combo, True, False, 0)

        self.show_all()

        response = self.run()
        if response == Gtk.ResponseType.OK:
            model = combo.get_model()
            tree_iter = combo.get_active_iter()
            category = model[tree_iter][0]

            self.database.hinsert("inventory", "name, description, type",
                                  self.item.get_text(),
                                  self.description.get_text(), category)
            self.database.__del__()
        elif response == Gtk.ResponseType.CANCEL:
            self.database.__del__()
        self.close()
