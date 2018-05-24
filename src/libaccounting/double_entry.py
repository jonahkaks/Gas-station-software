from src.definitions import *
from src.utils import Datetime

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import datetime


class DoubleEntry(Gtk.Dialog):
    def __init__(self, branch_id, date, acc_code, acc_type, *args, **kwargs):
        Gtk.Dialog.__init__(self, *args, **kwargs)
        self.currentDate = datetime.date.today()
        self.account = self.get_title()
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.account
        self.set_titlebar(hb)
        self.account_code = acc_code
        self.calendar = Gtk.Calendar()
        self.cwindow = Gtk.Window()
        self.cwindow.set_decorated(False)
        self.cwindow.add(self.calendar)
        self.cwindow.set_modal(True)
        self.calendar.connect('day-selected-double-click', self.hide_widget)
        self.database = DataBase("julaw.db")
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        self.definitions.set_date(date)
        self.date = Datetime.CalendarEntry()
        self.branch_id = branch_id
        self.date_range = date
        self.debit_array = {}
        self.credit_array = {}
        self.row_id = {}
        self.data = {}
        self.codes = {}
        self.account_list = Gtk.ListStore(int, str, bool, str, str, str, str, str, str)
        self.store = Gtk.ListStore(str)
        self.set_default_size(1200, 600)
        self.set_border_width(20)
        self.account_cd = {}
        self.accounts = self.database.hselect("name, code, placeholder, value", "accounts", "", "")
        for item in self.accounts:
            if item[0] == self.account:
                pass
            elif item[2]:
                pass
            else:
                self.account_cd[item[3]] = item[1]
                self.codes[item[1]] = item[3]
                self.store.append([item[3]])

        self.category = acc_type
        self.box = self.get_content_area()
        self.entry_array = []
        self.tree = Gtk.TreeView.new_with_model(self.account_list)
        self.tree.set_enable_tree_lines(True)
        self.selection = self.tree.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)

        self.make_list()
        self.scrollable_tree_list = Gtk.ScrolledWindow()
        self.scrollable_tree_list.add(self.tree)
        self.box.pack_start(self.scrollable_tree_list, True, True, 0)
        self.update_display()
        self.__connect_signals()
        self.show_all()
        response = self.run()
        if response == Gtk.ResponseType.OK:
            self.definitions.insertion(self.data)
        elif response == Gtk.ResponseType.CANCEL:
            pass
        self.destroy()

    def __connect_signals(self):
        self.tree.connect("button-press-event", self.button_press_cb)
        self.tree.connect("key-press-event", self.key_tree_tab)
        self.connect("destroy", Gtk.main_quit)

    def make_list(self):
        renderer = Gtk.CellRendererText()
        renderer.set_fixed_size(20, 25)
        column = Gtk.TreeViewColumn("#", renderer, text=0)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer_button = Gtk.CellRendererToggle()
        renderer_button.connect("toggled", self.show_widget)
        renderer.set_fixed_size(100, 25)
        renderer.set_property("editable", True)
        column = Gtk.TreeViewColumn("Date")
        column.pack_start(renderer, False)
        column.add_attribute(renderer, 'text', 1)
        column.pack_end(renderer_button, False)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(10, 25)
        renderer.connect("edited", self.edit_data)
        column = Gtk.TreeViewColumn("Folio", renderer, text=3)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(400, 25)
        column = Gtk.TreeViewColumn("Details", renderer, text=4)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", self.store)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        renderer_combo.connect("edited", self.edit_data)
        renderer_combo.set_fixed_size(200, 25)
        column = Gtk.TreeViewColumn("Transfer", renderer_combo, text=5)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Debit", renderer, text=6)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Credit", renderer, text=7)
        renderer.connect("edited", self.edit_data)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", False)
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("Balance", renderer, text=8)
        self.tree.append_column(column)

    def hide_widget(self, *args):
        self.cwindow.hide()

    def show_widget(self, widget, path):
        if not widget.get_active():
            alloc = widget.get_allocation()
            nreq, req = self.cwindow.get_preferred_size()
            pos, x, y = widget.get_window().get_origin()
            x += alloc.x
            y += alloc.y
            bwidth = alloc.width
            bheight = alloc.height

            x += bwidth - req.width
            y += bheight

            if x < 0:
                x = 0

            if y < 0:
                y = 0
            self.cwindow.move(x, y)
            self.cwindow.show_all()
            self.calendar.connect('day-selected', self.update_entry, path)
        else:
            self.hide_widget()

    def update_entry(self, widget, path):
        year, month, day = self.calendar.get_date()
        month = month + 1
        self.currentDate = datetime.date(year, month, day)
        text = self.currentDate.strftime("%Y-%m-%d")
        self.account_list[path][1] = text

    def edit_data(self, widget, row, value):
        path, col = self.tree.get_cursor()
        header = col.get_title().lower()
        columns = [c for c in self.tree.get_columns() if c.get_visible()]
        col_num = columns.index(col) + 1
        try:
            ids = self.row_id[int(str(row)) + 1]
        except KeyError:
            pass
        treeiter = self.account_list.get_iter(path)
        self.account_list.set_value(treeiter, col_num, value)

        if ids:
            header = header.lower()
            if header == "transfer":
                self.database.hupdate("transactions", "{0}='{1}'".format("contra_id", self.account_cd[value]),
                                      "transid={0}".format(ids))
            else:
                self.database.hupdate("transactions", "{0}='{1}'".format(header, value), "transid={0}".format(ids))
        else:
            pass
        self.calculate_balance(path)

    def calculate_balance(self, row):
        debit = self.account_list[row][6]
        credit = self.account_list[row][7]
        if not debit:
            debit = 0
        if not credit:
            credit = 0
        self.debit_array[str(row)] = float(debit)
        self.credit_array[str(row)] = float(credit)
        total = 0
        for k in self.debit_array:
            total += self.debit_array[k] - self.credit_array[k]

        if self.category in [1, 2]:
            pass

        elif self.category in [3, 4, 5]:
            total *= -1

        self.account_list[row][8] = str(total)

    def collect_data(self, row):
        rid = self.account_list[row][0]
        date = str(self.account_list[row][1])
        folio = str(self.account_list[row][3])
        details = str(self.account_list[row][4])
        transfer = str(self.account_list[row][5])
        debit = self.account_list[row][6]
        credit = self.account_list[row][7]
        if not debit:
            debit = 0
        if not credit:
            credit = 0
        self.calculate_balance(row)
        self.data[str(rid)] = [self.account_code, self.account_cd[transfer], date, details, folio, debit, credit]
        self.append_rows(int(rid) + 1)

    def append_rows(self, index):
        self.row_id[index] = None
        self.account_list.append([index, str(self.date.currentDate), True, "n", None,
                                  None, None, None, None])

    def update_display(self):
        data = []
        try:
            data = self.database.hselect("*", "transactions", " WHERE branchid={0} AND "
                                                              "account_id = {1} AND {2}".format(self.branch_id,
                                                                                                self.account_code,
                                                                                                self.date_range), "")
        except:
            pass
        if data:
            for n, array in enumerate(data):
                self.row_id[n + 1] = array[0]
                self.debit_array[str(n)] = float(array[7])
                self.credit_array[str(n)] = float(array[8])
                balance = 0
                for k in self.debit_array:
                    balance += self.debit_array[k] - self.credit_array[k]
                if self.category in [1, 2]:
                    pass
                elif self.category in [3, 4, 5]:
                    balance *= -1
                self.account_list.append([n + 1, array[4], True, array[6], array[5], self.codes[array[3]],
                                          str(array[7]),
                                          str(array[8]), str(balance)])
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
                self.database.hdelete("transactions", "transid={0}".format(record_id))
            else:
                record_id = rows
                self.row_id.pop(record_id)
            try:
                self.data.pop(record_id)
            except KeyError:
                pass
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
        if keyname == "Tab" or keyname == "Enter":

            if colnum + 1 <= 7:
                next_column = columns[colnum + 1]
            else:
                tmodel = treeview.get_model()
                titer = tmodel.iter_next(tmodel.get_iter(path))
                debit = self.account_list[path][6]
                credit = self.account_list[path][7]
                if titer is None and debit and credit:
                    self.collect_data(path)
                    titer = tmodel.iter_next(tmodel.get_iter(path))
                path = tmodel.get_path(titer)
                next_column = columns[0]

            GLib.timeout_add(50, treeview.set_cursor, path, next_column, True)
        elif keyname == 'Escape':
            pass
