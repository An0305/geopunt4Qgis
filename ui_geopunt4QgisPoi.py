# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geopunt4QgisPoi.ui'
#
# Created: Mon Dec  9 20:58:27 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_geopunt4QgisPoiDlg(object):
    def setupUi(self, geopunt4QgisPoiDlg):
        geopunt4QgisPoiDlg.setObjectName(_fromUtf8("geopunt4QgisPoiDlg"))
        geopunt4QgisPoiDlg.resize(450, 376)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geopunt4Qgis/images/geopuntPoiSmall.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        geopunt4QgisPoiDlg.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(geopunt4QgisPoiDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(geopunt4QgisPoiDlg)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.poiText = QtGui.QLineEdit(self.groupBox)
        self.poiText.setObjectName(_fromUtf8("poiText"))
        self.horizontalLayout.addWidget(self.poiText)
        self.zoekKnop = QtGui.QPushButton(self.groupBox)
        self.zoekKnop.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geopunt4Qgis/images/binocularsSmall.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoekKnop.setIcon(icon1)
        self.zoekKnop.setObjectName(_fromUtf8("zoekKnop"))
        self.horizontalLayout.addWidget(self.zoekKnop)
        self.verticalLayout.addWidget(self.groupBox)
        self.currentBoundsVink = QtGui.QCheckBox(geopunt4QgisPoiDlg)
        self.currentBoundsVink.setEnabled(True)
        self.currentBoundsVink.setObjectName(_fromUtf8("currentBoundsVink"))
        self.verticalLayout.addWidget(self.currentBoundsVink)
        self.resultLijst = QtGui.QListWidget(geopunt4QgisPoiDlg)
        self.resultLijst.setObjectName(_fromUtf8("resultLijst"))
        self.verticalLayout.addWidget(self.resultLijst)
        self.widget = QtGui.QWidget(geopunt4QgisPoiDlg)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.zoomSelKnop = QtGui.QPushButton(self.widget)
        self.zoomSelKnop.setObjectName(_fromUtf8("zoomSelKnop"))
        self.horizontalLayout_2.addWidget(self.zoomSelKnop)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(geopunt4QgisPoiDlg)
        QtCore.QMetaObject.connectSlotsByName(geopunt4QgisPoiDlg)

    def retranslateUi(self, geopunt4QgisPoiDlg):
        geopunt4QgisPoiDlg.setWindowTitle(_translate("geopunt4QgisPoiDlg", "Zoek een Locatie via geopunt", None))
        self.groupBox.setTitle(_translate("geopunt4QgisPoiDlg", "Zoek naar een plaats:", None))
        self.currentBoundsVink.setText(_translate("geopunt4QgisPoiDlg", "Beperk zoekresultaten tot huidige extent", None))
        self.zoomSelKnop.setText(_translate("geopunt4QgisPoiDlg", "Zoom naar selectie", None))

import resources_rc
