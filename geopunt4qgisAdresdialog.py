# -*- coding: utf-8 -*-
"""
/***************************************************************************
geopunt4qgisdialog
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
from qgis.gui import  QgsMessageBar, QgsVertexMarker
import geopunt, os, json, webbrowser
import geometryhelper as gh

class geopunt4QgisAdresDialog(QtGui.QDialog):
    def __init__(self, iface):
	    QtGui.QDialog.__init__(self)
	    self.iface = iface
	
	    # initialize locale
	    locale = QtCore.QSettings().value("locale/userLocale")[0:2]
	    localePath = os.path.join(os.path.dirname(__file__), 'i18n', 'geopunt4qgis_{}.qm'.format(locale))
	    if os.path.exists(localePath):
	        self.translator = QtCore.QTranslator()
	        self.translator.load(localePath)
	        if QtCore.qVersion() > '4.3.3': QtCore.QCoreApplication.installTranslator(self.translator)
	
	    self._initGui()

    def _initGui(self):
	"""setup the user interface"""
	self.ui = Ui_geopunt4Qgis()
	self.ui.setupUi(self)
    
	#get settings
	self.s = QtCore.QSettings()
	self.loadSettings()
    
	#setup geopunt and geometryHelper objects
	self.gp = geopunt.Adres(self.timeout)
	self.gh = gh.geometryHelper(self.iface)
    
	#create graphicsLayer
	self.graphicsLayer = []

	#populate gemeenteBox
	gemeentes = json.load( open(os.path.join(os.path.dirname(__file__),
			  "data/gemeentenVL.json")) )
	self.ui.gemeenteBox.addItems( [n["Naam"] for n in gemeentes] )
	self.ui.gemeenteBox.setEditText(QtCore.QCoreApplication.translate(
			  "geopunt4QgisAdresDialog", "gemeente"))
	self.ui.gemeenteBox.setStyleSheet('QComboBox {color: #808080}')
	self.ui.gemeenteBox.setFocus()
    
	#setup a message bar
	self.bar = QgsMessageBar() 
	self.bar.setSizePolicy( QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed )
	self.ui.verticalLayout.addWidget(self.bar)

	#event handlers 
	if self.adresSearchOnEnter:
	  self.ui.zoekText.returnPressed.connect(self.onZoekActivated)
	else:
	  self.ui.zoekText.textEdited.connect(self.onZoekActivated)
	self.ui.gemeenteBox.currentIndexChanged.connect(self.onZoekActivated)
	self.ui.resultLijst.itemDoubleClicked.connect(self.onItemActivated)
	self.ui.resultLijst.itemClicked.connect(self.onItemClick)
	self.ui.ZoomKnop.clicked.connect(self.onZoomKnopClick)
	self.ui.Add2mapKnop.clicked.connect(self.onAdd2mapKnopClick)
	self.ui.buttonBox.helpRequested.connect(self.openHelp)
	self.finished.connect(self.clean )
	
    def loadSettings(self):
        self.saveToFile = int( self.s.value("geopunt4qgis/adresSavetoFile" , 1))
        self.layerName =  self.s.value("geopunt4qgis/adreslayerText", "geopunt_adres")
        self.adresSearchOnEnter = int( self.s.value("geopunt4qgis/adresSearchOnEnter" , 0))
        self.timeout = 15
        
    def openHelp(self):
	webbrowser.open_new_tab("http://warrieka.github.io/index.html#!geopuntAddress.md")
	
    def onZoekActivated(self):
	    self._clearGraphicsLayer()
	    self.bar.clearWidgets()
	
	    gemeente = self.ui.gemeenteBox.currentText() 
	    if gemeente <> QtCore.QCoreApplication.translate("geopunt4QgisAdresDialog","gemeente"):
	      self.ui.gemeenteBox.setStyleSheet('QComboBox {color: #000000}')
	
	      txt = self.ui.zoekText.text() +", "+ gemeente
	
	      suggesties = self.gp.fetchSuggestion( txt , 25 )
	  
	      self.ui.resultLijst.clear()
	      if suggesties.__class__ == list and len(suggesties) <> 0:
	        self.ui.resultLijst.addItems(suggesties)
	        if len(suggesties) == 1:
	          self.ui.resultLijst.setCurrentRow(0)
	      elif suggesties.__class__ is str:
	        self.bar.pushMessage(
	          QtCore.QCoreApplication.translate("geopunt4QgisAdresDialog","Waarschuwing"),
		      suggesties, level=QgsMessageBar.WARNING)
	  
    def onItemActivated( self, item):
	    txt = item.text()
	    self._zoomLoc(txt)
	
    def onItemClick(self, item):
	    txt = item.text()
	    streetNr = txt.split(",")[:-1]
	    self.ui.zoekText.setText( ",".join(streetNr)  )
	
    def onZoomKnopClick(self):
	    item = self.ui.resultLijst.currentItem()
	    if item:
	      self._zoomLoc(item.text())

    def onAdd2mapKnopClick(self):
	    item = self.ui.resultLijst.currentItem()
	    if item:
	      self._addToMap(item.text())
	  
    def _clearGraphicsLayer(self):
	    for graphic in  self.graphicsLayer: 
	      self.iface.mapCanvas().scene().removeItem(graphic)
	    self.graphicsLayer = []
	
    def _zoomLoc(self, txt):
	    self._clearGraphicsLayer()
	    locations = self.gp.fetchLocation(txt)
	    if locations.__class__ == list and len(locations):
	        loc = locations[0]
	    
	        LowerLeftX = loc['BoundingBox']['LowerLeft']['X_Lambert72']
	        LowerLeftY = loc['BoundingBox']['LowerLeft']['Y_Lambert72']
	        UpperRightX = loc['BoundingBox']['UpperRight']['X_Lambert72']
	        UpperRightY = loc['BoundingBox']['UpperRight']['Y_Lambert72']
	    
	        self.gh.zoomtoRec(QgsPoint(LowerLeftX,LowerLeftY),QgsPoint(UpperRightX, UpperRightY), 31370)
	    
	        xlb, ylb = loc["Location"]["X_Lambert72"], loc["Location"]["Y_Lambert72"]
	        x, y = self.gh.prjPtToMapCrs(QgsPoint( xlb , ylb), 31370)
	    
	        m = QgsVertexMarker(self.iface.mapCanvas())
	        self.graphicsLayer.append(m)
	        m.setCenter(QgsPoint(x,y))
	        m.setColor(QtGui.QColor(255,255,0))
	        m.setIconSize(1)
	        m.setIconType(QgsVertexMarker.ICON_BOX) 
	        m.setPenWidth(9)
	    
	    elif locations.__class__ == str:
	      self.bar.pushMessage(
	        QtCore.QCoreApplication.translate("geopunt4QgisAdresDialog","Waarschuwing"), 
			    locations, level=QgsMessageBar.WARNING, duration=3)
	    else:
	      self.bar.pushMessage("Error", 
	        QtCore.QCoreApplication.translate("geopunt4QgisAdresDialog","onbekende fout"),
			    level=QgsMessageBar.CRITICAL, duration=3)
	    
    def _addToMap(self, txt):
	    locations = self.gp.fetchLocation(txt)
	    if locations.__class__ == list and len(locations):
	        loc = locations[0]
	        x, y = loc["Location"]["X_Lambert72"], loc["Location"]["Y_Lambert72"]
	        adres = loc["FormattedAddress"]
	        LocationType = loc["LocationType"]
	    
	        pt = self.gh.prjPtToMapCrs(QgsPoint( x, y), 31370)
	    
	        self.gh.save_adres_point( pt, adres, typeAddress=LocationType, 
			    layername=self.layerName, saveToFile=self.saveToFile, sender=self )
	    
	    elif locations.__class__ == str:
	      self.bar.pushMessage(
		    QtCore.QCoreApplication.translate("geopunt4QgisAdresDialog","Waarschuwing"), 
			    locations, level=QgsMessageBar.WARNING)	
	    else:
	      self.bar.pushMessage("Error", 
		    QtCore.QCoreApplication.translate("geopunt4QgisAdresDialog","onbekende fout"),
			    level=QgsMessageBar.CRITICAL)
	  
    def clean(self):
        self.bar.clearWidgets()
        self.ui.resultLijst.clear()
        self.ui.zoekText.setText("")
        self.ui.gemeenteBox.setEditText(QtCore.QCoreApplication.translate(
				"geopunt4QgisAdresDialog","gemeente"))
        self.ui.gemeenteBox.setStyleSheet('QComboBox {color: #808080}')
        self._clearGraphicsLayer()
	