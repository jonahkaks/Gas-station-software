from .definitions import *

try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gio, GLib, Gdk
except ImportError as e:
    print(e)


class OtherSales(Gtk.ScrolledWindow):
    def __init__(self, branch_id, database, *args):
        super(OtherSales, self).__init__(*args)
        self.database = database
        self.branch_id = branch_id
        self.date_range = None
        self.row_id = {}
        self.inventory_code = {}
        self.inventory_price = {}
        self.code_name = {}
        self.total_amount = []
        self.account_list = Gtk.ListStore(int, str, str, str, str, str)
        self.store = Gtk.ListStore(str)
        self.tree = Gtk.TreeView.new_with_model(self.account_list)
        self.tree.set_enable_tree_lines(True)
        self.selection = self.tree.get_selection()
        self.make_list()
        self.add(self.tree)
        self.update_inventory()
        self.__connect_signals()
        self.show_all()

    def __connect_signals(self):
        self.tree.connect("button-press-event", self.button_press_cb)
        self.tree.connect("key-press-event", self.key_tree_tab)
        self.connect("destroy", Gtk.main_quit)

    def set_date(self, date):
        self.date_range = date
        self.account_list.clear()
        self.update_display()

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
        if header == "itemcode":
            self.account_list[path][col_num + 2] = str(self.inventory_price[value])

        if ids:
            header = header.lower()
            self.database.hupdate("Sales", "{0}='{1}'".format(header, value), "id={0}".format(ids))
        else:
            pass
        self.calculate_balance(path)

    def update_inventory(self):
        self.store.clear()
        self.inventory_code.clear()
        inventory = self.database.hselect("inventory.code, inventory.name, prices.price",
                                          "inventory, prices", "where inventory.code=prices.code",
                                          "AND inventory.type != 'Fuel'")
        for n in inventory:
            self.store.append([n[1]])
            self.inventory_code[n[1]] = n[0]
            self.code_name[n[0]] = n[1]
            self.inventory_price[n[1]] = n[2]

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
        insert_id = self.database.hinsert("Sales", "branchid, date, itemcode, quantity, price", self.branch_id,
                                          self.date_range, self.inventory_code[item_code], quantity, price)
        self.row_id[rid] = insert_id
        self.append_rows(int(rid) + 1)

    def append_rows(self, index):
        self.row_id[index] = None
        self.account_list.append([index, None, None, None, None, None])

    def update_display(self):
        data = self.database.hselect("id, itemcode, quantity, price",
                                     "Sales", " WHERE branchid={0} AND "
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
                self.database.hdelete("Sales", "id={0}".format(record_id))
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
