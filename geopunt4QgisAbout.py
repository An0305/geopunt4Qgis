# -*- coding: utf-8 -*-
"""
/***************************************************************************
geopunt4QgisAboutdialog
                                A QGIS plugin
"Tool om geopunt in QGIS te gebruiken"
                            -------------------
        begin                : 2013-12-08
        copyright            : (C) 2013 by Kay Warrie
        email                : kaywarrie@gmail.com
***************************************************************************/

/***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************/
"""
import os.path
from PyQt4 import QtCore, QtGui
from ui_geopunt4QgisAbout import Ui_aboutDlg

class geopunt4QgisAboutdialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, None)
        self.setWindowFlags( self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint )
        self.setWindowFlags( self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # initialize locale
        locale = QtCore.QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(os.path.dirname(__file__), 'i18n', 
                  'geopunt4qgis_{}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QtCore.QTranslator()
            self.translator.load(localePath)
            if QtCore.qVersion() > '4.3.3': 
               QtCore.QCoreApplication.installTranslator(self.translator)
            
            #localised about html exists if locale exists
            self.htmlFile = os.path.join(os.path.dirname(__file__), 'i18n', 
                  'about-{}.html'.format(locale))
        else:
            #dutch is default
            self.htmlFile = os.path.join(os.path.dirname(__file__), 'i18n', 'about-nl.html')   
            self._initGui()
    
    
    
    def _initGui(self):
      # Set up the user interface from Designer.
      self.ui = Ui_aboutDlg() 
      self.ui.setupUi(self)
      self.ui.buttonBox.addButton( QtGui.QPushButton("Sluiten"), QtGui.QDialogButtonBox.RejectRole  )
      with open(self.htmlFile, 'r') as html:
           self.ui.aboutText.setHtml( html.read() )
      