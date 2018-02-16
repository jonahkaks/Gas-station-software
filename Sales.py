import gi

from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Sales(Gtk.ApplicationWindow):
    """
    here is the sales window which comes after the login window
    """

    def __init__(self, y, *args, **kwargs):
        super(Sales, self).__init__(*args, **kwargs)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.y = y
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

        self.settings_button = Gtk.MenuItem("Settings")
        self.settings_button.connect("activate", self.settings)
        self.menubar.append(self.settings_button)

        self.box.pack_start(self.menubar, False, False, 0)
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
            self.rtt[n].set_placeholder_text("rtt")
            self.rtt[n].connect('changed', self.sales_litres_caller, n)
            self.grid.attach(self.rtt[n], 6, 3 + n, 1, 1)

            self.litres.append(Gtk.Entry())
            self.litres[n].set_placeholder_text('litres')
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
        self.grid.attach(Gtk.Label('Bank'), 4, y + 10, 1, 1)
        self.cash = Gtk.Entry()
        self.cash.set_placeholder_text("cash")
        self.grid.attach(self.cash, 6, y + 8, 1, 1)

        self.bank = Gtk.Entry()
        self.bank.set_placeholder_text("banked")
        self.grid.attach(self.bank, 6, y + 10, 1, 1)

        self.expense_row = Gtk.Entry()
        self.expense_row.set_placeholder_text("Enter rows")

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
        self.expense_button = Gtk.Button(label="Add expense")
        self.expense_button.set_margin_top(30)
        self.expense_row.set_margin_top(30)
        self.expense_button.connect("clicked", self.expense_rows)
        self.grid.attach(self.expense_button, 2, y + 18, 1, 1)
        self.grid.attach(self.expense_row, 0, y + 18, 1, 1)
        self.debtor_row = Gtk.Entry()
        self.debtor_row.set_placeholder_text("Enter rows")
        """
        Adding the debtors rows is done here
        """
        self.debtor_button = Gtk.Button(label="Add Debtors")
        self.debtor_button.connect("clicked", self.debtors_rows)
        self.debtor_row.set_margin_top(30)
        self.debtor_row.set_margin_left(20)
        self.debtor_button.set_margin_top(30)
        self.grid.attach(self.debtor_row, 4, y + 18, 1, 1)
        self.grid.attach(self.debtor_button, 6, y + 18, 1, 1)

        """
        Adding the lubricants area
        """
        self.lub_row = Gtk.Entry()
        self.lub_row.set_placeholder_text("Add row")
        self.lub_row.set_margin_top(30)
        self.lub_row.set_margin_left(20)
        self.lub_button = Gtk.Button(label="Lubricants")
        self.lub_button.set_margin_top(30)
        self.lub_button.connect("clicked", self.lubricants_rows)
        self.grid.attach(self.lub_row, 10, y + 18, 1, 1)
        self.grid.attach(self.lub_button, 12, y + 18, 1, 1)
        self.lub_name = []
        self.lub_amount = []
        self.lub_total = Gtk.Entry()
        year, month, date = self.calender.get_date()
        real_insert(sales_date, 0, str(date) + "/" + str(month + 1) + "/" + str(year))
        self.changed_day()

    def mobile_caller(self, widget):
        if len(self.airtel_sending.get_text()) and len(self.airtel_withdraw.get_text()) and \
                len(self.mtn_sending.get_text()) and len(self.mtn_withdraw.get_text()) > 0: \
                mobile_money(0, self.airtel_sending.get_text(), self.airtel_withdraw.get_text(),
                             self.mtn_sending.get_text(), self.mtn_withdraw.get_text())

    def day_select(self, widget):
        """
         this function is for getting and storing a date
        """

        year, month, date = self.calender.get_date()
        real_insert(sales_date, 0, str(date) + "/" + str(month + 1) + "/" + str(year))

        self.changed_day()

    def changed_day(self):
        sales_results = get_details()[0]
        for i in range(0, len(sales_results), 1):
            if len(sales_results) == 3:
                self.product_label[i].set_active(2 * i)
            else:
                self.product_label[i].set_active(i)
            self.opening_meter[i].set_text(str(sales_results[i][4]))
            self.closing_meter[i].set_text(str(sales_results[i][5]))
            self.rtt[i].set_text(str(sales_results[i][6]))
        try:
            mobile_results = get_details()[1]
            self.airtel_sending.set_text(str(mobile_results[0][3]))
            self.airtel_withdraw.set_text(str(mobile_results[0][4]))
            self.mtn_sending.set_text(str(mobile_results[0][5]))
            self.mtn_withdraw.set_text(str(mobile_results[0][6]))
        except IndexError:
            pass

        try:
            prepaid = get_details()[2]
            for p in range(0, len(prepaid), 1):
                self.prep_name[p].set_text(str(prepaid[p][3]))
                self.prep_amount[p].set_text(str(prepaid[p][4]))

        except IndexError:
            pass

        try:
            expense_results = get_details()[3]
            if len(expense_results) > 0:
                self.expense_row.set_text(str(len(expense_results)))
                self.expense_rows("wigdet")
            for ex in range(0, len(expense_results), 1):
                self.exp_name[ex].set_text(str(expense_results[ex][3]))
                self.exp[ex].set_text(str(expense_results[ex][4]))

        except IndexError:
            pass
        try:
            debtor_results = get_details()[4]
            if len(debtor_results) > 0:
                self.debtor_row.set_text(str(len(debtor_results)))
                self.debtors_rows("wigdet")
            for d in range(0, len(debtor_results), 1):
                self.debtor_name[d].set_text(str(debtor_results[d][3]))
                self.debt_taken[d].set_text(str(debtor_results[d][4]))
                self.debt_paid[d].set_text(str(debtor_results[d][5]))
        except IndexError:
            pass

        try:
            lub_results = get_details()[5]
            if len(lub_results) > 0:
                self.lub_row.set_text(str(len(lub_results)))
                self.lubricants_rows("wigdet")
            for l in range(0, len(lub_results), 1):
                self.lub_name[l].set_text(str(lub_results[l][3]))
                self.lub_amount[l].set_text(str(lub_results[l][4]))
        except IndexError:
            pass

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
            self.prep_name[i].connect("changed", self.prepaid_caller, i)
            self.prep_name[i].set_placeholder_text("Name")
            grid.attach(self.prep_name[i], 0, 4 + 2 * i, 1, 1)
            self.prep_amount.append(Gtk.Entry())
            self.prep_amount[i].set_placeholder_text("Amount")
            self.prep_amount[i].connect("changed", self.prepaid_caller, i)
            grid.attach(self.prep_amount[i], 2, 4 + 2 * i, 1, 1)
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

    def lubricants_rows(self, widget):
        """
        Adding the lubricants rows
        """
        self.grid.attach(Gtk.Label("Name"), 10, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Amount"), 12, self.y + 20, 1, 1)
        for i in range(0, int(self.lub_row.get_text()), 1):
            self.lub_name.append(Gtk.Entry())
            self.lub_name[i].set_margin_left(20)
            self.lub_name[i].connect("changed", self.lubricants_caller, i)
            self.lub_name[i].set_placeholder_text("Name")
            self.grid.attach(self.lub_name[i], 10, self.y + 22 + 2 * i, 1, 1)
            self.lub_amount.append(Gtk.Entry())
            self.lub_amount[i].set_placeholder_text("Amount")
            self.lub_amount[i].connect("changed", self.lubricants_caller, i)
            self.grid.attach(self.lub_amount[i], 12, self.y + 22 + 2 * i, 1, 1)
        self.lub_total.set_placeholder_text("Total")
        self.grid.attach(self.lub_total, 12, self.y + 22 + 2 * (int(self.lub_row.get_text()) + 1), 1, 1)
        self.show_all()

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

        pms_od = Gtk.Entry()
        pms_od.set_placeholder_text("opening dips")
        pms_cd = Gtk.Entry()
        pms_cd.set_placeholder_text("closing dips")
        pms_dp = Gtk.Entry()
        pms_dp.set_placeholder_text("difference")
        dips_total = Gtk.Entry()

        grid.attach(pms_od, 4, 2, 1, 1)
        pms_cd.connect('changed', lambda widget: pms_dp.set_text(dips(0,
                                                                      pms_od.get_text(),
                                                                      pms_cd.get_text())))
        pms_dp.connect("changed", lambda widget: dips_total.set_text(pms_dp.get_text()))
        grid.attach(pms_cd, 6, 2, 1, 1)

        grid.attach(pms_dp, 8, 2, 1, 1)

        grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
        ago_od = Gtk.Entry()
        ago_od.set_placeholder_text("opening dips")
        ago_cd = Gtk.Entry()
        ago_cd.set_placeholder_text("closing dips")
        ago_dp = Gtk.Entry()
        grid.attach(ago_od, 4, 4, 1, 1)
        ago_cd.connect('changed',
                       lambda widget: ago_dp.set_text(dips(1, ago_od.get_text(), ago_cd.get_text())))
        ago_dp.connect("changed",
                       lambda widget: dips_total.set_text(str(int(dips_total.get_text()) + int(ago_dp.get_text()))))
        grid.attach(ago_cd, 6, 4, 1, 1)
        grid.attach(ago_dp, 8, 4, 1, 1)

        grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)
        bik_od = Gtk.Entry()
        bik_cd = Gtk.Entry()
        bik_dp = Gtk.Entry()

        grid.attach(bik_od, 4, 6, 1, 1)

        bik_cd.connect('changed', lambda widget: bik_dp.set_text(dips(2,
                                                                      bik_od.get_text(),
                                                                      bik_cd.get_text())))
        bik_dp.connect("changed", lambda widget: dips_total.set_text(str(int(dips_total.get_text()) +
                                                                         int(bik_dp.get_text()))))
        grid.attach(bik_cd, 6, 6, 1, 1)
        grid.attach(bik_dp, 8, 6, 1, 1)
        grid.attach(dips_total, 8, 8, 1, 1)
        dip_window.show_all()

        response = dip_window.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
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
        pms = Gtk.Entry()
        pms_price = Gtk.Entry()
        pms_total = Gtk.Entry()
        pms.set_placeholder_text("litres")
        grid.attach(pms, 4, 2, 1, 1)
        pms_price.set_placeholder_text("price")
        pms_price.connect('changed',
                          lambda widget:
                          pms_total.set_text(str(int(pms.get_text()) * int(pms_price.get_text()))))
        grid.attach(pms_price, 6, 2, 1, 1)
        pms_total.set_placeholder_text("total")
        pms_total.connect("changed", lambda widget: total.set_text(str(int(pms_total.get_text()))))
        grid.attach(pms_total, 8, 2, 1, 1)

        grid.attach(Gtk.Label("AGO"), 2, 4, 1, 1)
        ago = Gtk.Entry()
        ago_price = Gtk.Entry()
        ago_total = Gtk.Entry()
        ago.set_placeholder_text("litres")
        grid.attach(ago, 4, 4, 1, 1)
        ago_price.connect('changed',
                          lambda widget:
                          ago_total.set_text(str(int(ago.get_text()) * int(ago_price.get_text()))))
        ago_price.set_placeholder_text("price")
        grid.attach(ago_price, 6, 4, 1, 1)
        ago_total.set_placeholder_text("total")
        ago_total.connect("changed", lambda widget: total.set_text(str(int(total.get_text()) +
                                                                       int(ago_total.get_text()))))

        grid.attach(ago_total, 8, 4, 1, 1)

        grid.attach(Gtk.Label("BIK"), 2, 6, 1, 1)
        bik = Gtk.Entry()
        bik_price = Gtk.Entry()
        bik_total = Gtk.Entry()
        bik.set_placeholder_text("litres")
        grid.attach(bik, 4, 6, 1, 1)

        bik_price.set_placeholder_text("price")
        bik_price.connect('changed',
                          lambda widget:
                          bik_total.set_text(str(int(bik.get_text()) * int(bik_price.get_text()))))
        grid.attach(bik_price, 6, 6, 1, 1)

        bik_total.set_placeholder_text("total")
        bik_total.connect("changed", lambda widget: total.set_text(str(int(total.get_text()) +
                                                                       int(bik_total.get_text()))))
        grid.attach(bik_total, 8, 6, 1, 1)
        total.set_placeholder_text("total")
        grid.attach(total, 8, 8, 1, 1)

        fuel_window.show_all()

        response = fuel_window.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            cancel("fuel-purchases")
        fuel_window.close()

    def product_change(self, combo, k):
        """
        this function is for storing the selected product into an array
        """
        if len(sales_date) == 0:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Please Select a date")
            dialog.run()
            dialog.destroy()
        else:
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
        self.grid.attach(Gtk.Label("Expense"), 0, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Amount"), 2, self.y + 20, 1, 1)
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

    def debtors_rows(self, widget):
        """
         this is the debtors function for storing the debtors
        """
        self.grid.attach(Gtk.Label("Name"), 4, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Debt Taken"), 6, self.y + 20, 1, 1)
        self.grid.attach(Gtk.Label("Debt Paid"), 8, self.y + 20, 1, 1)

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

    @staticmethod
    def replace_widget(old, new):
        parent = old.get_parent()

        props = {}
        for key in Gtk.ContainerClass.list_child_properties(type(parent)):
            props[key.name] = parent.child_get_property(old, key.name)

        parent.remove(old)
        parent.add(new)

        for name, value in props.iteritems():
            parent.child_set_property(new, name, value)

    def save(self, widget):
        dialog = Gtk.Dialog("Sales Summary", self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_position(Gtk.WindowPosition.CENTER);
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
