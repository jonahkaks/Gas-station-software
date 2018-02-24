import gi

from calculator import Calc
from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Sales(Gtk.ApplicationWindow):
    """
    here is the sales window which comes after the login window
    """

    def __init__(self, y, *args, **kwargs):
        super(Sales, self).__init__(*args, **kwargs)
        self.pms_dp = Gtk.Entry()
        self.pms_cd = Gtk.Entry()
        self.pms_od = Gtk.Entry()
        self.ago_dp = Gtk.Entry()
        self.ago_cd = Gtk.Entry()
        self.ago_od = Gtk.Entry()
        self.bik_dp = Gtk.Entry()
        self.bik_cd = Gtk.Entry()
        self.bik_od = Gtk.Entry()
        self.ago = Gtk.Entry()
        self.bik_total = Gtk.Entry()
        self.bik_price = Gtk.Entry()
        self.bik = Gtk.Entry()
        self.ago_total = Gtk.Entry()
        self.ago_price = Gtk.Entry()
        self.pms_total = Gtk.Entry()
        self.pms_price = Gtk.Entry()
        self.pms = Gtk.Entry()
        self.maximize()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.y = y
        self.progress = Gtk.Spinner()
        self.dip_array = []
        self.exp = []
        self.exp_name = []
        self.opening_meter = []
        self.closing_meter = []
        self.rtt = []
        self.litres = []
        self.price = []
        self.amount = []
        self.expense_total = Gtk.Entry()
        self.product_label = []
        self.product_changed = []
        self.debt_paid = []
        self.debt_taken = []
        self.debtor_name = []
        self.prep_name = []
        self.prep_amount = []
        self.prepnarray = []
        self.prepaarray = []
        self.airtel_sending = Gtk.Entry()
        self.airtel_withdraw = Gtk.Entry()
        self.mtn_sending = Gtk.Entry()
        self.mtn_withdraw = Gtk.Entry()
        self.debt_taken_total = Gtk.Entry()
        self.debt_paid_total = Gtk.Entry()
        self.products = ["PMS", "PMS2", "AGO", "AGO2", "BIK"]
        self.set_border_width(10)
        self.grid = Gtk.Grid(column_spacing=3, row_spacing=6)
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled.add(self.grid)
        self.add(self.box)
        self.Save = Gtk.Button(label="Save")
        self.calender = Gtk.Calendar()
        self.menubar = Gtk.MenuBar()

        self.file_menu_d = Gtk.MenuItem("Purchases")
        self.file_menu = Gtk.Menu()
        self.file_menu_d.set_submenu(self.file_menu)
        self.fuel = Gtk.MenuItem("Fuel")
        self.fuel.connect("activate", self.fuel_purchase_window)
        self.file_menu.append(self.fuel)
        self.lubricants = Gtk.MenuItem("Lubricants")
        self.file_menu.append(self.lubricants)
        self.menubar.append(self.file_menu_d)

        self.reports_menu = Gtk.Menu()
        self.reports_menu_d = Gtk.MenuItem("Reports")
        self.reports_menu_d.set_submenu(self.reports_menu)
        self.reports_menu.append(Gtk.MenuItem("Trading Profit and Loss"))
        self.reports_menu.append(Gtk.MenuItem("Balance sheet"))
        self.menubar.append(self.reports_menu_d)

        self.dips = Gtk.MenuItem("Dips")
        self.dips.connect("activate", self.dips_window)
        self.menubar.append(self.dips)

        self.utilities = Gtk.MenuItem("Utilities")
        self.utilities.connect("activate", self.calculator)
        self.menubar.append(self.utilities)

        self.settings_button = Gtk.MenuItem("Settings")
        self.settings_button.connect("activate", self.settings)
        self.menubar.append(self.settings_button)

        self.box.pack_start(self.menubar, False, False, 0)
        self.box.pack_start(self.progress, False, False, 0)
        self.box.pack_start(self.scrolled, True, True, 0)

        self.calender.connect("day-selected", self.day_select)
        self.grid.attach(self.calender, 0, 1, 40, 1)
        self.Save.connect("clicked", self.save)
        self.box.pack_end(self.Save, False, False, 0)

        self.grid.attach(Gtk.Label('Product'), 0, 2, 1, 1)
        self.grid.attach(Gtk.Label('OpeningMeter'), 2, 2, 1, 1)
        self.grid.attach(Gtk.Label('ClosingMeter'), 4, 2, 1, 1)
        self.grid.attach(Gtk.Label('Rtt'), 6, 2, 1, 1)
        self.grid.attach(Gtk.Label('Litres'), 8, 2, 1, 1)
        self.grid.attach(Gtk.Label('Price'), 10, 2, 1, 1)
        self.grid.attach(Gtk.Label('Amount'), 12, 2, 1, 1)

        for n in range(0, y, 1):
            product_store = Gtk.ListStore(str)
            for product in self.products:
                product_store.append([product])
            product_combo = Gtk.ComboBox.new_with_model(product_store)
            renderer_text = Gtk.CellRendererText()
            product_combo.pack_start(renderer_text, True)
            product_combo.add_attribute(renderer_text, "text", 0)

            self.product_label.append(product_combo)
            self.product_label[n].connect("changed", self.product_change, n)
            self.grid.attach(self.product_label[n], 0, 3 + n, 1, 1)

            self.opening_meter.append(Gtk.Entry())
            self.opening_meter[n].set_placeholder_text('opening meter')
            self.opening_meter[n].connect('changed', self.sales_litres_caller, n)
            self.grid.attach(self.opening_meter[n], 2, 3 + n, 1, 1)

            self.closing_meter.append(Gtk.Entry())
            self.closing_meter[n].set_placeholder_text('closing meter')
            self.closing_meter[n].connect('changed', self.sales_litres_caller, n)
            self.grid.attach(self.closing_meter[n], 4, 3 + n, 1, 1)

            self.rtt.append(Gtk.Entry())
            self.rtt[n].set_text("0.0")
            self.rtt[n].connect('changed', self.sales_litres_caller, n)
            self.grid.attach(self.rtt[n], 6, 3 + n, 1, 1)

            self.litres.append(Gtk.Entry())
            self.litres[n].set_placeholder_text('litres')
            self.litres[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.litres[n], 8, 3 + n, 1, 1)
            self.price.append(Gtk.Entry())
            self.price[n].set_placeholder_text("price")
            self.price[n].connect("changed", self.sales_shs_caller, n)
            self.grid.attach(self.price[n], 10, 3 + n, 1, 1)

            self.amount.append(Gtk.Entry())
            self.amount[n].set_placeholder_text("shs")
            self.grid.attach(self.amount[n], 12, 3 + n, 1, 1)

        self.total_amount = Gtk.Entry()
        self.total_amount.set_placeholder_text("total")
        self.grid.attach(self.total_amount, 12, y + 4, 1, 1)

        self.grid.attach(Gtk.Label("Airtel"), 0, y + 6, 1, 1)
        self.grid.attach(Gtk.Label("Mtn"), 2, y + 6, 1, 1)

        self.airtel_sending.set_placeholder_text("Airtel sending")
        self.grid.attach(self.airtel_sending, 0, y + 8, 1, 1)
        self.airtel_sending.connect("changed", self.mobile_caller)

        self.airtel_withdraw.set_placeholder_text("Airtel withdraw")
        self.airtel_withdraw.connect("changed", self.mobile_caller)
        self.grid.attach(self.airtel_withdraw, 0, y + 10, 1, 1)

        self.mtn_sending.set_placeholder_text("Mtn sending")
        self.mtn_sending.connect("changed", self.mobile_caller)
        self.grid.attach(self.mtn_sending, 2, y + 8, 1, 1)

        self.mtn_withdraw.set_placeholder_text("Mtn withdraw")
        self.mtn_withdraw.connect("changed", self.mobile_caller)
        self.grid.attach(self.mtn_withdraw, 2, y + 10, 1, 1)

        """
        Adding the cash account
        """
        self.grid.attach(Gtk.Label('Cash'), 4, y + 8, 1, 1)
        self.grid.attach(Gtk.Label('Banked'), 4, y + 10, 1, 1)
        self.cash = Gtk.Entry()
        self.cash.set_placeholder_text("cash")
        self.grid.attach(self.cash, 6, y + 8, 1, 1)

        self.bank = Gtk.Entry()
        self.bank.set_placeholder_text("banked")
        self.grid.attach(self.bank, 6, y + 10, 1, 1)

        self.expense_row = Gtk.Entry()
        self.expense_row.set_placeholder_text("Enter expense rows")

        """
        Prepaid
        """
        self.grid.attach(Gtk.Label('Prepaid'), 10, y + 8, 1, 1)
        self.prepaid = Gtk.Entry()
        self.prepaid.set_placeholder_text("prepaid")
        self.grid.attach(self.prepaid, 12, y + 8, 1, 1)
        self.add_prepaid = Gtk.Button(label="Prepaid")
        self.add_prepaid.connect("clicked", self.add_prepaid_details)
        self.grid.attach(self.add_prepaid, 10, y + 10, 4, 1)

        """
        Expenses button here
         """

        self.expense_row.set_margin_top(30)
        self.expense_row.connect("changed", self.expense_rows)
        self.grid.attach(self.expense_row, 0, y + 18, 4, 1)
        self.debtor_row = Gtk.Entry()
        self.debtor_row.set_placeholder_text("Enter number of debtor rows")
        """
        Adding the debtors rows is done here
        """
        self.debtor_row.connect("changed", self.debtors_rows)
        self.debtor_row.set_margin_top(30)
        self.debtor_row.set_margin_left(20)
        self.grid.attach(self.debtor_row, 4, y + 18, 6, 1)

        """
        Adding the lubricants area
        """
        self.lub_row = Gtk.Entry()
        self.lub_row.set_placeholder_text("Enter Lubricant rows")
        self.lub_row.set_margin_top(30)
        self.lub_row.set_margin_left(20)
        self.lub_row.connect("changed", self.lubricants_rows)
        self.grid.attach(self.lub_row, 10, y + 18, 4, 1)
        self.lub_name = []
        self.lub_amount = []
        self.lub_total = Gtk.Entry()
        self.show_all()
        year, month, date = self.calender.get_date()
        real_insert(sales_date, 0, str(date) + "/" + str(month + 1) + "/" + str(year))
        self.changed_day()

    def mobile_caller(self, widget):
        if len(self.airtel_sending.get_text()) and len(self.airtel_withdraw.get_text()) and \
                len(self.mtn_sending.get_text()) and len(self.mtn_withdraw.get_text()) > 0: \
                mobile_money(0, self.airtel_sending.get_text(), self.airtel_withdraw.get_text(),
                             self.mtn_sending.get_text(), self.mtn_withdraw.get_text())

    def calculator(self, widget):
        cal = Calc("Calculator", self)
        cal.show_all()

    def day_select(self, widget):
        """
         this function is for getting and storing a date
        """

        year, month, date = self.calender.get_date()
        real_insert(sales_date, 0, str(date) + "/" + str(month + 1) + "/" + str(year))
        self.changed_day()

    def changed_day(self):
        self.progress.start()
        sales_results = get_details()
        if len(sales_results[0]) == 3:
            for g in range(0, len(sales_results[0]), 1):
                self.product_label[g].set_active(2 * g)
                self.opening_meter[g].set_text(str(sales_results[0][g][4]))
                self.closing_meter[g].set_text(str(sales_results[0][g][5]))
                self.rtt[g].set_text(str(sales_results[0][g][6]))
        elif len(sales_results[0]) > 3:
            for h in range(0, len(sales_results[0]), 1):
                self.product_label[h].set_active(h)
                self.opening_meter[h].set_text(str(sales_results[0][h][4]))
                self.closing_meter[h].set_text(str(sales_results[0][h][5]))
                self.rtt[h].set_text(str(sales_results[0][h][6]))
        elif len(sales_results[0]) == 0:
            for i in range(0, len(sales_results[0]), 1):
                self.product_label[i].set_active(i)
                self.opening_meter[i].set_text("")
                self.closing_meter[i].set_text("")
                self.rtt[i].set_text("")
                self.show_all()

        if len(sales_results[1]) > 0:
            self.airtel_sending.set_text(str(sales_results[1][0][3]))
            self.airtel_withdraw.set_text(str(sales_results[1][0][4]))
            self.mtn_sending.set_text(str(sales_results[1][0][5]))
            self.mtn_withdraw.set_text(str(sales_results[1][0][6]))
        elif len(sales_results[1]) == 0:
            self.airtel_sending.set_text("")
            self.airtel_withdraw.set_text("")
            self.mtn_sending.set_text("")
            self.mtn_withdraw.set_text("")

        self.prepnarray.clear()
        self.prepaarray.clear()
        if len(sales_results[2]) > 0:
            for p in range(0, len(sales_results[2]), 1):
                real_insert(self.prepnarray, p, sales_results[2][p][3])
                real_insert(self.prepaarray, p, sales_results[2][p][4])
                self.prepaid.set_text(str(add_array(self.prepaarray, p)))
        else:
            self.prepaid.set_text("")

        if len(sales_results[3]) > 0:
            self.expense_row.set_text(str(len(sales_results[3])))
            for ex in range(0, len(sales_results[3]), 1):
                self.exp_name[ex].set_text(str(sales_results[3][ex][3]))
                self.exp[ex].set_text(str(sales_results[3][ex][4]))
        elif len(sales_results[3]) == 0:
            self.expense_row.set_text("")
        if len(sales_results[4]) > 0:
            self.debtor_row.set_text(str(len(sales_results[4])))
            for d in range(0, len(sales_results[4]), 1):
                self.debtor_name[d].set_text(str(sales_results[4][d][3]))
                self.debt_taken[d].set_text(str(sales_results[4][d][4]))
                self.debt_paid[d].set_text(str(sales_results[4][d][5]))
        elif len(sales_results[4]) == 0:
            self.debtor_row.set_text("")

        if len(sales_results[5]) > 0:
            self.lub_row.set_text(str(len(sales_results[5])))
            for l in range(0, len(sales_results[5]), 1):
                self.lub_name[l].set_text(str(sales_results[5][l][3]))
                self.lub_amount[l].set_text(str(sales_results[5][l][4]))
        elif len(sales_results[5]) == 0:
            self.lub_row.set_text("")

        if len(sales_results[6]) > 0:
            real_insert(self.dip_array, 0, sales_results[6][0][3])
            real_insert(self.dip_array, 1, sales_results[6][0][4])
            real_insert(self.dip_array, 2, sales_results[6][0][5])
            real_insert(self.dip_array, 3, sales_results[6][0][6])
            real_insert(self.dip_array, 4, sales_results[6][0][7])
            real_insert(self.dip_array, 5, sales_results[6][0][8])
        elif len(sales_results[6]) == 0:
            self.dip_array.clear()

        if len(sales_results[7]) > 0:
            self.cash.set_text(str(sales_results[7][0][3]))
            self.bank.set_text(str(sales_results[7][0][4]))
        elif len(sales_results[7]) == 0:
            self.cash.set_text("")
            self.bank.set_text("")
        self.stop_spinner()

    def stop_spinner(self):
        self.progress.stop()

    def add_prepaid_details(self, widget):
        prep_window = Gtk.Dialog("Prepaid", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL,
                                                                          Gtk.ResponseType.CANCEL,
                                                                          Gtk.STOCK_OK,
                                                                          Gtk.ResponseType.OK))

        prep_window.set_default_size(500, 500)
        prep_window.set_border_width(40)
        box = prep_window.get_content_area()
        grid = Gtk.Grid(column_spacing=3, row_spacing=10)
        box.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label("Name"), 0, 2, 1, 1)
        grid.attach(Gtk.Label("Amount"), 2, 2, 1, 1)
        for i in range(0, 5, 1):
            self.prep_name.append(Gtk.Entry())
            self.prep_name[i].set_margin_left(20)
            self.prep_name[i].set_placeholder_text("Name")
            self.prep_name[i].connect("changed", self.prepaid_caller, i)
            grid.attach(self.prep_name[i], 0, 4 + 2 * i, 1, 1)
            self.prep_amount.append(Gtk.Entry())
            self.prep_amount[i].set_placeholder_text("Amount")
            self.prep_amount[i].connect("changed", self.prepaid_caller, i)
            grid.attach(self.prep_amount[i], 2, 4 + 2 * i, 1, 1)
            try:
                self.prep_name[i].set_text(self.prepnarray[i])
                self.prep_amount[i].set_text(str(self.prepaarray[i]))
            except IndexError:
                pass
        prep_window.show_all()
        response = prep_window.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            cancel("prepaid")
        prep_window.destroy()

    def prepaid_caller(self, widget, choice):
        if len(self.prep_name[choice].get_text()) and len(self.prep_amount[choice].get_text()) > 0:
            self.prepaid.set_text(prepaid(choice, self.prep_name[choice].get_text()
                                          , self.prep_amount[choice].get_text()))
            real_insert(self.prepnarray, choice, self.prep_name[choice].get_text())
            real_insert(self.prepaarray, choice, self.prep_amount[choice].get_text())

    def cash_caller(self, widget):
        if len(self.cash.get_text()) and len(self.bank.get_text()) > 0:
            cash(0, self.cash.get_text(), self.bank.get_text())

    def lubricants_rows(self, widget):
        """
        Adding the lubricants rows
        """
        if len(self.lub_name) > 0:
            for n in range(0, len(self.lub_name), 1):
                self.grid.remove(self.lub_name[n])
                self.grid.remove(self.lub_amount[n])
            self.grid.remove(self.lub_total)
        self.grid.attach(Gtk.Label("Name"), 10, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Amount"), 12, self.y + 20, 1, 1)
        try:
            for i in range(0, int(self.lub_row.get_text()), 1):
                self.lub_name.append(Gtk.Entry.new())
                self.lub_name[i].set_margin_left(20)
                self.lub_name[i].connect("changed", self.lubricants_caller, i)
                self.lub_name[i].set_placeholder_text("Name")
                self.grid.attach(self.lub_name[i], 10, self.y + 22 + 2 * i, 1, 1)
                self.lub_amount.append(Gtk.Entry.new())
                self.lub_amount[i].set_placeholder_text("Amount")
                self.lub_amount[i].connect("changed", self.lubricants_caller, i)
                self.grid.attach(self.lub_amount[i], 12, self.y + 22 + 2 * i, 1, 1)
            self.lub_total.set_placeholder_text("Total")
            self.grid.attach(self.lub_total, 12, self.y + 22 + 2 * (int(self.lub_row.get_text()) + 1), 1, 1)
            self.show_all()
        except ValueError:
            pass

    def lubricants_caller(self, widget, choice):
        if len(self.lub_name[choice].get_text()) and len(self.lub_amount[choice].get_text()) > 0:
            self.lub_total.set_text(lubricants(choice, self.lub_name[choice].get_text(),
                                               self.lub_amount[choice].get_text()))

    def settings(self, widget):
        """
        this is the function for displaying settings in the app
        """
        settings_window = Gtk.Dialog("Settings", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL,
                                                                               Gtk.ResponseType.CANCEL,
                                                                               Gtk.STOCK_OK,
                                                                               Gtk.ResponseType.OK))
        settings_window.set_default_size(700, 500)
        settings_window.set_border_width(40)
        box = settings_window.get_content_area()
        settings_panel = Gtk.Paned()
        box.pack_start(settings_panel, True, True, 0)
        settings_window.show_all()

        response = settings_window.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        settings_window.destroy()

    def dips_window(self, widget):
        """
        This is the dips window
        """
        dip_window = Gtk.Dialog("Dips", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL,
                                                                      Gtk.ResponseType.CANCEL,
                                                                      Gtk.STOCK_OK,
                                                                      Gtk.ResponseType.OK))
        dip_window.set_default_size(600, 400)
        dip_window.set_border_width(40)
        box = dip_window.get_content_area()
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
        self.pms_od.connect('changed', lambda widget:
        self.pms_dp.set_text(str(float(self.pms_od.get_text()) - float(self.pms_cd.get_text()))))
        self.pms_cd.connect("changed", lambda widget:
        self.pms_dp.set_text(str(float(self.pms_od.get_text()) - float(self.pms_cd.get_text()))))
        self.pms_dp.connect("changed", lambda widget: dips_total.set_text(
            float(self.pms_dp.get_text()) + float(self.ago_dp.get_text()) +
            float(self.bik_dp.get_text())))
        grid.attach(self.pms_cd, 6, 2, 1, 1)

        grid.attach(self.pms_dp, 8, 2, 1, 1)

        grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
        self.ago_od.set_placeholder_text("opening dips")
        self.ago_cd.set_placeholder_text("closing dips")
        self.ago_dp.set_placeholder_text("difference")
        grid.attach(self.ago_od, 4, 4, 1, 1)
        self.ago_od.connect('changed', lambda widget:
        self.ago_dp.set_text(str(float(self.ago_od.get_text()) - float(self.ago_cd.get_text()))))
        self.ago_cd.connect("changed", lambda widget:
        self.ago_dp.set_text(str(float(self.ago_od.get_text()) - float(self.ago_cd.get_text()))))
        self.ago_dp.connect("changed", lambda widget: dips_total.set_text(
            float(self.pms_dp.get_text()) + float(self.ago_dp.get_text()) +
            float(self.bik_dp.get_text())))
        grid.attach(self.ago_cd, 6, 4, 1, 1)
        grid.attach(self.ago_dp, 8, 4, 1, 1)

        grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)
        self.bik_od.set_placeholder_text("opening_dips")
        self.bik_cd.set_placeholder_text("closing_dips")
        self.bik_dp.set_placeholder_text("difference")

        grid.attach(self.bik_od, 4, 6, 1, 1)
        self.bik_od.connect('changed', lambda widget:
        self.bik_dp.set_text(str(float(self.bik_od.get_text()) - float(self.bik_cd.get_text()))))
        self.bik_cd.connect('changed', lambda widget:
        self.bik_dp.set_text(str(float(self.bik_od.get_text()) - float(self.bik_cd.get_text()))))
        self.bik_dp.connect("changed", lambda widget: dips_total.set_text(
            float(self.pms_dp.get_text()) + float(self.ago_dp.get_text()) +
            float(self.bik_dp.get_text())))
        grid.attach(self.bik_cd, 6, 6, 1, 1)
        grid.attach(self.bik_dp, 8, 6, 1, 1)
        grid.attach(dips_total, 8, 8, 1, 1)
        try:
            self.pms_od.set_text(str(self.dip_array[0]))
            self.pms_cd.set_text(str(self.dip_array[1]))
            self.ago_od.set_text(str(self.dip_array[2]))
            self.ago_cd.set_text(str(self.dip_array[3]))
            self.bik_od.set_text(str(self.dip_array[4]))
            self.bik_cd.set_text(str(self.dip_array[5]))
            dips_total.set_text(str(add_array(self.totaldips, 2)))
        except IndexError:
            pass
        dip_window.show_all()

        response = dip_window.run()
        if response == Gtk.ResponseType.OK:
            self.dips_caller()
        elif response == Gtk.ResponseType.CANCEL:
            cancel("dips")
        dip_window.destroy()

    def fuel_purchase_window(self, widget):
        fuel_window = Gtk.Dialog("Fuel Purchase", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL,
                                                                                Gtk.ResponseType.CANCEL,
                                                                                Gtk.STOCK_OK,
                                                                                Gtk.ResponseType.OK))

        fuel_window.set_default_size(600, 400)
        fuel_window.set_border_width(40)
        box = fuel_window.get_content_area()
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
                               self.pms_total.set_text(str(int(self.pms.get_text()) * int(self.pms_price.get_text()))))
        grid.attach(self.pms_price, 6, 2, 1, 1)
        self.pms_total.set_placeholder_text("total")
        self.pms_total.connect("changed", lambda widget: total.set_text(str(int(self.pms_total.get_text()))))
        grid.attach(self.pms_total, 8, 2, 1, 1)

        grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
        self.ago.set_placeholder_text("litres")
        grid.attach(self.ago, 4, 4, 1, 1)
        self.ago_price.connect('changed',
                               lambda widget:
                               self.ago_total.set_text(str(int(self.ago.get_text()) * int(self.ago_price.get_text()))))
        self.ago_price.set_placeholder_text("price")
        grid.attach(self.ago_price, 6, 4, 1, 1)
        self.ago_total.set_placeholder_text("total")
        self.ago_total.connect("changed", lambda widget: total.set_text(str(int(total.get_text()) +
                                                                            int(self.ago_total.get_text()))))

        grid.attach(self.ago_total, 8, 4, 1, 1)

        grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)
        self.bik.set_placeholder_text("litres")
        grid.attach(self.bik, 4, 6, 1, 1)

        self.bik_price.set_placeholder_text("price")
        self.bik_price.connect('changed',
                               lambda widget:
                               self.bik_total.set_text(str(int(self.bik.get_text()) * int(self.bik_price.get_text()))))
        grid.attach(self.bik_price, 6, 6, 1, 1)

        self.bik_total.set_placeholder_text("total")
        self.bik_total.connect("changed", lambda widget: total.set_text(str(int(total.get_text()) +
                                                                            int(self.bik_total.get_text()))))
        grid.attach(self.bik_total, 8, 6, 1, 1)
        total.set_placeholder_text("total")
        grid.attach(total, 8, 8, 1, 1)

        fuel_window.show_all()

        response = fuel_window.run()
        if response == Gtk.ResponseType.OK:
            self.fuel_purchase_caller()
        elif response == Gtk.ResponseType.CANCEL:
            cancel("fuel-purchases")
        fuel_window.close()

    def dips_caller(self, widget):
        if len(self.pms_od.get_text()) and len(self.pms_cd.get_text()) and \
                len(self.ago_od.get_text()) and len(self.ago_cd.get_text()) \
                and len(self.bik_od.get_text()) and len(self.bik_cd.get_text()) > 0:
            dips(self.pms_od.get_text(), self.pms_cd.get_text(), self.ago_od.get_text(),
                 self.ago_cd.get_text(), self.bik_od.get_text(), self.bik_cd.get_text())

    def fuel_purchase_caller(self, widget):
        if len(self.pms.get_text()) and len(self.pms_price.get_text()) and \
                len(self.ago.get_text()) and len(self.ago_price.get_text()) \
                and len(self.bik.get_text()) and len(self.bik_price.get_text()) > 0:
            fuel_purchase(self.pms.get_text(), self.pms_price.get_text(), self.ago.get_text(),
                          self.ago_price.get_text(), self.bik.get_text(), self.bik_price.get_text())

    def product_change(self, combo, k):
        """
        this function is for storing the selected product into an array
        """
        global model
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
        real_insert(self.product_changed, k, model[tree_iter][0])
        self.sales_litres_caller(combo, k)

    def expense_rows(self, widget):
        """
        this function helps to add rows for expenses
        """
        if len(self.exp_name) > 0:
            for n in range(0, len(self.exp_name), 1):
                self.grid.remove(self.exp_name[n])
                self.grid.remove(self.exp[n])
            self.grid.remove(self.expense_total)
        self.grid.attach(Gtk.Label("Expense"), 0, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Amount"), 2, self.y + 20, 1, 1)
        try:
            for i in range(0, int(self.expense_row.get_text()), 1):
                self.exp_name.append(Gtk.Entry())
                self.exp_name[i].connect("changed", self.expense_caller, i)
                self.exp_name[i].set_placeholder_text("Expense")
                self.grid.attach(self.exp_name[i], 0, self.y + 22 + 2 * i, 1, 1)
                self.exp.append(Gtk.Entry())
                self.exp[i].set_placeholder_text("Amount")
                self.exp[i].connect("changed", self.expense_caller, i)
                self.grid.attach(self.exp[i], 2, self.y + 22 + 2 * i, 1, 1)
            self.expense_total.set_placeholder_text("Total")
            self.grid.attach(self.expense_total, 2, self.y + 22 + 2 * (int(self.expense_row.get_text()) + 1), 1, 1)
            self.show_all()
        except ValueError:
            pass

    def debtors_rows(self, widget):
        """
         this is the debtors function for storing the debtors
        """
        if len(self.debtor_name) > 0:
            for n in range(0, len(self.debtor_name), 1):
                self.grid.remove(self.debtor_name[n])
                self.grid.remove(self.debt_taken[n])
                self.grid.remove(self.debt_paid[n])
            self.grid.remove(self.debt_paid_total)
            self.grid.remove(self.debt_taken_total)
        self.grid.attach(Gtk.Label("Name"), 4, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Debt Taken"), 6, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Debt Paid"), 8, self.y + 20, 1, 1)

        try:
            for i in range(0, int(self.debtor_row.get_text()), 1):
                self.debtor_name.append(Gtk.Entry())
                self.debtor_name[i].set_placeholder_text("Debtor")
                self.debtor_name[i].connect("changed", self.debtor_caller, i)
                self.debtor_name[i].set_margin_left(20)
                self.grid.attach(self.debtor_name[i], 4, self.y + 22 + 2 * i, 1, 1)

                self.debt_taken.append(Gtk.Entry())
                self.debt_taken[i].set_placeholder_text("Debt")
                self.debt_taken[i].connect("changed", self.debtor_caller, i)
                self.grid.attach(self.debt_taken[i], 6, self.y + 22 + 2 * i, 1, 1)

                self.debt_paid.append(Gtk.Entry())
                self.debt_paid[i].set_placeholder_text("Paid")
                self.debt_paid[i].connect("changed", self.debtor_caller, i)
                self.grid.attach(self.debt_paid[i], 8, self.y + 22 + 2 * i, 1, 1)

            self.debt_taken_total.set_placeholder_text("Debt_taken")
            self.grid.attach(self.debt_taken_total,
                             6, self.y + 22 + 2 * (int(self.debtor_row.get_text()) + 1),
                             1, 1)
            self.debt_paid_total.set_placeholder_text("Paid_debt")
            self.grid.attach(self.debt_paid_total, 8
                             , self.y + 22 + 2 * (int(self.debtor_row.get_text()) + 1), 1, 1)
            self.show_all()
        except ValueError:
            pass

    def debtor_caller(self, widget, choice):
        """
        this function is called inorder to store a row of debtors to a database
        """
        if len(self.debtor_name[choice].get_text()) and len(self.debt_taken[choice].get_text()) & \
                len(self.debt_paid[choice].get_text()) > 0:
            debtor_total = debtors(choice, self.debtor_name[choice].get_text(),
                                   self.debt_taken[choice].get_text(),
                                   self.debt_paid[choice].get_text())
            self.debt_paid_total.set_text(str(debtor_total[0]))
            self.debt_taken_total.set_text(str(debtor_total[1]))

    def expense_caller(self, widget, choice):
        """
        this function gets data from the expense table and stores it into the database

        """
        if len(self.exp_name[choice].get_text()) and len(self.exp[choice].get_text()) > 0:
            self.expense_total.set_text(expenses(choice, self.exp_name[choice].get_text(),
                                                 self.exp[choice].get_text()))

    def sales_litres_caller(self, widget, choice):
        """
         this function takes in the opening meter, closing meter ,rtt to return the litres sold
        """
        if len(self.product_changed[choice]) and len(self.opening_meter[choice].get_text()) and \
                len(self.closing_meter[choice].get_text()) and len(self.rtt[choice].get_text()) > 0:
            self.litres[choice].set_text(sales_litres(choice, self.product_changed[choice],
                                                      self.opening_meter[choice].get_text(),
                                                      self.closing_meter[choice].get_text(),
                                                      self.rtt[choice].get_text()))

    def sales_shs_caller(self, widget, choice):
        """
        this function is for calculating and storing the amount of fuel sold
        :param event: this is to specify which event was passed to the function
        :param widget: this is used to carry the properties of gtk entry widget
        :param choice: this is used to carry the exact element in the list
        """
        if len(self.litres[choice].get_text()) and len(self.price[choice].get_text()) > 0:
            result = sales_shs(choice, self.litres[choice].get_text(),
                               self.price[choice].get_text())
            self.amount[choice].set_text(result[0])
            self.total_amount.set_text(result[1])

    def save(self, widget):
        dialog = Gtk.Dialog("Sales Summary", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_position(Gtk.WindowPosition.CENTER)
        dialog.set_default_size(500, 500)
        label = Gtk.Label()
        label.set_text("totalsales:" + str(self.total_amount.get_text()) + "\n"
                       + "paid-debt:" + str(self.debt_paid_total.get_text()))
        box = dialog.get_content_area()
        box.pack_start(label, True, True, 0)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        dialog.close()
