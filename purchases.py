from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class FuelPurchase(Gtk.Dialog):

    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        self.set_default_size(600, 400)
        self.set_border_width(40)
        self.purchase_array = get_data("fuel_purchases")
        self.ago = Gtk.Entry()
        self.bik_total = Gtk.Entry()
        self.bik_price = Gtk.Entry()
        self.bik = Gtk.Entry()
        self.ago_total = Gtk.Entry()
        self.ago_price = Gtk.Entry()
        self.pms_total = Gtk.Entry()
        self.pms_price = Gtk.Entry()
        self.pms = Gtk.Entry()
        box = self.get_content_area()
        grid = Gtk.Grid(column_spacing=3, row_spacing=10)
        box.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label("Product"), 2, 0, 1, 1)
        grid.attach(Gtk.Label("Quantity"), 4, 0, 1, 1)
        grid.attach(Gtk.Label("Price"), 6, 0, 1, 1)
        grid.attach(Gtk.Label("Amount"), 8, 0, 1, 1)
        grid.attach(Gtk.Label("PMS"), 2, 2, 1, 1)
        total = Gtk.Entry()
        self.pms.set_placeholder_text("litres")
        grid.attach(self.pms, 4, 2, 1, 1)
        self.pms_price.set_placeholder_text("price")
        self.pms_price.connect('changed',
                               lambda widget:
                               self.pms_total.set_text(thousand_separator(
                                   str(int(self.pms.get_text().replace(",", "")) * int(
                                       self.pms_price.get_text().replace(",", ""))))))
        grid.attach(self.pms_price, 6, 2, 1, 1)
        self.pms_total.set_placeholder_text("total")
        self.pms_total.connect("changed", lambda widget: total.set_text(
            thousand_separator(str(int(self.pms_total.get_text().replace(",", ""))))))
        grid.attach(self.pms_total, 8, 2, 1, 1)

        grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
        self.ago.set_placeholder_text("litres")
        grid.attach(self.ago, 4, 4, 1, 1)
        self.ago_price.connect('changed', lambda widget: self.ago_total.set_text(
            thousand_separator(
                str(int(self.ago.get_text().replace(",", "")) * int(self.ago_price.get_text().replace(",", ""))))))
        self.ago_price.set_placeholder_text("price")
        grid.attach(self.ago_price, 6, 4, 1, 1)
        self.ago_total.set_placeholder_text("total")
        self.ago_total.connect("changed", lambda widget: total.set_text(
            thousand_separator(
                str(int(total.get_text().replace(",", "")) + int(self.ago_total.get_text().replace(",", ""))))))

        grid.attach(self.ago_total, 8, 4, 1, 1)

        grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)
        self.bik.set_placeholder_text("litres")
        grid.attach(self.bik, 4, 6, 1, 1)

        self.bik_price.set_placeholder_text("price")
        self.bik_price.connect('changed', lambda widget: self.bik_total.set_text(
            thousand_separator(
                str(int(self.bik.get_text().replace(",", "")) * int(self.bik_price.get_text().replace(",", ""))))))
        grid.attach(self.bik_price, 6, 6, 1, 1)

        self.bik_total.set_placeholder_text("total")
        self.bik_total.connect("changed", lambda widget: total.set_text(
            thousand_separator(
                str(int(total.get_text().replace(",", "")) + int(self.bik_total.get_text().replace(",", ""))))))
        grid.attach(self.bik_total, 8, 6, 1, 1)
        total.set_placeholder_text("total")
        grid.attach(total, 8, 8, 1, 1)

        try:
            self.pms.set_text(str(self.purchase_array[0]))
            self.pms_price.set_text(str(self.purchase_array[1]))
            self.ago.set_text(str(self.purchase_array[2]))
            self.ago_price.set_text(str(self.purchase_array[3]))
            self.bik.set_text(str(self.purchase_array[4]))
            self.bik_price.set_text(str(self.purchase_array[5]))
        except IndexError:
            pass

        self.show_all()

        response = self.run()
        if response == Gtk.ResponseType.OK:
            self.fuel_purchase_caller("button")
        elif response == Gtk.ResponseType.CANCEL:
            print("canceled")
        self.close()

    def fuel_purchase_caller(self, widget):
        if len(self.pms.get_text().replace(",", "")) and len(self.pms_price.get_text().replace(",", "")) and \
                len(self.ago.get_text().replace(",", "")) and len(self.ago_price.get_text().replace(",", "")) \
                and len(self.bik.get_text().replace(",", "")) and \
                len(self.bik_price.get_text().replace(",", "")) > 0:
            real_insert(self.purchase_array, 0, self.pms.get_text().replace(",", ""))
            real_insert(self.purchase_array, 1, self.pms_price.get_text().replace(",", ""))
            real_insert(self.purchase_array, 2, self.ago.get_text().replace(",", ""))
            real_insert(self.purchase_array, 3, self.ago_price.get_text().replace(",", ""))
            real_insert(self.purchase_array, 4, self.bik.get_text().replace(",", ""))
            real_insert(self.purchase_array, 5, self.bik_price.get_text().replace(",", ""))

            fuel_purchase(self.pms.get_text(), self.pms_price.get_text(), self.ago.get_text(),
                          self.ago_price.get_text(), self.bik.get_text(),
                          self.bik_price.get_text().replace(",", ""))


class Lubricants(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
