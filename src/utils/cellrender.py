#! /usr/bin/env python
# -*- encoding:utf-8 -*-
# 文件名:cellrenderbutton.py
"""Test code

Description:________
"""
__version__ = "0.1"
__date__ = "2009-02-20 15:38:24"
__author__ = "Mingxi Wu <fengshenx@gmail.com> "
__license__ = "Licensed under the GPL v2, see the file LICENSE in this tarball."
__copyright__ = "Copyright (C) 2009 by Mingxi Wu <fengshenx@gmail.com>."
# =================================================================================#
# ChangeLog
# 2009-11-18
# TualatriX, make it can accept text data

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject


class CellRendererButton(gtk.CellRenderer):
    __gsignals__ = {
        'clicked': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
    }

    __gproperties__ = {
        'text': (gobject.TYPE_STRING, 'Text', 'Text for button', '', gobject.PARAM_READWRITE)
    }
    _button_width = 10
    _button_height = 10

    def __init__(self, text=None):
        gtk.CellRenderer.__init__(self)

        self.text = text
        self.set_property('mode', gtk.CellRendererMode.ACTIVATABLE)

    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def do_get_size(self, widget, cell_area):
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
        wid.get_style().paint_layout(window, state, shadow, cell_area,
                                     wid, "button",
                                     cell_area.x + x + xpad,
                                     cell_area.y + y + ypad,
                                     w - 6, h - 6)
        flags = flags & gtk.CellRendererState.SELEdCTED
        gtk.CellRendererText.do_render(self, window, wid, bg_area,
                                       (cell_area[0], cell_area[1] + ypad, cell_area[2], cell_area[3]), expose_area,
                                       flags)

    def do_activate(self, event, widget, path, background_area, cell_area, flags):
        self.emit('clicked', path)


gobject.type_register(CellRendererButton)
