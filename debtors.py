from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Debtors(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        self.prep_name = []
        self.prep_dr = []
        self.prep_cr = []
        self.prepaid_array = get_data("prepaid", prepaid_id)
        self.set_default_size(500, 500)
        self.set_border_width(40)
        box = self.get_content_area()
        grid = Gtk.Grid(column_spacing=3, row_spacing=10)
        box.pack_start(grid, False, False, 0)
        grid.attach(Gtk.Label("Name"), 0, 2, 1, 1)
        grid.attach(Gtk.Label("Dr"), 2, 2, 1, 1)
        grid.attach(Gtk.Label("Cr"), 4, 2, 1, 1)
        for i in range(0, 5, 1):
            self.prep_name.append(Gtk.Entry())
            self.prep_name[i].set_margin_left(20)
            self.prep_name[i].set_placeholder_text("Name")
            grid.attach(self.prep_name[i], 0, 4 + 2 * i, 1, 1)
            self.prep_dr.append(Gtk.Entry())
            self.prep_dr[i].set_placeholder_text("Amount")
            grid.attach(self.prep_dr[i], 2, 4 + 2 * i, 1, 1)

            self.prep_cr.append(Gtk.Entry())
            self.prep_cr[i].set_placeholder_text("Amount")
            grid.attach(self.prep_cr[i], 4, 4 + 2 * i, 1, 1)
            try:
                self.prep_name[i].set_text(str(self.prepaid_array[i][3]))
                self.prep_dr[i].set_text(str(self.prepaid_array[i][4]))
                self.prep_cr[i].set_text(str(self.prepaid_array[i][5]))
            except IndexError:
                pass
        self.show_all()
        response = self.run()
        if response == Gtk.ResponseType.OK:
            self.prepaid_caller("button")
        elif response == Gtk.ResponseType.CANCEL:
            print("canceled")
        self.destroy()

    def prepaid_caller(self, widget):
        for choice in range(0, 4, 1):
            prepaid(choice, self.prep_name[choice].get_text(), self.prep_dr[choice].get_text(),
                    self.prep_cr[choice].get_text())
