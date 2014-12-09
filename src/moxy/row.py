#!/usr/bin/env python

'''
widget support for one row in a position table
'''

# Copyright (c) 2009 - 2014, UChicago Argonne, LLC.
# See LICENSE file for details.


import inspect
import os
import sys
from PySide import QtGui
import form_support


class Row(object):
    
    def __init__(self):
        self.ui = form_support.load_form('row.ui')
        self._init_icons()
    
    def _init_icons(self):
        '''use button icons'''
        ref = inspect.getsourcefile(Row)
        path = os.path.abspath(os.path.split(ref)[0])
        forms_path = os.path.join(path, 'forms')

        icon = QtGui.QIcon(os.path.join(forms_path, 'delete.bmp'))
        self.ui.deleteButton.setIcon(icon)
        self.ui.deleteButton.setText('')

        icon = QtGui.QIcon(os.path.join(forms_path, 'set.bmp'))
        self.ui.setButton.setIcon(icon)
        self.ui.setButton.setText('')

        icon = QtGui.QIcon(os.path.join(forms_path, 'go.bmp'))
        self.ui.goButton.setIcon(icon)
        self.ui.goButton.setText('')
