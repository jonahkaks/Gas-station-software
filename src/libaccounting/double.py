from src.definitions import *
from src.utils import Datetime

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DoubleEntry(Gtk.Dialog):
    def __init__(self, branch_id, date, *args, **kwargs):
        Gtk.Dialog.__init__(self, *args, **kwargs)
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.title = self.get_title()
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.title
        self.set_titlebar(hb)
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
        self.data = []
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
                                              "WHERE level !='NewTopLevelAccount'"
                                              " AND name !='{0}'".format(self.title), "")

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
        self.grid.attach(Gtk.Label("Num"), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label("Description"), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label("Transfer"), 6, 2, 1, 1)
        self.grid.attach(Gtk.Label("Debit"), 8, 2, 1, 1)
        self.grid.attach(Gtk.Label("Credit"), 10, 2, 1, 1)
        self.grid.attach(Gtk.Label("Balance"), 12, 2, 1, 1)

        if len(self.entry_array):
            self.add_row("button", len(self.entry_array))
        else:
            self.add_row("button", 1)
        response = self.run()
        if response == Gtk.ResponseType.OK:
            self.definitions.insertion(self.data)
            print(self.data)
        elif response == Gtk.ResponseType.CANCEL:
            pass
        self.destroy()

    def store_data(self, widget, event, choice):
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
        date = str(self.dates[choice].get_date())
        table = self.get_title()
        if len(debit) < 1:
            debit = 0
        if len(credit) < 1:
            credit = 0

        real_insert(self.data, choice,
                    [table, date, operation, affected, self.row_id[choice], details, folio, debit, credit])

    def add_row(self, widget, y):
        z = 0
        z += y
        if len(self.details) > 0:
            for n in range(0, len(self.details), 1):
                self.grid.remove(self.dates[n])
                self.grid.remove(self.details[n])
                self.grid.remove(self.folio[n])
                self.grid.remove(self.debit[n])
                self.grid.remove(self.credit[n])
                self.grid.remove(self.floating_balance[n])
                self.grid.remove(self.affected[n])

        for i in range(0, z, 1):
            self.row_id.append(None)

            self.dates.append(Datetime.CalendarEntry())
            self.grid.attach(self.dates[i], 0, 4 + 2 * i, 1, 1)

            self.folio.append(Gtk.Entry())
            self.folio[i].set_has_frame(False)
            self.folio[i].set_placeholder_text("Num")
            self.folio[i].set_width_chars(5)
            self.folio[i].connect("activate", self.add_row, z + 1)
            self.folio[i].connect("focus-out-event", self.store_data, i)
            self.folio[i].connect("changed", self.chan, i)
            self.grid.attach(self.folio[i], 2, 4 + 2 * i, 1, 1)

            self.details.append(Gtk.Entry())
            self.details[i].set_has_frame(False)
            self.details[i].set_placeholder_text("Enter transaction details")
            self.details[i].set_size_request(300, 10)
            self.details[i].connect("activate", self.add_row, z + 1)
            self.details[i].connect("focus-out-event", self.store_data, i)
            self.details[i].connect("changed", self.chan, i)
            self.grid.attach(self.details[i], 4, 4 + 2 * i, 1, 1)

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
            self.grid.attach(self.affected[i], 6, 4 + 2 * i, 1, 1)

            self.debit.append(Gtk.Entry())
            self.debit[i].set_has_frame(False)
            self.debit[i].connect("activate", self.add_row, z + 1)
            self.debit[i].set_size_request(100, 10)
            self.debit[i].connect("focus-out-event", self.store_data, i)
            self.debit[i].connect("changed", self.chan, i)
            self.debit[i].set_placeholder_text("Amount")
            self.grid.attach(self.debit[i], 8, 4 + 2 * i, 1, 1)

            self.credit.append(Gtk.Entry())
            self.credit[i].set_has_frame(False)
            self.credit[i].set_size_request(100, 10)
            self.credit[i].connect("activate", self.add_row, z + 1)
            self.credit[i].connect("focus-out-event", self.store_data, i)
            self.credit[i].connect("changed", self.chan, i)
            self.credit[i].set_placeholder_text("Amount")
            self.grid.attach(self.credit[i], 10, 4 + 2 * i, 1, 1)

            self.floating_balance.append(Gtk.Entry())
            self.floating_balance[i].set_editable(False)
            self.floating_balance[i].set_size_request(100, 10)
            self.floating_balance[i].set_has_frame(False)
            self.floating_balance[i].connect("activate", self.add_row, z + 1)
            self.floating_balance[i].connect("focus-out-event", self.store_data, i)
            self.floating_balance[i].connect("changed", self.chan, i)
            self.floating_balance[i].set_placeholder_text("Amount")
            self.grid.attach(self.floating_balance[i], 12, 4 + 2 * i, 1, 1)

        try:
            for n in range(0, len(self.entry_array), 1):
                store.clear()
                store.append([None, str(self.entry_array[n][4])])
                self.affected[n].set_active(0)
                real_insert(self.row_id, n, self.entry_array[n][0])
                self.dates[n].set_date_text(str(self.entry_array[n][1]))
                self.details[n].set_text(str(self.entry_array[n][5]))
                self.folio[n].set_text(str(self.entry_array[n][6]))
                self.debit[n].set_text(str(self.entry_array[n][7]))
                self.credit[n].set_text(str(self.entry_array[n][8]))
        except IndexError:
            pass
        self.show_all()

    def chan(self, widget, index):
        debit = self.debit[index].get_text().replace(",", "")
        credit = self.credit[index].get_text().replace(",", "")
        if len(debit) < 1:
            debit = 0
        if len(credit) < 1:
            credit = 0
        real_insert(self.debit_array, index, float(debit))
        real_insert(self.credit_array, index, float(credit))
        if self.category in ["Assets", "Expenses"]:
            results = str(add_array(self.debit_array) - add_array(self.credit_array))
        elif self.category in ["Incomes", "Liabilities", "Equity"]:
            results = str(add_array(self.credit_array) - add_array(self.debit_array))
        self.floating_balance[index].set_text(results)
