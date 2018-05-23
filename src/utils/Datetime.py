import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
import datetime
import logging


class CalendarEntry(gtk.Box):
    __gsignals__ = {
        'changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
    }

    def __init__(self):
        gtk.Box.__init__(self, False, 0)
        self.calendar = gtk.Calendar()

        self.button = gtk.ToggleButton(label="v")
        self.button.set_size_request(5, 5)
        self.cwindow = gtk.Window()
        self.display = False
        self.currentDate = datetime.date.today()
        self.entry = gtk.Entry()
        self.entry.set_editable(False)
        self.entry.set_has_frame(False)
        self.cwindow.set_decorated(False)
        self.cwindow.add(self.calendar)
        self.cwindow.set_modal(True)

        self.entry.set_width_chars(10)
        self.pack_start(self.entry, True, True, 0)
        self.pack_start(self.button, False, False, 0)

        self.__connect_signals()
        self.update_entry()

    def __connect_signals(self):
        self.day_selected_handle = self.calendar.connect('day-selected', self.update_entry)
        self.day_selected_double_handle = self.calendar.connect('day-selected-double-click', self.hide_widget)
        self.clicked_handle = self.button.connect('toggled', self.show_widget)
        self.activate = self.entry.connect('activate', self.update_calendar)
        self.focus_out = self.entry.connect('focus-out-event', self.focus_out_event)
        self.keypress = self.entry.connect('key-press-event', self.hide_widget)

    def __block_signals(self):
        self.calendar.handler_block(self.day_selected_handle)
        self.calendar.handler_block(self.day_selected_double_handle)
        self.button.handler_block(self.clicked_handle)
        self.entry.handler_block(self.activate)
        self.entry.handler_block(self.focus_out)

    def __unblock_signals(self):
        self.calendar.handler_unblock(self.day_selected_handle)
        self.calendar.handler_unblock(self.day_selected_double_handle)
        self.button.handler_unblock(self.clicked_handle)
        self.entry.handler_unblock(self.activate)
        self.entry.handler_unblock(self.focus_out)

    def get_text(self):
        return self.entry.get_text()

    def set_date(self, date):
        if not date:
            date = datetime.date.fromtimestamp(time.time())
        self.currentDate = date
        self.__block_signals()
        self.calendar.select_day(1)
        self.calendar.select_month(self.currentDate.month - 1, self.currentDate.year)
        self.calendar.select_day(self.currentDate.day)
        self.__unblock_signals()
        self.update_entry()

    def set_date_text(self, date):
        self.entry.set_text(date)

    def get_date(self):
        return self.currentDate

    def hide_widget(self, *args):
        self.cwindow.hide()
        self.button.set_active(False)

    def show_widget(self, widget):
        if widget.get_active():
            alloc = self.button.get_allocation()
            nreq, req = self.cwindow.get_preferred_size()
            pos, x, y = self.button.get_window().get_origin()
            x += alloc.x
            y += alloc.y
            bwidth = alloc.width
            bheight = alloc.height

            x += bwidth - req.width
            y += bheight

            if x < 0:
                x = 0

            if y < 0:
                y = 0

            self.cwindow.move(x, y)
            self.cwindow.show_all()
        else:
            self.hide_widget()

    def update_entry(self, *args):
        year, month, day = self.calendar.get_date()
        month = month + 1
        self.currentDate = datetime.date(year, month, day)
        text = self.currentDate.strftime("%Y-%m-%d")
        self.entry.set_text(text)
        self.emit('changed', self.currentDate)

    def update_calendar(self, *args):
        try:
            dt = datetime.datetime.strptime(self.entry.get_text(), "%d-%m-%Y")
        except:
            try:
                dt = datetime.datetime.strptime(self.entry.get_text(), "%d-%m-%Y")
            except:
                logging.info('CalendarEntry.update_calendar: Error parsing date, setting it as today...')
                dt = datetime.date.fromtimestamp(datetime.time())

        self.set_date(dt)
        self.hide_widget()
        self.button.set_active(False)

    def focus_out_event(self, *args):
        self.currentDate = self.entry.get_text()
        self.hide_widget()
