import gi

from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class FuelDips(Gtk.Dialog):

    def __init__(self, *args):
        Gtk.Dialog.__init__(self, *args)
        self.dips_id = ""
        self.dip_array = []
        try:
            self.dip_array = get_data("dips")[0]
            self.dips_id = self.dip_array[0]
        except IndexError:
            pass
        self.pms_dp = Gtk.Entry()
        self.pms_cd = Gtk.Entry()
        self.pms_od = Gtk.Entry()
        self.ago_dp = Gtk.Entry()
        self.ago_cd = Gtk.Entry()
        self.ago_od = Gtk.Entry()
        self.bik_dp = Gtk.Entry()
        self.bik_cd = Gtk.Entry()
        self.bik_od = Gtk.Entry()
        self.set_default_size(600, 400)
        self.set_border_width(40)
        box = self.get_content_area()
        grid = Gtk.Grid(column_spacing=3, row_spacing=10)
        box.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label("Product"), 2, 0, 1, 1)
        grid.attach(Gtk.Label("Opening Stock"), 4, 0, 1, 1)
        grid.attach(Gtk.Label("Closing Stock"), 6, 0, 1, 1)
        grid.attach(Gtk.Label("Sales By Dips"), 8, 0, 1, 1)

        grid.attach(Gtk.Label("PMS"), 2, 2, 1, 1)

        self.pms_od.set_placeholder_text("opening dips")
        self.pms_cd.set_placeholder_text("closing dips")
        self.pms_dp.set_placeholder_text("difference")
        dips_total = Gtk.Entry()

        grid.attach(self.pms_od, 4, 2, 1, 1)
        try:
            self.pms_od.connect('changed', lambda widget:
            self.pms_dp.set_text(
                str(float(self.pms_od.get_text()) - float(self.pms_cd.get_text()))))
            self.pms_cd.connect("changed", lambda widget:
            self.pms_dp.set_text(
                str(float(self.pms_od.get_text()) - float(self.pms_cd.get_text()))))
            self.pms_dp.connect("changed", lambda widget: dips_total.set_text(str(
                float(self.pms_dp.get_text()) + float(self.ago_dp.get_text()) +
                float(self.bik_dp.get_text()))))
            self.ago_od.connect('changed', lambda widget:
            self.ago_dp.set_text(
                str(float(self.ago_od.get_text()) - float(self.ago_cd.get_text()))))
            self.ago_cd.connect("changed", lambda widget:
            self.ago_dp.set_text(
                str(float(self.ago_od.get_text()) - float(self.ago_cd.get_text()))))
            self.ago_dp.connect("changed", lambda widget: dips_total.set_text(str(
                float(self.pms_dp.get_text()) + float(self.ago_dp.get_text()) +
                float(self.bik_dp.get_text()))))
            self.bik_od.connect('changed', lambda widget: self.bik_dp.set_text(
                str(float(self.bik_od.get_text()) - float(self.bik_cd.get_text()))))
            self.bik_cd.connect('changed', lambda widget:
            self.bik_dp.set_text(
                str(float(self.bik_od.get_text()) - float(self.bik_cd.get_text()))))
            self.bik_dp.connect("changed", lambda widget: dips_total.set_text(str(
                float(self.pms_dp.get_text()) + float(self.ago_dp.get_text()) +
                float(self.bik_dp.get_text()))))
        except ValueError:
            pass
        self.ago_od.set_placeholder_text("opening dips")
        self.ago_cd.set_placeholder_text("closing dips")
        self.ago_dp.set_placeholder_text("difference")
        grid.attach(self.ago_od, 4, 4, 1, 1)
        grid.attach(self.ago_cd, 6, 4, 1, 1)
        grid.attach(self.ago_dp, 8, 4, 1, 1)
        grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)
        self.bik_od.set_placeholder_text("opening_dips")
        self.bik_cd.set_placeholder_text("closing_dips")
        self.bik_dp.set_placeholder_text("difference")

        dips_total.set_placeholder_text("totaldips")
        grid.attach(self.bik_od, 4, 6, 1, 1)
        grid.attach(self.bik_cd, 6, 6, 1, 1)
        grid.attach(self.bik_dp, 8, 6, 1, 1)
        grid.attach(dips_total, 8, 8, 1, 1)
        grid.attach(self.pms_cd, 6, 2, 1, 1)
        grid.attach(self.pms_dp, 8, 2, 1, 1)
        grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
        try:
            self.pms_od.set_text(str(self.dip_array[3]))
            self.pms_cd.set_text(str(self.dip_array[4]))
            self.ago_od.set_text(str(self.dip_array[5]))
            self.ago_cd.set_text(str(self.dip_array[6]))
            self.bik_od.set_text(str(self.dip_array[7]))
            self.bik_cd.set_text(str(self.dip_array[8]))
        except IndexError:
            pass
        self.show_all()

        response = self.run()
        if response == Gtk.ResponseType.OK:
            self.dips_caller("button")
        elif response == Gtk.ResponseType.CANCEL:
            print("cancelled")
        self.destroy()

    def dips_caller(self, widget):
        if len(self.pms_od.get_text()) and len(self.pms_cd.get_text()) and \
                len(self.ago_od.get_text()) and len(self.ago_cd.get_text()) \
                and len(self.bik_od.get_text()) and len(self.bik_cd.get_text()) > 0:
            results = dips(self.dips_id, self.pms_od.get_text(), self.pms_cd.get_text(),
                           self.ago_od.get_text(),
                           self.ago_cd.get_text(), self.bik_od.get_text()
                           , self.bik_cd.get_text())
            self.pms_dp.set_text(results[0])
            self.ago_dp.set_text(results[1])
            self.bik_dp.set_text(results[2])
            self.dips_id = results[3]
