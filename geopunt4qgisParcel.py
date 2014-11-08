# -*- coding: utf-8 -*-
"""
/***************************************************************************
geopunt4qgisdialog
                A QGIS plugin
"Tool om geopunt in QGIS te gebruiken"
                -------------------
    begin                : 2014-11-08
    copyright            : (C) 2014 by Kay Warrie
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
from ui_geopunt4qgisParcel import Ui_geopunt4QgisParcelDlg
from qgis.core import *
from qgis.gui import  QgsMessageBar, QgsVertexMarker, QgsRubberBand
import geopunt, os, json, webbrowser
from geometryhelper import geometryHelper

class geopunt4QgisParcelDlg(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self, None)
        self.setWindowFlags( self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint )
        #self.setWindowFlags( self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
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
        self.ui = Ui_geopunt4QgisParcelDlg()
        self.ui.setupUi(self)
        self.ui.buttonBox.addButton( QtGui.QPushButton("Sluiten"), QtGui.QDialogButtonBox.RejectRole  )

        #get settings
        self.s = QtCore.QSettings()
        self.loadSettings()

        #setup geometryHelper object
        self.gh = geometryHelper(self.iface)
        
        #variables
        self.firstShow = True 
        self.municipalities = []
        self.departments = []
        self.sections = []
        self.parcels = []
        self.graphics = []
        
        #event handlers 
        self.ui.municipalityCbx.currentIndexChanged.connect(self.municipalityChanged)
        self.ui.departmentCbx.currentIndexChanged.connect( self.departmentChanged )
        self.ui.sectionCbx.currentIndexChanged.connect(self.sectionChanged)
        self.ui.parcelCbx.currentIndexChanged.connect(self.parcelChanged)
        self.ui.ZoomKnop_muni.clicked.connect(self.zoomTo)
        self.ui.ZoomKnop_dep.clicked.connect(self.zoomTo)
        self.ui.ZoomKnop_sect.clicked.connect(self.zoomTo)
        self.ui.ZoomKnop_parcel.clicked.connect(self.zoomTo)
        self.ui.buttonBox.helpRequested.connect(self.openHelp)
        self.finished.connect( self.clearGraphics )
        
    def loadSettings(self):
        self.timeout =  int( self.s.value("geopunt4qgis/timeout" ,15))
        if int( self.s.value("geopunt4qgis/useProxy" , 0)):
            self.proxy = self.s.value("geopunt4qgis/proxyHost" ,"")
            self.port = self.s.value("geopunt4qgis/proxyPort" ,"")
        else:
            self.proxy = ""
            self.port = ""
        self.parcel = geopunt.parcel(self.timeout, self.proxy, self.port )
        
    def show(self):
        QtGui.QDialog.show(self)
        if self.firstShow:
             inet =  geopunt.internet_on( proxyUrl=self.proxy, port=self.port, timeout=self.timeout )
             if inet:
                self.firstShow = False
                
                self.municipalities = self.parcel.getMunicipalities()
                self.ui.municipalityCbx.clear()
                self.ui.municipalityCbx.addItems( [''] + [n['municipalityName'] for n in self.municipalities] )
             else:
                self.bar.pushMessage(
                  QtCore.QCoreApplication.translate("geopunt4QgisParcelDlg", "Waarschuwing "), 
                  QtCore.QCoreApplication.translate("geopunt4QgisParcelDlg", 
                    "Kan geen verbing maken met het internet."), level=QgsMessageBar.WARNING, duration=3)
        
    def municipalityChanged(self):
        municipality= self.ui.municipalityCbx.currentText()
        
        if municipality == '': return
      
        niscode = [n['municipalityCode'] for n in self.municipalities if n['municipalityName'] == municipality ][0]
        self.departments = self.parcel.getDepartments(niscode)
        
        self.ui.departmentCbx.clear()
        self.ui.departmentCbx.addItems(['']+ [n['departmentName'] for n in self.departments] )
        self.ui.sectionCbx.clear()
        self.ui.parcelCbx.clear()
        self.ui.Add2mapKnop.setEnabled(False)
  
    def departmentChanged(self):
        department = self.ui.departmentCbx.currentText()
        municipality= self.ui.municipalityCbx.currentText()

        if municipality == '' or department == '': return

        niscode = [n['municipalityCode'] for n in self.municipalities if n['municipalityName'] == municipality ][0]
        departmentcode = [n['departmentCode'] for n in self.departments if n['departmentName'] == department ][0]
        self.sections = [n['sectionCode'] for n in self.parcel.getSections(niscode, departmentcode)]

        self.ui.sectionCbx.clear()
        self.ui.sectionCbx.addItems([''] + self.sections)
        self.ui.parcelCbx.clear()
        self.ui.Add2mapKnop.setEnabled(False)

    def sectionChanged(self):
        department = self.ui.departmentCbx.currentText()
        municipality= self.ui.municipalityCbx.currentText()
        section = self.ui.sectionCbx.currentText()
        
        if municipality == '' or department == '' or section == '': return
        
        niscode = [n['municipalityCode'] for n in self.municipalities if n['municipalityName'] == municipality ][0]
        departmentcode = [n['departmentCode'] for n in self.departments if n['departmentName'] == department ][0]
        self.parcels = self.parcel.getParcels( niscode, departmentcode, section )
        
        self.ui.parcelCbx.clear()
        self.ui.parcelCbx.addItems([''] + [n['perceelnummer'] for n in self.parcels])
        
        self.ui.Add2mapKnop.setEnabled(False)

    def parcelChanged(self):
        self.ui.Add2mapKnop.setEnabled( self.ui.parcelCbx.currentText() != '' )

    def zoomTo(self):
        sender = self.sender()
        municipality= self.ui.municipalityCbx.currentText()
        if municipality:
            niscode = [n['municipalityCode'] for n in self.municipalities if n['municipalityName'] == municipality ][0]
            self.clearGraphics()
        else: 
            niscode = None
        department = self.ui.departmentCbx.currentText()
        if department:
            departmentcode = [n['departmentCode'] for n in self.departments if n['departmentName'] == department ][0]
        else:
            departmentcode = None
        section = self.ui.sectionCbx.currentText()
        parcelNr = self.ui.parcelCbx.currentText()
        
        if sender is self.ui.ZoomKnop_muni and municipality != '':
            muniInfo = self.parcel.getMunicipalitieInfo( niscode, 31370, 'full') 
            bbox= json.loads( muniInfo['geometry']['boundingBox'])['coordinates'][0]
            self.clearGraphics()
            self.gh.zoomtoRec( bbox[0], bbox[2], 31370 )        
            shape = json.loads( muniInfo['geometry']['shape'])
            self.addPolygonFromJson( shape )
            return
        if sender is self.ui.ZoomKnop_dep and department != '':
            depInfo = self.parcel.getDepartmentInfo( niscode, departmentcode, 31370, 'full') 
            bbox= json.loads( depInfo['geometry']['boundingBox'])['coordinates'][0]
            self.clearGraphics()
            self.gh.zoomtoRec( bbox[0], bbox[2], 31370 )
            shape = json.loads( depInfo['geometry']['shape'])
            self.addPolygonFromJson( shape )
            return
        if sender is self.ui.ZoomKnop_sect and section != '':
            sectInfo = self.parcel.getSectionInfo( niscode, departmentcode, section, 31370, 'full') 
            bbox= json.loads( sectInfo['geometry']['boundingBox'])['coordinates'][0]
            self.clearGraphics()
            self.gh.zoomtoRec( bbox[0], bbox[2], 31370 )
            shape = json.loads( sectInfo['geometry']['shape'])
            self.addPolygonFromJson( shape )
            return
        if sender is self.ui.ZoomKnop_parcel and parcelNr != '':
            parcelInfo = self.parcel.getParcel( niscode, departmentcode, section, parcelNr, 31370, 'full') 
            bbox= json.loads( parcelInfo['geometry']['boundingBox'])['coordinates'][0]
            self.clearGraphics()
            self.gh.zoomtoRec( bbox[0], bbox[2], 31370 )
            shape = json.loads( parcelInfo['geometry']['shape'])
            self.addPolygonFromJson( shape )
            return

    def openHelp(self):
        webbrowser.open_new_tab("http://www.geopunt.be/voor-experts/geopunt-plugins/functionaliteiten")

    def addPolygonFromJson(self, geojson ):
        canvas = self.iface.mapCanvas()
        prjPolygon = []
        rings = geojson['coordinates']
        for ring in rings:
           prjRing = self.gh.prjLineToMapCrs( ring, 31370 )
           prjPolygon.append( prjRing.asPolyline() )
        
        gPolygon = QgsGeometry.fromPolygon( prjPolygon )
        rBand = QgsRubberBand(canvas, True) 
        self.graphics.append( rBand )
        rBand.setToGeometry( gPolygon, None )
        rBand.setColor(QtGui.QColor(0,0,255, 70))
        rBand.setBorderColor( QtGui.QColor(70,70,70, 220) )
        rBand.setWidth(3)

    def clearGraphics(self):
        canvas = self.iface.mapCanvas()
        for g in self.graphics:
            canvas.scene().removeItem(g)
    