#!/usr/bin/env python
import os,os.path,re,logging,sys,struct,math,traceback,getopt,inspect
import pygtk
pygtk.require('2.0')
import gtk,gtk.glade,gobject

# two panel browser

def get_selected_rows_from_treeview(treeview):
    """
    will return a single value or a list depending on what the selection mode is
    """
    if isinstance(treeview, gtk.TreeView):
        selection = treeview.get_selection()
    elif isinstance(treeview, gtk.TreeSelection):
        selection = treeview
    else:
        return None

    if selection.get_mode() == gtk.SELECTION_MULTIPLE:
        (model, pathlist) = selection.get_selected_rows()
        result = []
        for path in pathlist:
            result.append(model[path])
        return result
    else:
        (model, iter) = selection.get_selected()
        if iter:
            return model[iter] 
        else:
            # not sure why, but firing a second time
            return None


class Node:
    def __init__(self, path, parent_node = None):
        self.path = path 
        self.parent_node = parent_node 
        self.nodes = []

    def fullpath(self):
        return self.path

    def walk(self):
        print self.fullpath()
        for node in self.nodes:
            node.walk()

    def get_treestore(self, treestore = None, start_iter = None, file_list = False):
        if not treestore:
            treestore = gtk.TreeStore(str, str) 

        if (isinstance(self, DirectoryNode) and not file_list) or (isinstance(self, FileNode) and file_list): 
            node_iter = treestore.append(start_iter, [os.path.basename(self.path), self.path])
        else:
            node_iter = None

        # dont recurse for file list
        if not file_list or not start_iter:
            for node in self.nodes:
                node.get_treestore(treestore, node_iter, file_list)

        return treestore

    def get_files_treestore(self):
        return self.get_treestore(None, None, True)

class FileNode(Node):
    def __init__(self, path, parent_node = None):
        Node.__init__(self, path, parent_node)
        self.nodes = [] # file won't ever have this

class DirectoryNode(Node):
    def __init__(self, path, parent_node = None):
        Node.__init__(self, path, parent_node)
        self.nodes = self.get_list()

    def get_list(self):
        nodes = []
        paths = os.listdir(self.path)
        for path in paths:
            fullpath = self.path + "\\" + path
            if os.path.isdir(fullpath):
                node = DirectoryNode(fullpath, self)
            else:
                node = FileNode(fullpath, self)

            nodes.append(node)

        return nodes

class AkTreeView(gtk.TreeView):
    def __init__(self, treestore = None):
        gtk.TreeView.__init__(self, treestore)

        self.textedit = gtk.CellRendererText()
        self.textedit.set_property('editable', False)
        #textedit.connect('edited', self.on_textedit_changed, (treestore, 0))
        self.append_column(gtk.TreeViewColumn("Name", self.textedit, text=0))

class BrowserScrolledWindow(gtk.ScrolledWindow):
    def __init__(self, treestore = None):
        gtk.ScrolledWindow.__init__(self)
        self.treeview = AkTreeView(treestore)
        self.add(self.treeview)

class Browser(gtk.Window):
    def __init__(self, arguments):
        import getopt, glob, operator
        gtk.Window.__init__(self)
        #z48 = Devices.get_instance("z48", "usb")
        options, arguments = getopt.getopt(arguments, '?p')

        d = DirectoryNode("c:\\j\\mpc1000\\akpakm\\joe")
        self.hpaned = gtk.HPaned()
        self.treestore_dir = d.get_treestore()
        self.treestore_files = gtk.TreeStore(str, str) # temp
        # scrolling treeviews
        self.sw_dir = BrowserScrolledWindow(self.treestore_dir)
        self.sw_files = BrowserScrolledWindow(self.treestore_files)
        # hook up events
        self.sw_dir.treeview.connect("button-press-event", self.on_treeview_event)
        selection = self.sw_dir.treeview.get_selection()
        selection.connect("changed", self.on_dir_selection_changed)
        self.sw_files.treeview.connect("button-press-event", self.on_treeview_event)
        selection = self.sw_files.treeview.get_selection()
        selection.connect("changed", self.on_file_selection_changed)
        self.init_files(d.path)
        self.hpaned.add1(self.sw_dir)
        self.hpaned.add2(self.sw_files)
        self.add(self.hpaned)
        self.show_all()
        self.connect("delete-event", gtk.main_quit)

    def init_files(self, path):
        if not isinstance(path, DirectoryNode):
            d = DirectoryNode(path)
        else:
            d = path

        self.treestore_files = d.get_files_treestore()
        self.sw_files.treeview.set_model(self.treestore_files)
        self.sw_files.queue_draw()

    def on_treeview_event(self, widget, event):
        return False

    def on_dir_selection_changed(self, selection):
        selected_name = get_selected_rows_from_treeview(selection)
        self.init_files(selected_name[1]) # col 1 - full path

    def on_file_selection_changed(self, selection):
        treeview = selection.get_tree_view()
        selected_name = get_selected_rows_from_treeview(treeview)
        if selected_name:
            self.init_files(selected_name[1]) # col 1 - full path

def main(arguments):
    browser = Browser(arguments)
    gtk.main()


if __name__ == '__main__':
    main(sys.argv[1:])

