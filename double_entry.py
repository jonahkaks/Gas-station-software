from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DoubleEntry(Gtk.Dialog):
    def __init__(self, branch_id, date, *args, **kwargs):
        Gtk.Dialog.__init__(self, *args, **kwargs)
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.title = self.get_title()
        self.database = DataBase("julaw.db")
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        self.definitions.set_date(date)
        self.branch_id = branch_id
        self.date = date
        self.dates = []
        self.button = []
        self.details = []
        self.debit = []
        self.folio = []
        self.credit = []
        self.row_id = []
        self.debit_array = []
        self.credit_array = []
        self.category = None
        try:
            self.category = self.database.hselect("account_type", "accounts",
                                                  "WHERE name='{0}'".format(self.title), "")[0][0]
        except IndexError:
            pass
        self.affected = []
        self.floating_balance = []
        self.set_default_size(1200, 600)
        self.set_border_width(20)
        self.accounts = self.database.hselect("name", "accounts",
                                              "WHERE level !='NewTopLevelAccount' AND name !='{0}' AND"
                                              " branchid={1}".format(self.title,
                                                                     self.definitions.get_id()), "")

        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.add(self.grid)
        box = self.get_content_area()
        self.entry_array = []
        try:
            self.entry_array = self.database.hselect("*", self.title,
                                                     " WHERE branchid={0} AND {1}".format(branch_id,
                                                                                          date), "")
        except:
            pass
        if len(self.entry_array) == 0:
            self.entry_array = []
        box.pack_start(self.scrollable, True, True, 0)
        self.grid.attach(Gtk.Label("Date"), 0, 2, 1, 1)
        self.grid.attach(Gtk.Label(), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label("Num"), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label("Description"), 6, 2, 1, 1)
        self.grid.attach(Gtk.Label("Transfer"), 8, 2, 1, 1)
        self.grid.attach(Gtk.Label("Debit"), 10, 2, 1, 1)
        self.grid.attach(Gtk.Label("Credit"), 12, 2, 1, 1)
        self.grid.attach(Gtk.Label("Balance"), 14, 2, 1, 1)

        if len(self.entry_array):
            self.add_row("button", len(self.entry_array))
        else:
            self.add_row("button", 1)
        response = self.run()
        if response == Gtk.ResponseType.OK:
            pass
        elif response == Gtk.ResponseType.CANCEL:
            pass
        self.destroy()

    def insertion_caller(self, event, widget, choice):
        model = self.affected[choice].get_model()
        tree_iter = self.affected[choice].get_active_iter()
        operation = ""
        affected = ""
        try:
            operation = model[tree_iter][0]
            affected = model[tree_iter][1]
        except:
            pass
        details = self.details[choice].get_text()
        folio = self.folio[choice].get_text()
        debit = self.debit[choice].get_text()
        credit = self.credit[choice].get_text()
        date = self.dates[choice].get_text()
        if len(details) and len(debit) and len(credit) and len(date) > 0:
            table = self.get_title()
            id = self.definitions.insertion(table, date, operation, affected,
                                            self.row_id[choice], details, folio, debit, credit)
            self.entry_array = self.database.hselect("*", self.title,
                                                     " WHERE branchid={0} "
                                                     "AND {1}".format(self.branch_id, self.date), "")

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
                self.grid.remove(self.dates[n])
                self.grid.remove(self.button[n])
                self.grid.remove(self.details[n])
                self.grid.remove(self.folio[n])
                self.grid.remove(self.debit[n])
                self.grid.remove(self.credit[n])
                self.grid.remove(self.floating_balance[n])
                self.grid.remove(self.affected[n])

        for i in range(0, z, 1):
            self.row_id.append(None)

            self.dates.append(Gtk.Entry())
            self.dates[i].set_has_frame(False)
            self.dates[i].connect("activate", self.add_row, z + 1)
            self.dates[i].connect("focus-out-event", self.insertion_caller, i)
            self.dates[i].connect("focus-in-event", self.set_date, i)
            self.grid.attach(self.dates[i], 0, 4 + 2 * i, 1, 1)

            self.button.append(Gtk.Button(label="."))
            self.button[i].connect("clicked", self.date_popup, i)
            self.grid.attach(self.button[i], 2, 4 + 2 * i, 1, 1)

            self.folio.append(Gtk.Entry())
            self.folio[i].set_has_frame(False)
            self.folio[i].set_placeholder_text("Num")
            self.folio[i].connect("activate", self.add_row, z + 1)
            self.folio[i].connect("focus-out-event", self.insertion_caller, i)
            self.folio[i].connect("changed", self.chan, i)
            self.folio[i].connect("focus-in-event", self.set_date, i)
            self.grid.attach(self.folio[i], 4, 4 + 2 * i, 1, 1)

            self.details.append(Gtk.Entry())
            self.details[i].set_has_frame(False)
            self.details[i].set_placeholder_text("Details")
            self.details[i].connect("activate", self.add_row, z + 1)
            self.details[i].connect("focus-out-event", self.insertion_caller, i)
            self.details[i].connect("focus-in-event", self.set_date, i)
            self.details[i].connect("changed", self.chan, i)
            self.grid.attach(self.details[i], 6, 4 + 2 * i, 1, 1)

            store = Gtk.ListStore(str, str)
            store.append(["", ""])
            for row in self.accounts:
                store.append(["Debit", row[0]])
                store.append(["Credit", row[0]])
            combo = Gtk.ComboBox.new_with_model(store)
            renderer_text = Gtk.CellRendererText()
            combo.pack_start(renderer_text, False)
            combo.add_attribute(renderer_text, "text", 0)
            renderer_text = Gtk.CellRendererText()
            combo.pack_end(renderer_text, False)
            combo.add_attribute(renderer_text, "text", 1)
            self.affected.append(combo)
            self.grid.attach(self.affected[i], 8, 4 + 2 * i, 1, 1)

            self.debit.append(Gtk.Entry())
            self.debit[i].set_has_frame(False)
            self.debit[i].connect("activate", self.add_row, z + 1)
            self.debit[i].connect("focus-out-event", self.insertion_caller, i)
            self.debit[i].connect("changed", self.chan, i)
            self.debit[i].set_placeholder_text("Amount")
            self.debit[i].connect("focus-in-event", self.set_date, i)
            self.grid.attach(self.debit[i], 10, 4 + 2 * i, 1, 1)

            self.credit.append(Gtk.Entry())
            self.credit[i].set_has_frame(False)
            self.credit[i].connect("activate", self.add_row, z + 1)
            self.credit[i].connect("focus-out-event", self.insertion_caller, i)
            self.credit[i].connect("changed", self.chan, i)
            self.credit[i].connect("focus-in-event", self.set_date, i)
            self.credit[i].set_placeholder_text("Amount")
            self.grid.attach(self.credit[i], 12, 4 + 2 * i, 1, 1)

            self.floating_balance.append(Gtk.Entry())
            self.floating_balance[i].set_has_frame(False)
            self.floating_balance[i].connect("activate", self.add_row, z + 1)
            self.floating_balance[i].connect("focus-out-event", self.insertion_caller, i)
            self.floating_balance[i].connect("focus-in-event", self.set_date, i)
            self.floating_balance[i].connect("changed", self.chan, i)
            self.floating_balance[i].set_placeholder_text("Amount")
            self.grid.attach(self.floating_balance[i], 14, 4 + 2 * i, 1, 1)

        try:
            for n in range(0, len(self.entry_array), 1):
                store.clear()
                store.append([None, str(self.entry_array[n][4])])
                self.affected[n].set_active(0)
                real_insert(self.row_id, n, self.entry_array[n][0])
                self.dates[n].set_text(str(self.entry_array[n][1]))
                self.details[n].set_text(str(self.entry_array[n][5]))
                self.folio[n].set_text(str(self.entry_array[n][6]))
                self.debit[n].set_text(str(self.entry_array[n][7]))
                self.credit[n].set_text(str(self.entry_array[n][8]))
        except IndexError:
            pass
        self.show_all()

    def date_popup(self, widget, choice):
        dialog = Gtk.Dialog("Calender", self.get_ancestor(Gtk.ApplicationWindow),
                            Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK,
                                                    Gtk.ResponseType.OK,
                                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        box = dialog.get_content_area()
        dialog.set_default_size(300, 300)
        calender = Gtk.Calendar()
        box.pack_start(calender, True, True, 0)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            year, month, date = calender.get_date()
            value = make_date(year, month, date)
            self.dates[choice].set_text(value)

        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.close()

    def chan(self, widget, index):
        debit = self.debit[index].get_text().replace(",", "")
        credit = self.credit[index].get_text().replace(",", "")
        if len(debit) and len(credit) > 0:
            results = "0"
            real_insert(self.debit_array, index, eval(debit))
            real_insert(self.credit_array, index, eval(credit))
            if self.category in ["Assets", "Expenses"]:
                results = str(add_array(self.debit_array) - add_array(self.credit_array))
            elif self.category in ["Incomes", "Liabilities", "Equity"]:
                results = str(add_array(self.credit_array) - add_array(self.debit_array))

            self.floating_balance[index].set_text(results)

    def set_date(self, widget, event, choice):
        if len(self.dates[choice].get_text()) == 0:
            calender = Gtk.Calendar()
            year, month, day = calender.get_date()
            value = make_date(year, month, day)
            self.dates[choice].set_text(value)
