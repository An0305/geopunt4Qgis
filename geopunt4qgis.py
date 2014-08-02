# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geopunt4Qgis
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import  QgsMessageBar, QgsVertexMarker
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialogs
from geopunt4qgisAdresdialog import geopunt4QgisAdresDialog
from geopunt4QgisPoidialog import geopunt4QgisPoidialog
from reverseAdresMapTool import reverseAdresMapTool
from geopunt4QgisAbout import geopunt4QgisAboutdialog
from geopunt4QgisSettingsdialog import geopunt4QgisSettingsdialog
from geopunt4QgisBatchGeoCode import geopunt4QgisBatcGeoCodeDialog
from geopunt4QgisGipod import geopunt4QgisGipodDialog
from geopunt4QgisElevation import geopunt4QgisElevationDialog
from geopunt4QgisDataCatalog import geopunt4QgisDataCatalog
#import selfmade libs
from versionChecker import versionChecker
#import from libraries
import geopunt, geometryhelper
import os.path, webbrowser
from threading import Timer

class geopunt4Qgis:
    def __init__(self, iface):
        'initialize'
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'geopunt4qgis_{}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            if qVersion() > '4.3.3': QCoreApplication.installTranslator(self.translator)

        #version check
        if locale == 'nl':  
           vc = versionChecker()
           if not vc.isUptoDate():
              QMessageBox.warning(None, QCoreApplication.translate("geopunt4Qgis", "Waarschuwing"),
                  QCoreApplication.translate("geopunt4Qgis", 
                  "Je versie van <a href='http://plugins.qgis.org/>plugins/geopunt4Qgis' >geopunt4qgis</a> is niet meer "+ 
                  "up to date. <br/>Je kunt deze upgraden via het menu:<br/> "+
                  "<strong>Plugins > Beheer en installeer Plugins > Op te waarderen.</strong>"+
                  "<br/>Klik daarna op <strong>Plugin opwaarderen</strong>"))           

        # Create the dialogs (after translation) and keep reference
        self.adresdlg = geopunt4QgisAdresDialog(self.iface)
        self.batchgeoDlg = geopunt4QgisBatcGeoCodeDialog(self.iface) 
        self.poiDlg = geopunt4QgisPoidialog(self.iface)        
        self.gipodDlg = geopunt4QgisGipodDialog(self.iface)
        self.settingsDlg = geopunt4QgisSettingsdialog()
        self.elevationDlg = geopunt4QgisElevationDialog(self.iface)
        self.datacatalogusDlg = geopunt4QgisDataCatalog(self.iface)
        self.aboutDlg = geopunt4QgisAboutdialog()
        
    def initGui(self):
        'intialize settings'
        #get settings
        self.s = QSettings()
        self.loadSettings()
        
        #geopunt adres and geometry object
        self.adres = geopunt.Adres(self.timeout, self.proxy, self.port)
        self.gh = geometryhelper.geometryHelper(self.iface)
        self.graphicsLayer = []

        # Create actions that will start plugin configuration
        self.adresAction = QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntAddress.png"),
            QCoreApplication.translate("geopunt4Qgis" , u"Zoek een Adres"), self.iface.mainWindow())
        self.reverseAction = QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntReverse.png"),
                QCoreApplication.translate("geopunt4Qgis", u"Prik een Adres op kaart"), 
                self.iface.mainWindow())
        self.batchAction = QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntBatchgeocode.png"),
	        QCoreApplication.translate("geopunt4Qgis", u"CSV-adresbestanden geocoderen"),
	        self.iface.mainWindow())
        self.poiAction = QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntPoi.png"),
                QCoreApplication.translate("geopunt4Qgis" , u"Zoek een Plaats - interesse punt"), 
	        self.iface.mainWindow())	
        self.gipodAction = QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntGIPOD.png"),
                QCoreApplication.translate("geopunt4Qgis" , u"Bevraag GIPOD"), self.iface.mainWindow())
        self.settingsAction = QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntSettings.png"),
                QCoreApplication.translate("geopunt4Qgis" , u"Instellingen"), self.iface.mainWindow())  
        self.elevationAction =  QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntElevation.png"),
                QCoreApplication.translate("geopunt4Qgis" , u"Hoogteprofiel"), self.iface.mainWindow())
        self.datacatalogusAction =  QAction(QIcon(":/plugins/geopunt4Qgis/images/geopuntDataCatalogus.png"),
                QCoreApplication.translate("geopunt4Qgis" , u"Datacatalogus"), self.iface.mainWindow())
        self.aboutAction = QAction(QIcon(":/plugins/geopunt4Qgis/images/geopunt.png"),
                QCoreApplication.translate("geopunt4Qgis" , u"Over geopunt4Qgis"), self.iface.mainWindow())
 
        # connect the action to the run method
        self.adresAction.triggered.connect(self.runAdresDlg)
        self.reverseAction.triggered.connect(self.reverse)
        self.batchAction.triggered.connect(self.runBatch)
        self.poiAction.triggered.connect(self.runPoiDlg)
        self.gipodAction.triggered.connect(self.runGipod)
        self.elevationAction.triggered.connect(self.runElevation)
        self.datacatalogusAction.triggered.connect(self.rundatacatalog)
        self.settingsAction.triggered.connect(self.runSettingsDlg)
        self.aboutAction.triggered.connect(self.runAbout)
        
        # Add to toolbar button
        self.iface.addToolBarIcon(self.adresAction)
        self.iface.addToolBarIcon(self.reverseAction)
        self.iface.addToolBarIcon(self.batchAction)
        self.iface.addToolBarIcon(self.poiAction)        
        self.iface.addToolBarIcon(self.gipodAction)
        self.iface.addToolBarIcon(self.elevationAction)
        self.iface.addToolBarIcon(self.datacatalogusAction)
        
        # Add to Menu
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.adresAction)
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.reverseAction)
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.batchAction)
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.poiAction)        
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.gipodAction)
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.elevationAction)
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.datacatalogusAction)
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.settingsAction)
        self.iface.addPluginToMenu(u"&geopunt4Qgis", self.aboutAction)
        
    def unload(self):
        ' Remove the plugin menu items and icons'
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.adresAction)
        self.iface.removeToolBarIcon(self.adresAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.poiAction)
        self.iface.removeToolBarIcon(self.poiAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.reverseAction)
        self.iface.removeToolBarIcon(self.reverseAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.batchAction)
        self.iface.removeToolBarIcon(self.batchAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.aboutAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.settingsAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.gipodAction)
        self.iface.removeToolBarIcon(self.gipodAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.elevationAction)
        self.iface.removeToolBarIcon(self.elevationAction)
        self.iface.removePluginMenu(u"&geopunt4Qgis", self.datacatalogusAction)
        self.iface.removeToolBarIcon(self.datacatalogusAction)
        
    def loadSettings(self):
        self.saveToFile_reverse = int(self.s.value("geopunt4qgis/reverseSavetoFile", 0))
        layerName_reverse = self.s.value("geopunt4qgis/reverseLayerText", "")
        if layerName_reverse != "":
           self.layerName_reverse= layerName_reverse
        self.timeout =  int(  self.s.value("geopunt4qgis/timeout" ,15))
        self.proxy = self.s.value("geopunt4qgis/proxyHost" ,"")
        self.port = self.s.value("geopunt4qgis/proxyPort" ,"")
        self.startDir = self.s.value("geopunt4qgis/startDir", os.path.dirname(__file__))
        
    def runSettingsDlg(self):
        ' show the dialog'
        self.settingsDlg.show()
        # Run the dialog event loop
        result = self.settingsDlg.exec_()
        if result:
            self.loadSettings()
            
    def runAdresDlg(self):
        ' show the dialog'
        self.adresdlg.show()
        self.adresdlg.loadSettings()
        # Run the dialog event loop
        self.adresdlg.exec_()
        
    def runPoiDlg(self):
        'show the dialog'
        self.poiDlg.show()
        self.poiDlg.loadSettings()
        # Run the dialog event loop
        self.poiDlg.exec_()
  
    def runGipod(self):
        'show the dialog'
        self.gipodDlg.show()
        self.gipodDlg.loadSettings()
        # Run the dialog event loop
        self.gipodDlg.exec_()
  
    def runBatch(self):
        'show the dialog'
        self.batchgeoDlg.show()
        self.batchgeoDlg.loadSettings()
        # Run the dialog event loop
        self.batchgeoDlg.exec_()

    def runElevation(self):
        'show the dialog'
        self.elevationDlg.show()
        self.elevationDlg.loadSettings()
        # Run the dialog event loop
        self.elevationDlg.exec_()

    def rundatacatalog(self):
        'show the dialog'
        self.datacatalogusDlg.show()
        # Run the dialog event loop
        self.datacatalogusDlg.exec_()

    def runAbout(self):
        'show the dialog'
        self.aboutDlg.show()
        # Run the dialog event loop
        self.aboutDlg.exec_()
        
    def reverse(self):
        widget = self.iface.messageBar().createMessage(
                QCoreApplication.translate("geopunt4Qgis" ,"Zoek een Adres: "), 
                QCoreApplication.translate("geopunt4Qgis" ,'Klik op de kaart om het adres op te vragen'))
                    
        helpBtn = QPushButton("Help", widget)
        helpBtn.clicked.connect(self.openReverseHelp)
        widget.layout().addWidget(helpBtn)
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushWidget(widget, level=QgsMessageBar.INFO)

        reverseAdresTool = reverseAdresMapTool(self.iface, self._reverseAdresCallback) 
        self.iface.mapCanvas().setMapTool(reverseAdresTool)
        
    def _reverseAdresCallback(self, point):
        self._addMarker( point )
        lam72 = QgsCoordinateReferenceSystem(31370)
        mapCrs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        xform = QgsCoordinateTransform(mapCrs, lam72)
        lam72pt = xform.transform(point)
        
        #to clear or not clear that is the question
        self.iface.messageBar().clearWidgets()
        
        #fetch Location from geopunt
        adres = self.adres.fetchLocation( str( lam72pt.x() ) + "," + str( lam72pt.y() ), 1)
        Timer( 3, self._clearGraphicLayer, ()).start()
    
        if len(adres) and adres.__class__ is list:
            #only one result in list, was set in request
            FormattedAddress = adres[0]["FormattedAddress"]
      
            #add a button to the messageBar widget
            widget = self.iface.messageBar().createMessage(QCoreApplication.translate("geopunt4Qgis", "Resultaat: "), FormattedAddress)
            
            xlam72, ylam72 = adres[0]["Location"]["X_Lambert72"], adres[0]["Location"]["Y_Lambert72"]    
            xy = self.gh.prjPtToMapCrs([xlam72, ylam72], 31370)            
            self._addMarker( xy, QColor(0,255,200))
            
            button = QPushButton(widget)
            button.clicked.connect(lambda: self._addReverse(adres[0]))
            button.setText(QCoreApplication.translate("geopunt4Qgis" ,"Voeg toe"))
            
            widget.layout().addWidget(button)
            
            self.iface.messageBar().clearWidgets()
            self.iface.messageBar().pushWidget(widget, level=QgsMessageBar.INFO)
    
        elif len(adres) == 0:
            self.iface.messageBar().pushMessage(QCoreApplication.translate("geopunt4Qgis","Waarschuwing"),
            QCoreApplication.translate("geopunt4Qgis", "Geen resultaten gevonden"), 
                    level=QgsMessageBar.INFO, duration=3)
      
        elif adres.__class__ is str:
            self.iface.messageBar().pushMessage(QCoreApplication.translate("geopunt4Qgis", "Waarschuwing"),
                adres, level=QgsMessageBar.WARNING)
        else:
            self.iface.messageBar().pushMessage("Error", 
            QCoreApplication.translate("geopunt4Qgis","onbekende fout"), level=QgsMessageBar.CRITICAL)
      
    def _addReverse(self, adres):
        formattedAddress, locationType = adres["FormattedAddress"] , adres["LocationType"]
        xlam72, ylam72 = adres["Location"]["X_Lambert72"] , adres["Location"]["Y_Lambert72"]
    
        if not hasattr(self, 'layerName_reverse'):
           layerName, accept = QInputDialog.getText(None,
             QCoreApplication.translate("geopunt4Qgis", 'Laag toevoegen'),
             QCoreApplication.translate("geopunt4Qgis", 'Geef een naam voor de laag op:') )
           if accept == False: return
           else:  self.layerName_reverse = layerName
           
        xy = self.gh.prjPtToMapCrs([xlam72, ylam72], 31370)
        self.gh.save_adres_point(xy, formattedAddress, locationType, layername=self.layerName_reverse, 
          startFolder=os.path.join( self.startDir, self.layerName_reverse), saveToFile=self.saveToFile_reverse ,
          sender=self.iface.mainWindow())
        self.iface.messageBar().popWidget()	
        self._clearGraphicLayer()
        
    def openReverseHelp(self):
        webbrowser.open_new_tab("http://kgis.be/index.html#!geopuntReverse.md")
                
    def _addMarker(self, pnt, clr=QColor(255,255,0)):
        m = QgsVertexMarker(self.iface.mapCanvas())
        m.setCenter( pnt )
        m.setColor(clr)
        m.setIconSize(1)
        m.setIconType(QgsVertexMarker.ICON_BOX) 
        m.setPenWidth(9)
        self.graphicsLayer.append(m)
        return m
      
    def _clearGraphicLayer(self):
      for graphic in  self.graphicsLayer: 
        self.iface.mapCanvas().scene().removeItem(graphic)
      self.graphicsLayer = []