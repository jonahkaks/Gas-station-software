#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Sales(Gtk.ScrolledWindow):
    def __init__(self, branch_id, y, *args, **kwargs):
        super(Sales, self).__init__(*args, **kwargs)
        self.database = DataBase("julaw.db")
        self.definitions = Definitions()
        self.definitions.set_id(branch_id)
        self.branch_id = branch_id
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.calender = Gtk.Calendar()
        year, month, day = self.calender.get_date()
        value = make_date(year, month, day)
        self.date = value
        self.calender.connect("day-selected", self.changed_day)
        self.profit_label = Gtk.Label()

        self.opening_meter = []
        self.closing_meter = []
        self.rtt = []
        self.litres = []
        self.price = []
        self.amount = []

        self.product_label = []
        self.product_id = []
        self.button = Gtk.Button()
        self.grid = Gtk.Grid()

        self.box.pack_start(self.calender, False, False, 0)
        self.box.pack_start(self.grid, False, True, 0)
        self.box.pack_end(self.button, False, True, 0)
        self.button.add(self.profit_label)

        self.add(self.box)
        self.grid.attach(Gtk.Label(label='Product'), 0, 2, 2, 1)
        self.grid.attach(Gtk.Label(label='OpeningMeter'), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='ClosingMeter'), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Rtt'), 6, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Litres'), 8, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Price'), 10, 2, 1, 1)
        self.grid.attach(Gtk.Label(label='Amount'), 12, 2, 1, 1)

        for n in range(len(y)):
            self.product_id.append("")
            self.product_label.append(Gtk.Label(label=y[n]))
            self.grid.attach(self.product_label[n], 0, 3 + n, 1, 1)

            self.opening_meter.append(Gtk.Entry())
            self.opening_meter[n].set_has_frame(False)
            self.opening_meter[n].set_placeholder_text('opening meter')
            self.opening_meter[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.opening_meter[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.opening_meter[n], 2, 3 + n, 1, 1)

            self.closing_meter.append(Gtk.Entry())
            self.closing_meter[n].set_has_frame(False)
            self.closing_meter[n].set_placeholder_text('closing meter')
            self.closing_meter[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.closing_meter[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.closing_meter[n], 4, 3 + n, 1, 1)

            self.rtt.append(Gtk.Entry())
            self.rtt[n].set_has_frame(False)
            self.rtt[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.rtt[n].connect('changed', self.subtraction, n)
            self.grid.attach(self.rtt[n], 6, 3 + n, 1, 1)

            self.litres.append(Gtk.Entry())
            self.litres[n].set_has_frame(False)
            self.litres[n].set_placeholder_text('litres')
            self.litres[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.litres[n], 8, 3 + n, 1, 1)

            self.price.append(Gtk.Entry())
            self.price[n].set_has_frame(False)
            self.price[n].set_placeholder_text("price")
            self.price[n].connect('focus-out-event', self.sales_litres_caller, n)
            self.price[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.price[n], 10, 3 + n, 1, 1)

            self.amount.append(Gtk.Entry())
            self.amount[n].set_has_frame(False)
            self.amount[n].set_placeholder_text("shs")
            self.grid.attach(self.amount[n], 12, 3 + n, 1, 1)

        self.total_amount = Gtk.Entry()
        self.total_amount.set_has_frame(False)
        self.total_amount.set_placeholder_text("total")
        self.grid.attach(self.total_amount, 12, len(y) + 4, 1, 1)

        self.changed_day("calender")

    def sales_litres_caller(self, event, widget, choice):
        product = self.product_label[choice].get_label()
        opening = self.opening_meter[choice].get_text()
        closing = self.closing_meter[choice].get_text()
        rtt = self.rtt[choice].get_text()
        price = self.price[choice].get_text()

        if len(product) and len(opening) and len(closing) and len(rtt) and len(price) > 0:
            result = self.definitions.sales_litres(self.product_id[choice], product, opening,
                                                   closing, rtt, price)
            self.litres[choice].set_text(result[0])
            real_insert(self.product_id, choice, result[1])
            self.changed_day("button")

    def sales_shs_caller(self, widget, choice):
        if len(self.litres[choice].get_text()) and len(
                self.price[choice].get_text()) > 0:
            result = self.definitions.sales_shs(choice, self.litres[choice].get_text(),
                                                self.price[choice].get_text())
            self.amount[choice].set_text(thousand_separator(str(result[0])))
            self.total_amount.set_text(thousand_separator(str(result[1])))

    def changed_day(self, widget):
        year, month, day = self.calender.get_date()
        value = make_date(year, month, day)
        self.definitions.set_date(value)
        self.date = value
        sales_results = self.definitions.get_data("fuel")
        cash = self.definitions.get_cash_profit()
        self.profit_label.set_markup("<span color='blue'><b>Cash at hand:</b>{0}       </span>"
                                     "<span color='green'>Gross profit:{1}</span>".format(thousand_separator(cash),
                                                                                          30000))

        if len(sales_results) > 0:
            for hs in range(0, len(sales_results), 1):
                real_insert(self.product_id, hs, sales_results[hs][0])
                self.opening_meter[hs].set_text(str(sales_results[hs][4]))
                self.closing_meter[hs].set_text(str(sales_results[hs][5]))
                self.rtt[hs].set_text(str(sales_results[hs][6]))
                self.price[hs].set_text(str(sales_results[hs][7]))

        elif len(sales_results) == 0:
            for i in range(0, len(self.opening_meter), 1):
                real_insert(self.product_id, i, "")
                self.opening_meter[i].set_text("")
                self.closing_meter[i].set_text("")
                self.rtt[i].set_text("0.0")
                self.litres[i].set_text("")
                self.amount[i].set_text("")

            self.total_amount.set_text("")
        self.show_all()

    def subtraction(self, widget, choice):
        try:
            opening_stock = float(self.opening_meter[choice].get_text())
            closing_stock = float(self.closing_meter[choice].get_text())
            rtt = float(self.rtt[choice].get_text())
            result = closing_stock - (opening_stock + rtt)

            self.litres[choice].set_text(locale.format("%05.2f", result, grouping=False))
            price = int(self.price[choice].get_text())

            real_insert(self.pr, choice, price)

            real_insert(self.amount_array, choice, result * price)
            self.amount.set_text(str(self.amount_array[choice]))
            self.total_amount.set_text(str(add_array(self.amount_array)))

        except:
            pass
