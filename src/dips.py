from .definitions import *

try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gio, GLib, Gdk
except ImportError as e:
    print(e)


class Dips(Gtk.ScrolledWindow):
    def __init__(self, branch_id, database, *args):
        super(Dips, self).__init__(*args)
        self.database = database
        self.branch_id = branch_id
        self.date_range = None
        self.row_id = {}
        self.pms = {}
        self.ago = {}
        self.bik = {}
        self.fuel_code = {}
        self.fuel_name = {}
        self.store = Gtk.ListStore(str)
        self.total_amount = []
        self.account_list = Gtk.ListStore(str, str, str, str, str, str)
        self.tree = Gtk.TreeView.new_with_model(self.account_list)
        self.tree.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.selection = self.tree.get_selection()
        self.make_list()
        self.add(self.tree)
        self.update_tanks()
        self.__connect_signals()
        self.show_all()

    def __connect_signals(self):
        self.tree.connect("key-press-event", self.key_tree_tab)
        self.connect("destroy", Gtk.main_quit)

    def set_date(self, date):
        self.date_range = date
        self.account_list.clear()
        self.update_display()

    @staticmethod
    def add_list(array):
        total = 0
        for v in array:
            total += array[v]
        return total

    def update_sales_meter(self, product, value, choice):
        ans = 0
        if product[:3] == "PMS":
            self.pms[choice] = float(value)
            ans = self.add_list(self.pms)
        elif product[:3] == "AGO":
            self.ago[choice] = float(value)
            ans = self.add_list(self.ago)
        elif product[:3] == "BIK":
            self.bik[choice] = float(value)
            ans = self.add_list(self.bik)

        counter = 0
        n = 0
        for i in range(0, len(self.account_list), 1):
            if self.account_list[i][0] == product[:3]:
                self.account_list[i][4] = str(ans)
                counter = 1
                break
            n = i
        if counter:
            self.calculate_balance(n)
            pass
        else:
            self.account_list[n][0] = product
            self.account_list[n][4] = str(ans)
            self.append_rows(n + 1)
        self.calculate_balance(n)

    def make_list(self):
        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", self.store)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        renderer_combo.connect("edited", self.edit_data)
        renderer_combo.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Tanks", renderer_combo, text=0)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(100, 25)
        renderer.connect("edited", self.edit_data)
        column = Gtk.TreeViewColumn("Opening Dips", renderer, text=1)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Closing Dips", renderer, text=2)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Sales Dips", renderer, text=3)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Sales Meter", renderer, text=4)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Difference", renderer, text=5)
        self.tree.append_column(column)

    def update_tanks(self):
        self.fuel_code.clear()
        self.fuel_name.clear()
        tanks = self.database.hselect("id, name", "tanks", "", "")
        for n in tanks:
            self.store.append([n[1]])
            self.fuel_code[n[1]] = n[0]
            self.fuel_name[n[0]] = n[1]

    def edit_data(self, widget, row, value):
        path, col = self.tree.get_cursor()
        header = col.get_title().split(" ")[0].lower()
        columns = [c for c in self.tree.get_columns() if c.get_visible()]
        col_num = columns.index(col)
        ids = 0
        try:
            ids = self.row_id[int(str(row)) + 1]
        except KeyError:
            pass
        treeiter = self.account_list.get_iter(path)
        self.account_list.set_value(treeiter, col_num, value)
        if header == "tanks":
            header = "tank_id"
            value = self.fuel_code[value]

        if ids:
            header = header.lower()
            self.database.hupdate("Dips", "{0}='{1}'".format(header, value), "id={0}".format(ids))
        else:
            pass
        self.calculate_balance(path)

    def calculate_balance(self, row):
        opening = self.account_list[row][1]
        closing = self.account_list[row][2]
        dips = self.account_list[row][3]
        meters = self.account_list[row][4]
        if not opening:
            opening = 0
        if not closing:
            closing = 0
        if not dips:
            dips = 0
        if not meters:
            meters = 0
        litres = float(opening) - float(closing)
        self.account_list[row][5] = str(float(meters) - float(dips))
        self.account_list[row][3] = str(litres)

    def insert_data(self, row):
        rid = int(str(row))
        product = self.account_list[row][0]
        opening = self.account_list[row][1]
        closing = self.account_list[row][2]
        self.calculate_balance(row)
        insert_id = self.database.hinsert("Dips", "branchid, date, tank_id, opening, closing", self.branch_id,
                                          self.date_range, self.fuel_code[product], opening, closing)
        self.row_id[rid] = insert_id
        self.append_rows(int(rid) + 1)

    def update_display(self):
        data = self.database.hselect("id, tank_id, opening, closing",
                                     "Dips", " WHERE branchid={0} AND "
                                             "date ='{1}'".format(self.branch_id, self.date_range), "")
        if data:
            for i, n in enumerate(data):
                self.row_id[i + 1] = n[0]
                real_insert(self.total_amount, i, n[3] - n[2])
                self.account_list.append([self.fuel_name[n[1]], str(n[2]), str(n[3]),
                                          str(n[2] - n[3]), None, None])
                self.calculate_balance(i)
            self.row_id[len(data) + 1] = None
            self.append_rows(len(data) + 1)
        else:
            self.append_rows(1)

    def append_rows(self, index):
        self.row_id[index] = None
        self.account_list.append([None, None, None, None, None, None])

    def key_tree_tab(self, treeview, event):
        keyname = Gdk.keyval_name(event.keyval)
        path, col = treeview.get_cursor()
        columns = [c for c in treeview.get_columns() if c.get_visible()]
        colnum = columns.index(col)

        if keyname == "Tab" or keyname == "Esc" or keyname == "Enter":

            if colnum + 1 <= 3:
                next_column = columns[colnum + 1]
            else:
                tmodel = treeview.get_model()
                titer = tmodel.iter_next(tmodel.get_iter(path))
                opening = self.account_list[path][1]
                closing = self.account_list[path][2]
                if titer is None and opening and closing:
                    self.insert_data(path)
                    titer = tmodel.iter_next(tmodel.get_iter(path))
                path = tmodel.get_path(titer)
                next_column = columns[0]

            if keyname in ['Tab', 'Enter']:
                GLib.timeout_add(50, treeview.set_cursor, path, next_column, True)
            elif keyname == 'Escape':
                pass
