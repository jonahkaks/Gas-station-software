import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject


class CellRendererButton(gtk.CellRenderer):
    __gproperties__ = {"callable": (gobject.TYPE_PYOBJECT,
                                    "callable property",
                                    "callable property",
                                    gobject.PARAM_READWRITE)}
    _button_width = 10
    _button_height = 10

    def __init__(self):
        gtk.CellRenderer.__init__(self)
        self.set_property("xalign", 0.5)
        self.set_property("mode", gtk.CellRendererMode.ACTIVATABLE)
        self.callable = None
        self.table = None

    # __init__()

    def do_set_property(self, pspec, value):
        if pspec.name == "callable":
            if callable(value):
                self.callable = value
            else:
                raise TypeError("callable property must be callable!")
        else:
            raise AttributeError("Unknown property %s" % pspec.name)

    # do_set_property()

    def do_get_property(self, pspec):
        if pspec.name == "callable":
            return self.callable
        else:
            raise AttributeError("Unknown property %s" % pspec.name)

    # do_get_property()

    def do_get_size(self, wid, cell_area):
        xpad = self.get_property("xpad")
        ypad = self.get_property("ypad")

        if not cell_area:
            x, y = 0, 0
            w = 2 * xpad + self._button_width
            h = 2 * ypad + self._button_height
        else:
            w = 2 * xpad + cell_area.width
            h = 2 * ypad + cell_area.height

            xalign = self.get_property("xalign")
            yalign = self.get_property("yalign")

            x = max(0, xalign * (cell_area.width - w))
            y = max(0, yalign * (cell_area.height - h))

        return x, y, w, h

    # do_get_size()

    def do_render(self, window, wid, bg_area, cell_area, expose_area, flags=True):
        if not window:
            return

        xpad = self.get_property("xpad")
        ypad = self.get_property("ypad")

        x, y, w, h = self.get_size(wid, cell_area)

        # if flags & gtk.CELL_RENDERER_SELECTED :
        # state = gtk.STATE_ACTIVE
        # shadow = gtk.SHADOW_OUT
        if flags & gtk.CellRendererState.PRELIT:
            state = gtk.StateFlags.PRELIGHT
            shadow = gtk.ShadowType.ETCHED_OUT
        else:
            state = gtk.StateFlags.NORMAL
            shadow = gtk.ShadowType.OUT
        wid.get_style().paint_box(window, state, shadow, cell_area,
                                  wid, "button",
                                  cell_area.x + x + xpad,
                                  cell_area.y + y + ypad,
                                  w - 6, h - 6)
        flags = flags & gtk.CellRendererState.SELECTED
        gtk.CellRendererText.do_render(self, window, wid, bg_area,
                                       (cell_area[0], cell_area[1] + ypad, cell_area[2], cell_area[3]), expose_area,
                                       flags)

    # do_render()

    def do_activate(self, event, wid, path, bg_area, cell_area, flags):
        cb = self.get_property("callable")
        if cb is not None:
            cb(path)
        return True


# _CellRendererButton


gobject.type_register(CellRendererButton)
