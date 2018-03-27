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
        self.debit_array = []
        self.credit_array = []

        self.floating_balance = []
        self.set_default_size(740, 600)
        self.set_border_width(40)

        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.add(self.grid)
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
        self.grid.attach(Gtk.Label("Balance"), 6, 2, 1, 1)

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
        details = self.details[choice].get_text()
        debit = self.debit[choice].get_text()
        credit = self.credit[choice].get_text()
        if len(details) and len(debit) and len(credit) > 0:
            table = self.get_title()
            id = insertion(table, self.row_id[choice], details, debit, credit)
            self.entry_array = get_data(table)
            if len(self.entry_array) == 0:
                self.entry_array = []
            real_insert(self.row_id, choice, id)
            real_insert(self.debit_array, choice, eval(debit))
            real_insert(self.credit_array, choice, eval(credit))

    def add_row(self, widget, y):
        z = 0
        z += y
        if len(self.details) > 0:
            for n in range(0, len(self.details), 1):
                self.grid.remove(self.details[n])
                self.grid.remove(self.debit[n])
                self.grid.remove(self.credit[n])
                self.grid.remove(self.floating_balance[n])

        for i in range(0, z, 1):
            self.row_id.append(None)
            self.details.append(Gtk.Entry())
            self.details[i].set_has_frame(False)
            self.details[i].set_margin_left(20)
            self.details[i].set_placeholder_text("Name")
            self.details[i].connect("activate", self.add_row, z + 1)
            self.details[i].connect("focus-out-event", self.insertion_caller, i)
            self.details[i].connect("changed", self.chan, i)

            self.grid.attach(self.details[i], 0, 4 + 2 * i, 1, 1)
            self.debit.append(Gtk.Entry())
            self.debit[i].set_has_frame(False)
            self.debit[i].connect("activate", self.add_row, z + 1)
            self.debit[i].connect("focus-out-event", self.insertion_caller, i)
            self.debit[i].connect("changed", self.chan, i)
            self.debit[i].set_placeholder_text("Amount")
            self.grid.attach(self.debit[i], 2, 4 + 2 * i, 1, 1)

            self.credit.append(Gtk.Entry())
            self.credit[i].set_has_frame(False)
            self.credit[i].connect("activate", self.add_row, z + 1)
            self.credit[i].connect("focus-out-event", self.insertion_caller, i)
            self.credit[i].connect("changed", self.chan, i)
            self.credit[i].set_placeholder_text("Amount")
            self.grid.attach(self.credit[i], 4, 4 + 2 * i, 1, 1)

            self.floating_balance.append(Gtk.Entry())
            self.floating_balance[i].set_has_frame(False)
            self.floating_balance[i].connect("activate", self.add_row, z + 1)
            self.floating_balance[i].connect("focus-out-event", self.insertion_caller, i)
            self.floating_balance[i].connect("changed", self.chan, i)
            self.floating_balance[i].set_placeholder_text("Amount")
            self.grid.attach(self.floating_balance[i], 6, 4 + 2 * i, 1, 1)

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
        details = self.details[index].get_text()
        debit = self.debit[index].get_text()
        credit = self.credit[index].get_text()
        if len(details) and len(debit) and len(credit) > 0:
            real_insert(self.debit_array, index, eval(debit))
            real_insert(self.credit_array, index, eval(credit))
            results = str(add_array(self.debit_array) - add_array(self.credit_array))
            self.floating_balance[index].set_text(results)
