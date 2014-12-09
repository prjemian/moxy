#!/usr/bin/env python

'''
MOXY: the Configure box
'''

# Copyright (c) 2009 - 2014, UChicago Argonne, LLC.
# See LICENSE file for details.


from PySide import QtGui
import inspect
import os
import moxy
import form_support


CONFIGURE_UI_FILE = 'configure_pv.ui'  # name of screen description file, in forms subdirectory
LOGO_FILE = 'epicslogo101.bmp'
dialog_showing = False      # for singleton support


# TODO: need way to add/delete groups and positioners
# TODO: fill the QListView widget: self.ui.listView
# TODO: change QListView to QTreeView?

class ConfigureBox(object):
    
    def __init__(self):
        global dialog_showing
        if dialog_showing:
            return          # enforce that this dialog is a singleton
        dialog_showing = True

        # Locate the directory that contains this file.
        # This will be used to load other file resources
        # relative to this directory.
        ref = inspect.getsourcefile(ConfigureBox)
        self.path = os.path.abspath(os.path.split(ref)[0])

        self.ui = form_support.load_form(CONFIGURE_UI_FILE)
        self._init_logo_()
        
        self.ui.show()

        # TODO: apply changes only if QtGui.QDialog.Accepted
        self.ui.exec_()     # make this a modal dialog, blocking until the user closes it
        dialog_showing = False
    
    def _init_logo_(self):
        logo_file = os.path.join(self.path, 'forms', LOGO_FILE)
        self.ui.logo.setPixmap(QtGui.QPixmap(logo_file))
