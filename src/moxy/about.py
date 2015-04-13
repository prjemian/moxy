#!/usr/bin/env python

'''
MOXY: the About box
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


from PyQt4 import QtGui, QtCore
import inspect
import os
import moxy
import form_support


ABOUT_UI_FILE = 'about.ui'  # name of screen description file, in "resources" subdirectory
LICENSE_FILE = 'LICENSE'    # name of the license file, in same directory as this code
README_FILE = 'README.rst'
LOGO_FILE = 'logo.png'
_DIALOG_SHOWING_ = False      # for singleton support
_ADD_URL_BUTTON_ = True       # only do this once


class AboutBox(object):
    
    def __init__(self):
        global _DIALOG_SHOWING_, _ADD_URL_BUTTON_
        if _DIALOG_SHOWING_:
            return          # enforce that this dialog is a singleton
        _DIALOG_SHOWING_ = True

        # Locate the directory that contains this file.
        # This will be used to load other file resources
        # relative to this directory.
        ref = inspect.getsourcefile(AboutBox)
        self.path = os.path.abspath(os.path.split(ref)[0])

        self.ui = form_support.load_form(ABOUT_UI_FILE)
        self._init_heading_()
        self._init_logo_()
        self._init_tabs_(self.ui.tabs)

        if _ADD_URL_BUTTON_:
            pb = QtGui.QPushButton(moxy.__url__, clicked=self.doUrl)
            self.ui.verticalLayout.addWidget(pb)
            _ADD_URL_BUTTON_ = False
        
        self.ui.show()

        #only one button, no need to check if QtGui.QDialog.Accepted
        self.ui.exec_()     # make this a modal dialog, blocking until the user closes it
        _DIALOG_SHOWING_ = False
    
    def _init_heading_(self):
        title = moxy.__package_name__  + ', version ' + moxy.__version__
        self.ui.title.setText(title)
        self.ui.copyright.setText(moxy.__copyright__)
    
    def _init_logo_(self):
        logo_file = os.path.join(self.path, 'forms', LOGO_FILE)
        self.ui.logo.setPixmap(QtGui.QPixmap(logo_file))
   
    def _init_tabs_(self, tabs):
        while tabs.count() > 0:   # first, dispose all default tabs
            tabs.removeTab(0)
        
        # next, create the tabs we want
        path = os.path.abspath(os.path.join(self.path, '..', '..'))
        readme_filename = os.path.join(path, README_FILE)
        description_text = open(readme_filename, 'r').read()
        description_widget = QtGui.QTextEdit('<pre>' + description_text + '</pre>')
        tabs.addTab(description_widget, 'Description')

        credits_text = moxy.__credits__
        credits_widget = QtGui.QTextEdit('<pre>' + credits_text + '</pre>') 
        tabs.addTab(credits_widget, 'Credits')
        
        license_filename = os.path.join(self.path, LICENSE_FILE)
        license_text = open(license_filename, 'r').read()
        license_widget = QtGui.QTextEdit('<pre>' + license_text + '</pre>')
        license_widget.setReadOnly(True)
        tabs.addTab(license_widget, 'License')

    def doUrl(self):
        service = QtGui.QDesktopServices()
        url = QtCore.QUrl(moxy.__url__)
        service.openUrl(url)
