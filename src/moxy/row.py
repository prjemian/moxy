#!/usr/bin/env python

'''
widget support for one row in a position table
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


import os
from PySide import QtGui
import form_support


class Row(object):
    
    def __init__(self):
        self.ui = form_support.load_form('row.ui')
        self._init_icons()
    
    def _init_icons(self):
        '''use button icons'''
        forms_path = form_support.get_forms_path()

        icon = QtGui.QIcon(os.path.join(forms_path, 'delete.bmp'))
        self.ui.deleteButton.setIcon(icon)
        self.ui.deleteButton.setText('')

        icon = QtGui.QIcon(os.path.join(forms_path, 'set.bmp'))
        self.ui.setButton.setIcon(icon)
        self.ui.setButton.setText('')

        icon = QtGui.QIcon(os.path.join(forms_path, 'go.bmp'))
        self.ui.goButton.setIcon(icon)
        self.ui.goButton.setText('')
