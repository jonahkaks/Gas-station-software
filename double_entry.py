from definitions import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DoubleEntry(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.details = []
        self.debit = []
        self.credit = []
        self.row_id = []
        self.balance = Gtk.Label()
        self.total_debit = []
        self.total_credit = []
        self.set_default_size(600, 500)
        self.set_border_width(40)
        self.totald = Gtk.Entry()
        self.totalc = Gtk.Entry()
        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.add(self.grid)
        self.totald.set_placeholder_text("Total deposit")
        self.totalc.set_placeholder_text("Total credit")
        box = self.get_content_area()
        self.entry_array = []
        title = self.get_title()
        try:
            self.entry_array = get_data(title)
        except:
            pass
        if len(self.entry_array) == 0:
            self.entry_array = []
        box.pack_start(self.scrollable, True, True, 0)
        self.grid.attach(Gtk.Label("Details"), 0, 2, 1, 1)
        self.grid.attach(Gtk.Label("Dr"), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label("Cr"), 4, 2, 1, 1)
        if len(self.entry_array):
            self.add_row("button", len(self.entry_array))
        else:
            self.add_row("button", 1)
        response = self.run()
        if response == Gtk.ResponseType.OK:
            print("okay")
        elif response == Gtk.ResponseType.CANCEL:
            print("canceled")
        self.destroy()

    def insertion_caller(self, event, widget, choice):
        if len(self.details[choice].get_text()) and len(self.debit[choice].get_text()) \
                and len(self.credit[choice].get_text()) > 0:
            table = self.get_title()
            results = insertion(table, self.row_id[choice], choice, self.details[choice].get_text(),
                                self.debit[choice].get_text(), self.credit[choice].get_text())
            self.entry_array = get_data(table)
            if len(self.entry_array) == 0:
                self.entry_array = []
            self.totald.set_text(results[0])
            self.totalc.set_text(results[1])
            real_insert(self.row_id, choice, results[2])
            self.balance.set_markup("<span color=\'red\'><b>Balance ={0}</b></span>"
                                    .format(float(results[0]) - float(results[1])))

    def add_row(self, widget, y):
        z = 0
        z += y
        if len(self.details) > 0:
            for n in range(0, len(self.details), 1):
                self.grid.remove(self.details[n])
                self.grid.remove(self.debit[n])
                self.grid.remove(self.credit[n])
            self.grid.remove(self.totald)
            self.grid.remove(self.totalc)
            self.grid.remove(self.balance)
        for i in range(0, z, 1):
            self.row_id.append(None)
            self.details.append(Gtk.Entry())
            self.details[i].set_margin_left(20)
            self.details[i].set_placeholder_text("Name")
            self.details[i].connect("activate", self.add_row, z + 1)
            self.details[i].connect("focus-out-event", self.insertion_caller, i)
            self.details[i].connect("changed", self.chan, i)

            self.grid.attach(self.details[i], 0, 4 + 2 * i, 1, 1)
            self.debit.append(Gtk.Entry())
            self.debit[i].connect("activate", self.add_row, z + 1)
            self.debit[i].connect("focus-out-event", self.insertion_caller, i)
            self.debit[i].connect("changed", self.chan, i)
            self.debit[i].set_placeholder_text("Amount")
            self.grid.attach(self.debit[i], 2, 4 + 2 * i, 1, 1)

            self.credit.append(Gtk.Entry())
            self.credit[i].connect("activate", self.add_row, z + 1)
            self.credit[i].connect("focus-out-event", self.insertion_caller, i)
            self.credit[i].connect("changed", self.chan, i)
            self.credit[i].set_placeholder_text("Amount")
            self.grid.attach(self.credit[i], 4, 4 + 2 * i, 1, 1)
        self.grid.attach(self.totald, 2, 4 + 2 * (y + 1), 1, 1)
        self.grid.attach(self.totalc, 4, 4 + 2 * (y + 1), 1, 1)
        self.grid.attach(self.balance, 4, 6 + 2 * (y + 1), 1, 1)
        try:
            for n in range(0, len(self.entry_array), 1):
                real_insert(self.row_id, n, self.entry_array[n][0])
                self.details[n].set_text(str(self.entry_array[n][4]))
                self.debit[n].set_text(str(self.entry_array[n][5]))
                self.credit[n].set_text(str(self.entry_array[n][6]))
        except IndexError:
            pass
        self.show_all()

    def chan(self, widget, index):
        try:
            real_insert(details_array, index, self.details[index].get_text())
            real_insert(debit_array, index, float(self.debit[index].get_text()))
            real_insert(credit_array, index, float(self.credit[index].get_text()))
        except ValueError:
            pass
        results = str(add_array(debit_array)), str(add_array(credit_array))
        self.totald.set_text(results[0])
        self.totalc.set_text(results[1])
        self.balance.set_markup("<span color=\'red\'><b>Balance ={0}</b></span>"
                                .format(float(results[0]) - float(results[1])))
