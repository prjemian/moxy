#!/usr/bin/env python

'''
MOXY: the Configure box
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


from PySide import QtGui, QtCore
import inspect
import os
import moxy
import form_support


CONFIGURE_UI_FILE = 'configure_pv.ui'  # name of screen description file, in forms subdirectory
LOGO_FILE = 'epicslogo101.bmp'
_DIALOG_SHOWING_ = False      # for singleton support
GROUP_COUNTER = 0
MOXYMOTOR_COUNTER = 0


# TODO: need way to add/delete groups and positioners
# TODO: fill the QListView widget: self.ui.listView
# TODO: change QListView to QTreeView?

class ConfigureBox(object):
    
    def __init__(self):
        global _DIALOG_SHOWING_
        if _DIALOG_SHOWING_:
            return          # enforce that this dialog is a singleton
        _DIALOG_SHOWING_ = True

        self.ui = form_support.load_form(CONFIGURE_UI_FILE)
        self._init_logo_()
        
        self.groups = []
        self._initTreeWidget()
        self.selectedItem = None    # treeWidget item selected (or None)
        self._initActions()
        self.createAxis()           # make at least one axis to start with
        self.createAxis()           # make at least one axis to start with
        self.createAxis()           # make at least one axis to start with
        
        self.ui.show()

        # make this a modal dialog, blocking until the user closes it
        if self.ui.exec_():
            # apply changes only if QtGui.QDialog.Accepted
            print self.groups
            pass
        _DIALOG_SHOWING_ = False
    
    def _init_logo_(self):
        logo_file = os.path.join(form_support.get_forms_path(), LOGO_FILE)
        self.ui.logo.setPixmap(QtGui.QPixmap(logo_file))
        
    def _initActions(self):
        # TODO: combine the two create buttons
        # TODO: combine the two remove buttons
        self.ui.createGroup.clicked.connect(self.doCreateGroup)
        self.ui.removeGroup.clicked.connect(self.doRemove)
        self.ui.createAxis.clicked.connect(self.doCreateAxis)
        self.ui.removeAxis.clicked.connect(self.doRemove)
        self.ui.treeWidget.itemSelectionChanged.connect(self.doSelectionChanged)
        self.ui.treeWidget.itemClicked.connect(self.doClicked)
        self.ui.treeWidget.itemPressed.connect(self.doPressed)
        
    def _initTreeWidget(self):
        treewidget = self.ui.treeWidget
        treewidget.setColumnCount(1)
        treewidget.setHeaderLabels(['axes groups --> moxy motors'])
    
    def doClicked(self, item, column):
        print 'Clicked', item, column, ' not handled yet'
        self.selectedItem = item
        # TODO: enable push buttons based on selection
    
    def doCreateGroup(self):
        '''create a group'''
        self.createAxis()
    
    def doCreateAxis(self):
        '''create a moxymotor axis within a group'''
        print 'Create', self.selectedItem
        print 'self.selectedItem', type(self.selectedItem)
        print 'self.groups', type(self.groups)
        # FIXME: next test results in "NotImplementedError: operator not implemented."
#         if self.selectedItem in self.groups:  # only if a group is selected
#             print ' not handled yet'
#             # self.createMoxyMotor(group)
#         else:
#             print 'Create', self.selectedItem, ' not allowed for `axis`'
    
    def doPressed(self, item, column):
        print 'Pressed', item, column, ' not handled yet'
        self.selectedItem = item
    
    def doRemove(self):
        print 'Remove', self.selectedItem, ' not handled yet'
        # TODO: always confirm
    
    def doSelectionChanged(self):
        print 'SelectionChanged'
        self.selectedItem = None
        # TODO: disable push buttons based on selection
    
    def doGenericSignal(self, *args, **kw):
        print 'GenericSignal', args, kw, ' not handled yet'
    
    def createAxis(self):
        global GROUP_COUNTER
        GROUP_COUNTER += 1
        group = QtGui.QTreeWidgetItem(None)
        group.setFirstColumnSpanned(True)
        group.setText(0, 'axis group ' + str(GROUP_COUNTER))
        self.ui.treeWidget.addTopLevelItems([group,])
        self.ui.treeWidget.expandItem(group)
        # self.ui.treeWidget.setItemSelected(group, True)
        self.groups.append(group)
    
    def createMoxyMotor(self, group):
        global MOXYMOTOR_COUNTER
        MOXYMOTOR_COUNTER += 1
        mmotor = QtGui.QTreeWidgetItem(group)
        mmotor.setText(0, 'motor ' + str(MOXYMOTOR_COUNTER))


if __name__ == '__main__':
    '''simple test program for developers'''
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QWidget()
    MainWindow.show()
    cb = ConfigureBox()
    #sys.exit(app.exec_())
    sys.exit()
