# Copyright (C) 2018 jonahk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Gio
from src.Login import Login

MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <menu id="app-menu">
        <section>
            <item>
                <attribute name="action">app.new</attribute>
                <attribute name="label" translatable="yes">_New</attribute>
            </item>
            <item>
                <attribute name="action">app.about</attribute>
                <attribute name="label" translatable="yes">_About</attribute>
            </item>
            <item>
                <attribute name="action">app.help</attribute>
                <attribute name="label" translatable="yes">_Help</attribute>
            </item>
            <item>
                <attribute name="action">app.commandline</attribute>
                <attribute name="label" translatable="yes">_CommandLine</attribute>
            </item>
            <item>
                <attribute name="action">app.quit</attribute>
                <attribute name="label" translatable="yes">_Quit</attribute>
            </item>
        </section>
    </menu>
</interface>
"""


class Application(Gtk.Application):
    """
      this is the main application control logic where all the windows take in
    """

    def __init__(self, **kwargs):
        super(Application, self).__init__(application_id="org.gnome.Gas-Station-Software",
                                          flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                                          **kwargs)

        self.window = None
        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)
        GLib.set_application_name("Gas-Station-Software")
        GLib.set_prgname("org.gnome.Gas-Station-Software")

    def __repr__(self):
        return '<Application>'

    def do_activate(self):
        """
        this application function is used to activate the login window when the app is started

        """
        self.window = Login()
        self.window.set_title("Login")
        self.window.set_application(self)
        self.window.show_all()

    def new_window(self, action, param):
        self.window = Login()
        self.window.set_title("Login")
        self.window.set_application(self)
        self.window.show_all()

    def do_startup(self):
        """
        this function controls all the application actions and functions

        """
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.new_window)
        self.add_action(action)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("commandline", None)
        self.add_action(action)
        action = Gio.SimpleAction.new("help", None)
        action.connect("activate", self.on_help)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('../data/application.css')
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_USER)

    @staticmethod
    def on_help(action, param):
        Gtk.show_uri(None, "https://github.com/jonahkaks/Gas-Station-Software/blob/master/README.md", Gdk.CURRENT_TIME)

    def on_about(self, action, param):
        """
        this function is used to return the about dialog on if the about button is clicked
        """
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.set_program_name('Gas station')
        about_dialog.set_copyright("Copyright \xc2\xa9 2018 Newton Jonah")
        about_dialog.set_version('0.1.0')
        about_dialog.set_website('https://github.com/jonahkaks/Gas-Station-Software/blob/master/README.md')
        about_dialog.set_website_label("NewtonJonah")
        about_dialog.set_logo_icon_name("gnome-builder")
        about_dialog.set_authors(["Kafeero Jonah", "Kibalama Timothy"])
        about_dialog.set_license("""Gas station is free software: you can redistribute it and/or modify
            it under the terms of the GNU General Public License as published
            by the Free Software Foundation, either version 3 of the License,
            or (at your option) any later version.
            FuelStation is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty
            of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
            See the GNU General Public License for more details.
            You should have received a copy of the GNU General Public License
            along with Software.  If not, see <http://www.gnu.org/licenses/>.""")
        about_dialog.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        if options.contains("test"):
            print("Test argument recieved")
        self.activate()
        return 0

    def on_quit(self, action, param):
        """
        this function is used to destroy the whole application
        """
        self.quit()


def main():
    app = Application()
    return app.run(sys.argv)


if __name__ == '__main__':
    main()
