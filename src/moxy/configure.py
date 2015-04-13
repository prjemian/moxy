#!/usr/bin/env python

'''
MOXY: the Configure box
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


from PyQt4 import QtGui, QtCore
import inspect
import os
import moxy
import form_support


CONFIGURE_UI_FILE = 'configure_pv.ui'  # name of screen description file, in forms subdirectory
LOGO_FILE = 'epicslogo101.bmp'
_DIALOG_SHOWING_ = False      # for singleton support
GROUP_COUNTER = 0
MOXYMOTOR_COUNTER = 0


# TODO: need to delete groups and positioners

class ConfigureBox(object):
    
    def __init__(self):
        global _DIALOG_SHOWING_
        if _DIALOG_SHOWING_:
            return          # enforce that this dialog is a singleton
        _DIALOG_SHOWING_ = True

        self.ui = form_support.load_form(CONFIGURE_UI_FILE)
        self._init_logo_()
        
        self._initTreeWidget()
        self.selectedItem = None    # treeWidget item selected (or None)
        self.selectedKind = None
        self._initActions()
        self.setButtonStates(False, False, False)
        
        self.createGroup()           # make at least one axis to start with
        
        self.ui.show()

        # make this a modal dialog, blocking until the user closes it
        if self.ui.exec_():
            # apply changes only if QtGui.QDialog.Accepted
            self.debrief()
        _DIALOG_SHOWING_ = False
    
    def _init_logo_(self):
        logo_file = os.path.join(form_support.get_forms_path(), LOGO_FILE)
        self.ui.logo.setPixmap(QtGui.QPixmap(logo_file))
        
    def _initActions(self):
        # TODO: combine the two create buttons
        self.ui.createGroup.clicked.connect(self.doCreateGroup)
        self.ui.removeGroup.clicked.connect(self.doRemove)
        self.ui.createAxis.clicked.connect(self.doCreateAxis)
        self.ui.removeAxis.clicked.connect(self.doRemove)
        self.ui.treeWidget.itemSelectionChanged.connect(self.doSelectionChanged)
        self.ui.treeWidget.itemClicked.connect(self.doClicked)
        # self.ui.treeWidget.itemPressed.connect(self.doPressed)
        
    def _initTreeWidget(self):
        treewidget = self.ui.treeWidget
        treewidget.setColumnCount(1)
        treewidget.setHeaderLabels(['axes groups --> moxy motors'])
    
    def debrief(self):
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            print item.text(0)
            for j in range(item.childCount()):
                print '\t', item.child(j).text(0)
    
    def doClicked(self, item, column):
        _parent = item.parent()
        self.selectedItem = item
        if item.parent() is None:
            self.selectedKind = 'group'
            self.setButtonStates(True, True, False)
        else:
            self.selectedKind = 'axis'
            self.setButtonStates(False, True, True)
    
    def doCreateGroup(self):
        '''create a group'''
        self.createGroup()
    
    def doCreateAxis(self):
        '''create a moxymotor axis within a group'''
        # print 'Create', self.selectedItem
        self.createAxis()
    
    def doPressed(self, item, column):
        print 'Pressed', item, column, ' not handled yet'
        self.selectedItem = item
    
    def doRemove(self):
        # TODO: always confirm
        if self.selectedItem is None: return
        if self.selectedItem.parent() is None:
            parent = self.ui.treeWidget
            index = parent.indexOfTopLevelItem(self.selectedItem)
            parent.takeTopLevelItem(index)
        else:
            group = self.selectedItem.parent()
            index = group.indexOfChild(self.selectedItem)
            group.takeChild(index)
    
    def doSelectionChanged(self):
        # print 'SelectionChanged'
        self.selectedItem = None
        self.selectedKind = None
        self.setButtonStates(False, False, False)
    
    def doGenericSignal(self, *args, **kw):
        print 'GenericSignal', args, kw, ' not handled yet'
    
    def createGroup(self):
        global GROUP_COUNTER
        GROUP_COUNTER += 1
        group = QtGui.QTreeWidgetItem(None)
        group.setFirstColumnSpanned(True)
        group.setText(0, 'axis group ' + str(GROUP_COUNTER))
        self.ui.treeWidget.addTopLevelItems([group,])
        self.ui.treeWidget.expandItem(group)
        # self.ui.treeWidget.setItemSelected(group, True)
    
    def createAxis(self):
        if self.selectedItem is None:
            return
        group = self.selectedItem.parent() or self.selectedItem
        self.createMoxyMotor(group)
    
    def createMoxyMotor(self, group):
        global MOXYMOTOR_COUNTER
        MOXYMOTOR_COUNTER += 1
        mmotor = QtGui.QTreeWidgetItem(group)
        mmotor.setText(0, 'motor ' + str(MOXYMOTOR_COUNTER))
    
    def setButtonStates(self, removeGroup=True, createAxis=True, removeAxis=True):
        self._enableButton(self.ui.removeGroup, removeGroup)
        self._enableButton(self.ui.createAxis, createAxis)
        self._enableButton(self.ui.removeAxis, removeAxis)
    
    def _enableButton(self, button, state = True):
        if button.isEnabled() != state:
            button.setEnabled(state)


if __name__ == '__main__':
    '''simple test program for developers'''
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QWidget()
    MainWindow.show()
    cb = ConfigureBox()
    #sys.exit(app.exec_())
    sys.exit()
