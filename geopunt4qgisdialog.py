# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geopunt4QgisDialog
                                 A QGIS plugin
 "Tool om geopunt in QGIS te gebruiken"
                             -------------------
        begin                : 2013-12-05
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
from PyQt4 import QtCore, QtGui
from ui_geopunt4qgis import Ui_geopunt4Qgis
from qgis.core import *
import geopunt 
import geometryhelper as gh

class geopunt4QgisDialog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_geopunt4Qgis()
        self.ui.setupUi(self)
        self.iface = iface
        
        self.gp = geopunt.geopunt()
        self.gh = gh.geometryHelper(iface)
        
        self.ui.zoekText.returnPressed.connect(self.onZoekActivated)
        self.ui.zoekBtn.clicked.connect(self.onZoekActivated)
        self.ui.resultLijst.itemDoubleClicked.connect(self.onItemActivated)
        self.ui.ZoomKnop.clicked.connect(self.onZoomKnopClick)
        self.ui.Add2mapKnop.clicked.connect(self.onAdd2mapKnopClick)
        
    def onZoekActivated(self):
        txt = self.ui.zoekText.text()
        suggesties = self.gp.fetchSuggestion( txt , 12 )
        self.ui.resultLijst.clear()
        self.ui.resultLijst.addItems(suggesties)
        
    def onItemActivated( self , item):
	txt = item.text()
	self._zoomLoc(txt)
	
    def onZoomKnopClick(self):
	item = self.ui.resultLijst.currentItem()
	if item:
	  self._zoomLoc(item.text())

    def onAdd2mapKnopClick(self):
	item = self.ui.resultLijst.currentItem()
	if item:
	  self._addToMap(item.text())
	
    def _zoomLoc(self, txt):
	locations = self.gp.fetchLocation(txt)
	if len( locations ):
	    loc = locations[0]
	    
	    LowerLeftX = loc['BoundingBox']['LowerLeft']['X_Lambert72']
	    LowerLeftY = loc['BoundingBox']['LowerLeft']['Y_Lambert72']
	    UpperRightX = loc['BoundingBox']['UpperRight']['X_Lambert72']
	    UpperRightY = loc['BoundingBox']['UpperRight']['Y_Lambert72']
	    
	    self.gh.zoomtoRec(QgsPoint(UpperRightX, UpperRightY), 
		      QgsPoint(LowerLeftX,LowerLeftY), 31370)
	    
    def _addToMap(self, txt):
	locations = self.gp.fetchLocation(txt)
	if len( locations ):
	    loc = locations[0]
	    x, y = loc["Location"]["X_Lambert72"], loc["Location"]["Y_Lambert72"]
	    adres = loc["FormattedAddress"]
	    LocationType = loc["LocationType"]
	    
	    lat, lon = self.gh.prjPtToMapCrs(QgsPoint( x , y), 31370)
	    
	    self.gh.save_point(QgsPoint(lat, lon), adres, LocationType )
