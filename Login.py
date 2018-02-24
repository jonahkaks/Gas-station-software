import gi

from Sales import Sales
from definitions import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Login(Gtk.ApplicationWindow):
    """
this is the login window of the application that takes the username and password and
authenticates a user
    """

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.sales_window = None
        self.set_border_width(150)
        self.set_default_size(500, 500)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                           spacing=50)
        self.add(self.box)
        self.username = Gtk.Entry()
        self.username.set_placeholder_text('username')
        self.box.pack_start(self.username, True, True, 0)

        self.password = Gtk.Entry()
        self.password.set_placeholder_text('password')
        self.password.set_visibility(False)
        self.password.connect("activate", self.controller)
        self.box.pack_start(self.password, True, True, 0)

        self.button = Gtk.Button(label='Login')
        self.button.connect('clicked', self.controller)
        self.box.pack_start(self.button, True, True, 0)

        self.label = Gtk.Label()
        self.box.pack_start(self.label, True, True, 0)

    def controller(self, widget):
        """
        this is the function that is used to login into the sales window
        :param widget: this gets the clicked button to authenticate a user
        """
        allowed = login(self.username.get_text(), self.password.get_text())

        while not allowed:
            self.label.set_markup("<span color=\'red\'><b><i>Invalid login try again</i></b></span>")
            self.show_all()
            return 0
        self.sales_window = Sales(allowed[1])
        self.sales_window.set_title(allowed[0].upper() + " DAY BOOK")
        self.sales_window.set_application(self.get_application())
        self.destroy()
