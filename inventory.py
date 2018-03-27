from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class Purchases(Gtk.Dialog):

    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        hcreate("Purchases", "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                             "`branchid` INT ( 2 ) NOT NULL, `date` DATE NOT NULL,"
                             " `Invoice_id` INT ( 20 ) NOT NULL, `Inventory_id` INT ( 20 ) NOT NULL,"
                             " `quantity` INT ( 6 ) NOT NULL, `unit_price` INT ( 9 ) NOT NULL")
        self.set_border_width(10)
        self.set_size_request(920, 500)
        self.purchase_array = hselect("*", "Purchases", " WHERE branchid=" + str(branch_id[0]),
                                      " AND date='" + sales_date[0] + "'")
        self.invoice = []
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

        box = self.get_content_area()
        self.grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        scrolled = Gtk.ScrolledWindow()
        scrolled.add(self.grid)
        box.pack_start(scrolled, True, True, 0)

        self.grid.attach(Gtk.Label("InvoiceId"), 0, 2, 1, 1)
        self.grid.attach(Gtk.Label("ItemCode"), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label("Quantity"), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label("Price"), 6, 2, 1, 1)
        self.grid.attach(Gtk.Label("Amount"), 8, 2, 1, 1)
        if len(self.purchase_array):
            self.add_row("button", len(self.purchase_array))
        else:
            self.add_row("button", 1)
        self.show_all()

        response = self.run()
        if response == Gtk.ResponseType.OK:
            print("okay")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")
        self.close()

    def purchase_caller(self, widget, event, choice):
        invoice = self.invoice[choice].get_text()
        inventory = self.item[choice].get_text()
        quantity = self.quantity[choice].get_text()
        price = self.price[choice].get_text()
        if len(invoice) and len(inventory) and \
                len(quantity) and len(price) > 0:
            insert = purchase(self.row_id[choice], invoice, inventory, quantity, price)
            real_insert(self.row_id, choice, insert)

    def add_row(self, widget, y):
        image = []
        z = 0
        z += y
        if len(self.invoice) > 0:
            for n in range(0, len(self.invoice), 1):
                self.grid.remove(self.invoice[n])
                self.grid.remove(self.item[n])
                self.grid.remove(self.quantity[n])
                self.grid.remove(self.price[n])
                self.grid.remove(self.amount[n])
            self.grid.remove(self.balance)
        for i in range(0, z, 1):
            self.row_id.append(None)
            self.invoice.append(Gtk.Entry())
            self.invoice[i].set_margin_left(20)
            self.invoice[i].set_has_frame(False)
            self.invoice[i].set_placeholder_text("Invoice id")
            self.invoice[i].connect("activate", self.add_row, z + 1)
            self.invoice[i].connect("focus-out-event", self.purchase_caller, i)
            self.grid.attach(self.invoice[i], 0, 4 + 2 * i, 1, 1)

            self.item.append(Gtk.Entry())
            image.append(Gio.ThemedIcon(name="bottom"))
            self.item[i].set_icon_from_gicon(Gtk.EntryIconPosition.SECONDARY,
                                             image[i])
            self.item[i].connect("button-press-event", self.popover, i)
            self.item[i].connect("activate", self.add_row, z + 1)
            self.item[i].set_has_frame(False)
            self.item[i].connect("focus-out-event", self.purchase_caller, i)

            self.item[i].set_placeholder_text("Item")
            self.choose.append(Gtk.Button())
            self.grid.attach(self.item[i], 2, 4 + 2 * i, 1, 1)

            self.quantity.append(Gtk.Entry())
            self.quantity[i].connect("activate", self.add_row, z + 1)
            self.quantity[i].set_has_frame(False)
            self.quantity[i].connect("focus-out-event", self.purchase_caller, i)
            self.quantity[i].connect("changed", self.calculate, i)

            self.quantity[i].set_placeholder_text("Quantity")
            self.grid.attach(self.quantity[i], 4, 4 + 2 * i, 1, 1)

            self.price.append(Gtk.Entry())
            self.price[i].set_has_frame(False)
            self.price[i].connect("activate", self.add_row, z + 1)
            self.price[i].connect("focus-out-event", self.purchase_caller, i)
            self.price[i].connect("changed", self.calculate, i)
            self.price[i].set_placeholder_text("Price")
            self.grid.attach(self.price[i], 6, 4 + 2 * i, 1, 1)

            self.amount.append(Gtk.Entry())
            self.amount[i].set_has_frame(False)
            self.amount[i].connect("activate", self.add_row, z + 1)
            self.amount[i].set_placeholder_text("Amount")
            self.grid.attach(self.amount[i], 8, 4 + 2 * i, 1, 1)
        self.balance.set_has_frame(False)
        self.grid.attach(self.balance, 8, 4 + 2 * (y + 1), 1, 1)

        try:
            for n in range(0, len(self.purchase_array), 1):
                real_insert(self.row_id, n, self.purchase_array[n][0])
                self.invoice[n].set_text(str(self.purchase_array[n][3]))
                self.item[n].set_text(str(self.purchase_array[n][4]))
                self.quantity[n].set_text(str(self.purchase_array[n][5]))
                self.price[n].set_text(str(self.purchase_array[n][6]))
        except IndexError:
            pass
        self.show_all()

    def popover(self, widget, event, choice):
        self.popup = Gtk.Menu.new()
        product = []
        inventory = hselect("Inventory_id, Inventory_name", "Inventory",
                            " WHERE branchid={0}".format(branch_id[0]), "")

        if len(inventory) == 0:
            self.item[choice].set_editable(False)
            error_handler(self, "Pliz register inventory")
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


class Item(Gtk.Dialog):

    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        hcreate("Inventory", "`Inventory_id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                             " `branchid` INTEGER NOT NULL, `Inventory_name` TEXT,"
                             " `Inventory_description` TEXT")
        self.item = Gtk.Entry()
        self.item.set_placeholder_text("Item")
        self.description = Gtk.Entry()
        self.description.set_placeholder_text("description")
        self.item.set_placeholder_text("child account")

        box = self.get_content_area()

        self.set_default_size(300, 300)
        self.set_border_width(50)
        box.pack_start(self.item, True, False, 0)
        box.pack_start(self.description, True, False, 0)

        self.show_all()

        response = self.run()
        if response == Gtk.ResponseType.OK:
            hinsert("Inventory", "branchid, "
                                 "Inventory_name, Inventory_description",
                    branch_id[0], self.item.get_text(), self.description.get_text())
        elif response == Gtk.ResponseType.CANCEL:
            print("cancel")
        self.close()
