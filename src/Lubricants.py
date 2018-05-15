from .definitions import *

try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gio
except ImportError as e:
    print(e)


class Lubricants(Gtk.Dialog):

    def __init__(self, branch_id, date, *args):
        Gtk.Dialog.__init__(self, *args)
        self.database = DataBase("julaw.db")
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        self._branch_id = branch_id
        self._date = date
        self.definitions.set_date(date)
        self.database.hcreate("Lubricants", "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                                            "`branchid` INT ( 2 ) NOT NULL, `date` DATE NOT NULL,"
                                            "`Inventory_id` INT ( 20 ) NOT NULL,"
                                            " `quantity` INT ( 6 ) NOT NULL, `unit_price` INT ( 9 ) NOT NULL")
        self.set_border_width(10)
        self.set_size_request(920, 500)
        self.lubs = self.definitions.get_data("Lubricants")
        self.row_id = []
        self.popup = None
        self.item = []
        self.quantity = []
        self.price = []
        self.amount = []
        self.balance = Gtk.Entry()
        self.total = []
        self.balance.set_placeholder_text("Total Amount")
        self.choose = []

        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        scrolled = Gtk.ScrolledWindow()
        scrolled.add(self.grid)
        self.pack_start(scrolled, True, True, 0)

        self.grid.attach(Gtk.Label("ItemCode"), 0, 2, 1, 1)
        self.grid.attach(Gtk.Label("Quantity"), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label("Price"), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label("Amount"), 6, 2, 1, 1)
        if len(self.lubs):
            self.add_row("button", len(self.lubs))
        else:
            if len(self.item):
                for i in range(len(self.item)):
                    self.grid.remove(self.item[i])
                    self.grid.remove(self.quantity[i])
                    self.grid.remove(self.price[i])
                    self.grid.remove(self.amount[i])
                self.grid.remove(self.balance)
            else:
                pass
            self.add_row("button", 1)
        self.show_all()

    def lubricants_caller(self, widget, event, choice):
        inventory = self.item[choice].get_text()
        quantity = self.quantity[choice].get_text()
        price = self.price[choice].get_text()
        insert = None
        if len(inventory) and len(quantity) and len(price) > 0:
            if self.row_id[choice]:
                pass
            else:
                insert = self.database.hinsert("Lubricants", "branchid, date, Inventory_id, quantity, unit_price",
                                               self._branch_id, self._date, inventory, quantity, price)
            real_insert(self.row_id, choice, insert)

    def add_row(self, widget, y):
        z = 0
        z += y
        if len(self.item) > 0:
            for n in range(0, len(self.item), 1):
                self.grid.remove(self.item[n])
                self.grid.remove(self.quantity[n])
                self.grid.remove(self.price[n])
                self.grid.remove(self.amount[n])
            self.grid.remove(self.balance)
        for i in range(0, z, 1):
            self.row_id.append(None)

            self.item.append(Gtk.Entry())
            image = Gio.ThemedIcon(name="bottom")
            self.item[i].set_icon_from_gicon(Gtk.EntryIconPosition.SECONDARY, image)
            self.item[i].connect("button-press-event", self.popover, i)
            self.item[i].connect("activate", self.add_row, z + 1)
            self.item[i].set_has_frame(False)
            self.item[i].connect("focus-out-event", self.lubricants_caller, i)
            self.item[i].set_placeholder_text("Item")
            self.grid.attach(self.item[i], 0, 4 + 2 * i, 1, 1)

            self.quantity.append(Gtk.Entry())
            self.quantity[i].connect("activate", self.add_row, z + 1)
            self.quantity[i].set_has_frame(False)
            self.quantity[i].connect("focus-out-event", self.lubricants_caller, i)
            self.quantity[i].connect("changed", self.calculate, i)

            self.quantity[i].set_placeholder_text("Quantity")
            self.grid.attach(self.quantity[i], 2, 4 + 2 * i, 1, 1)

            self.price.append(Gtk.Entry())
            self.price[i].set_has_frame(False)
            self.price[i].connect("activate", self.add_row, z + 1)
            self.price[i].connect("focus-out-event", self.lubricants_caller, i)
            self.price[i].connect("changed", self.calculate, i)
            self.price[i].set_placeholder_text("Price")
            self.grid.attach(self.price[i], 4, 4 + 2 * i, 1, 1)

            self.amount.append(Gtk.Entry())
            self.amount[i].set_has_frame(False)
            self.amount[i].connect("activate", self.add_row, z + 1)
            self.amount[i].set_placeholder_text("Amount")
            self.grid.attach(self.amount[i], 6, 4 + 2 * i, 1, 1)
        self.balance.set_has_frame(False)
        self.grid.attach(self.balance, 6, 4 + 2 * (y + 1), 1, 1)

        try:
            for n in range(0, len(self.lubs), 1):
                real_insert(self.row_id, n, self.lubs[n][0])
                self.item[n].set_text(str(self.lubs[n][3]))
                self.quantity[n].set_text(str(self.lubs[n][4]))
                self.price[n].set_text(str(self.lubs[n][5]))
        except IndexError:
            pass
        self.show_all()

    def popover(self, widget, event, choice):
        self.popup = Gtk.Menu.new()
        product = []
        inventory = self.database.hselect("Inventory_code, Inventory_name", "Inventory",
                                          " WHERE branchid={0} AND"
                                          " Category='Lubricants'".format(self.definitions.get_id()), "")

        if len(inventory) == 0:
            self.item[choice].set_editable(False)
            error_handler(self.get_ancestor(Gtk.ApplicationWindow), "Pliz register inventory")
            return
        for x in range(0, len(inventory), 1):
            product.append([inventory[x][0], Gtk.MenuItem(inventory[x][1])])
            product[x][1].connect("activate", lambda widget, m: self.item[choice].set_text(str(product[m][0])), x)
            self.popup.insert(product[x][1], x)
        self.popup.popup(None, None, None, None, event.button, Gtk.get_current_event_time())
        self.popup.show_all()

    def calculate(self, widget, choice):
        price = self.price[choice].get_text()
        quantity = self.quantity[choice].get_text()
        if len(quantity) and len(price) > 0:
            amount = int(price) * float(quantity)
            self.amount[choice].set_text(locale.format("%05.2f", amount, grouping=True))
            real_insert(self.total, choice, amount)
            total = add_array(self.total)

            self.balance.set_text(locale.format("%05.2f", total,
                                                grouping=True))
