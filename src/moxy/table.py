#!/usr/bin/env python

'''
widget support for a position table
'''

# Copyright (c) 2009 - 2014, UChicago Argonne, LLC.
# See LICENSE file for details.


import os
import sys
from PySide import QtGui
import row
import form_support


class Table(object):
    
    def __init__(self):
        self.ui = form_support.load_form('table.ui')
        
        # TODO: replace these examples with proper function
        for _ in range(3):
            self.ui.layout0.addWidget(row.Row().ui)
        self.ui.layout0.addStretch(1)
