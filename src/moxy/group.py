#!/usr/bin/env python

'''
widget support for a group of a positioners
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


import os
import sys
from PyQt4 import QtGui
import form_support
import table


class Group(object):
    
    def __init__(self):
        self.ui = form_support.load_form('group.ui')
        self._init_tables_(self.ui.tables)
    
    def _init_tables_(self, tables):
        while tables.count() > 0:   # first, dispose all default tabs
            tables.removeTab(0)
        
        tbl = table.Table()
        tables.addTab(tbl.ui, 'table0')
