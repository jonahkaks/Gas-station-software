import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DialogAccount:
    def __init__(self, account_list, database, row, account, value_list, account_codes, account_types,
                 ctypes, placeholder):
        value = value_list[account]
        self.parent_store = Gtk.ListStore(str)
        builder = Gtk.Builder()
        self.parent_code = None
        builder.add_from_file("../data/dialog-account.glade")
        dialog = builder.get_object("account_dialog")
        self.notebook = builder.get_object("account_notebook")
        self.name_entry = builder.get_object("name_entry")
        self.description_entry = builder.get_object("description_entry")
        self.label = builder.get_object("parent_label")
        self.parent_scroll = builder.get_object("parent_scroll")
        self.list = builder.get_object("type_view")
        self.selection = builder.get_object("treeview-selection")
        self.placeholder = builder.get_object("placeholder")
        self.list1 = builder.get_object("type_view1")
        self.parent = None
        self.selection1 = builder.get_object("treeview-selection1")
        self.account_store = Gtk.ListStore(str)
        self.list1.set_model(self.account_store)
        renderer = Gtk.CellRendererText()
        renderer.set_fixed_size(100, 25)
        column = Gtk.TreeViewColumn("", renderer, text=0)
        self.list1.append_column(column)
        self.list.set_model(self.parent_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("", renderer, text=0)
        self.list.append_column(column)
        self.parent_store.append(["Assets"])
        self.parent_store.append(["Expenses"])
        self.parent_store.append(["Liabilities"])
        self.parent_store.append(["Incomes"])
        self.parent_store.append(["Equity"])

        try:
            self.parent = value.split(":")[0]
            child = value.split(":")[-1]
            self.get_parent(self.parent)
            if child:
                self.account_store.append([child])
            else:
                self.account_store.append([self.parent])

        except AttributeError:
            for n in value:
                self.account_store.append([n])

        handlers = {
            "onDeleteWindow": Gtk.main_quit
        }
        builder.connect_signals(handlers)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = self.name_entry.get_text()
            place = 0
            description = self.description_entry.get_text()
            if self.placeholder.get_active():
                place = 1
            if self.parent:
                self.get_parent(self.parent)
                value = "{0}:{1}".format(value, name)
                insert_id = database.hinsert("accounts", "parent, name, description, type, value, placeholder",
                                             account, name,
                                             description, self.parent_code, value, place)
                account_list.append(row, ["document-new", name, description, "0", "black"])
            else:
                x, y = self.selection.get_selected()
                self.parent = x[y][0]
                self.get_parent(self.parent)
                value = "{0}".format(name)
                insert_id = database.hinsert("accounts", "parent, name, description, type, value, placeholder",
                                             account, name,
                                             description,
                                             self.parent_code, value, place)
                account_list.append(None, ["document-new", name, description, "0", "black"])
            account_codes[name] = insert_id
            account_types[name] = self.parent_code
            ctypes[insert_id] = self.parent_code
            placeholder[name] = place
            value_list[name] = value

        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.close()

    def get_parent(self, value):
        if value == "Assets":
            self.selection.select_path(0)
            self.parent_code = 1
        elif value == "Expenses":
            self.selection.select_path(1)
            self.parent_code = 2
        elif value == "Liabilities":
            self.selection.select_path(2)
            self.parent_code = 3
        elif value == "Incomes":
            self.selection.select_path(3)
            self.parent_code = 4
        elif value == "Equity":
            self.selection.select_path(4)
            self.parent_code = 5
