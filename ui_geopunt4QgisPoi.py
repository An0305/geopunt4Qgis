# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geopunt4QgisPoi.ui'
#
# Created: Thu Nov 20 18:45:01 2014
#      by: PyQt4 UI code generator 4.10.4
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
        geopunt4QgisPoiDlg.resize(562, 574)
        geopunt4QgisPoiDlg.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        geopunt4QgisPoiDlg.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geopunt4Qgis/images/geopuntPoiSmall.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        geopunt4QgisPoiDlg.setWindowIcon(icon)
        geopunt4QgisPoiDlg.setSizeGripEnabled(False)
        self.verticalLayout = QtGui.QVBoxLayout(geopunt4QgisPoiDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.filterBox = QtGui.QGroupBox(geopunt4QgisPoiDlg)
        self.filterBox.setFlat(False)
        self.filterBox.setCheckable(False)
        self.filterBox.setObjectName(_fromUtf8("filterBox"))
        self.gridLayout = QtGui.QGridLayout(self.filterBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.currentBoundsVink = QtGui.QCheckBox(self.filterBox)
        self.currentBoundsVink.setEnabled(True)
        self.currentBoundsVink.setTristate(False)
        self.currentBoundsVink.setObjectName(_fromUtf8("currentBoundsVink"))
        self.gridLayout.addWidget(self.currentBoundsVink, 0, 1, 1, 1)
        self.filterWgt = QtGui.QWidget(self.filterBox)
        self.filterWgt.setObjectName(_fromUtf8("filterWgt"))
        self.formLayout = QtGui.QFormLayout(self.filterWgt)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.filterLbl0 = QtGui.QLabel(self.filterWgt)
        self.filterLbl0.setObjectName(_fromUtf8("filterLbl0"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.filterLbl0)
        self.filterPoiNIS = QtGui.QComboBox(self.filterWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterPoiNIS.sizePolicy().hasHeightForWidth())
        self.filterPoiNIS.setSizePolicy(sizePolicy)
        self.filterPoiNIS.setObjectName(_fromUtf8("filterPoiNIS"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.filterPoiNIS)
        self.filterLbl1 = QtGui.QLabel(self.filterWgt)
        self.filterLbl1.setObjectName(_fromUtf8("filterLbl1"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.filterLbl1)
        self.filterPoiThemeCombo = QtGui.QComboBox(self.filterWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterPoiThemeCombo.sizePolicy().hasHeightForWidth())
        self.filterPoiThemeCombo.setSizePolicy(sizePolicy)
        self.filterPoiThemeCombo.setEditable(False)
        self.filterPoiThemeCombo.setObjectName(_fromUtf8("filterPoiThemeCombo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.filterPoiThemeCombo)
        self.filterPoiCategoryCombo = QtGui.QComboBox(self.filterWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterPoiCategoryCombo.sizePolicy().hasHeightForWidth())
        self.filterPoiCategoryCombo.setSizePolicy(sizePolicy)
        self.filterPoiCategoryCombo.setObjectName(_fromUtf8("filterPoiCategoryCombo"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.filterPoiCategoryCombo)
        self.filterPoiTypeCombo = QtGui.QComboBox(self.filterWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterPoiTypeCombo.sizePolicy().hasHeightForWidth())
        self.filterPoiTypeCombo.setSizePolicy(sizePolicy)
        self.filterPoiTypeCombo.setObjectName(_fromUtf8("filterPoiTypeCombo"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.filterPoiTypeCombo)
        self.filterLbl2 = QtGui.QLabel(self.filterWgt)
        self.filterLbl2.setObjectName(_fromUtf8("filterLbl2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.filterLbl2)
        self.poiText = QtGui.QLineEdit(self.filterWgt)
        self.poiText.setObjectName(_fromUtf8("poiText"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.poiText)
        self.filterLbl3 = QtGui.QLabel(self.filterWgt)
        self.filterLbl3.setObjectName(_fromUtf8("filterLbl3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.filterLbl3)
        self.label = QtGui.QLabel(self.filterWgt)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label)
        self.gridLayout.addWidget(self.filterWgt, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.filterBox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.zoekKnop = QtGui.QPushButton(geopunt4QgisPoiDlg)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geopunt4Qgis/images/magnifyingGlass.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoekKnop.setIcon(icon1)
        self.zoekKnop.setAutoDefault(True)
        self.zoekKnop.setDefault(True)
        self.zoekKnop.setObjectName(_fromUtf8("zoekKnop"))
        self.horizontalLayout_3.addWidget(self.zoekKnop)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.resultLijst = QtGui.QTableWidget(geopunt4QgisPoiDlg)
        self.resultLijst.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.resultLijst.setFrameShape(QtGui.QFrame.StyledPanel)
        self.resultLijst.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.resultLijst.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.resultLijst.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.resultLijst.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.resultLijst.setRowCount(0)
        self.resultLijst.setObjectName(_fromUtf8("resultLijst"))
        self.resultLijst.setColumnCount(6)
        item = QtGui.QTableWidgetItem()
        self.resultLijst.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.resultLijst.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.resultLijst.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.resultLijst.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.resultLijst.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.resultLijst.setHorizontalHeaderItem(5, item)
        self.resultLijst.horizontalHeader().setSortIndicatorShown(True)
        self.resultLijst.horizontalHeader().setStretchLastSection(False)
        self.resultLijst.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.resultLijst)
        self.buttonWgt = QtGui.QWidget(geopunt4QgisPoiDlg)
        self.buttonWgt.setObjectName(_fromUtf8("buttonWgt"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.buttonWgt)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.addToMapKnop = QtGui.QPushButton(self.buttonWgt)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geopunt4Qgis/images/addPointLayer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addToMapKnop.setIcon(icon2)
        self.addToMapKnop.setAutoDefault(False)
        self.addToMapKnop.setObjectName(_fromUtf8("addToMapKnop"))
        self.horizontalLayout_2.addWidget(self.addToMapKnop)
        self.zoomSelKnop = QtGui.QPushButton(self.buttonWgt)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geopunt4Qgis/images/binocularsSmall.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomSelKnop.setIcon(icon3)
        self.zoomSelKnop.setAutoDefault(False)
        self.zoomSelKnop.setObjectName(_fromUtf8("zoomSelKnop"))
        self.horizontalLayout_2.addWidget(self.zoomSelKnop)
        self.verticalLayout.addWidget(self.buttonWgt)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.addMinModelBtn = QtGui.QPushButton(geopunt4QgisPoiDlg)
        self.addMinModelBtn.setObjectName(_fromUtf8("addMinModelBtn"))
        self.horizontalLayout_4.addWidget(self.addMinModelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.buttonBoxLayout = QtGui.QHBoxLayout()
        self.buttonBoxLayout.setObjectName(_fromUtf8("buttonBoxLayout"))
        self.msgLbl = QtGui.QLabel(geopunt4QgisPoiDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msgLbl.sizePolicy().hasHeightForWidth())
        self.msgLbl.setSizePolicy(sizePolicy)
        self.msgLbl.setFrameShape(QtGui.QFrame.Panel)
        self.msgLbl.setFrameShadow(QtGui.QFrame.Sunken)
        self.msgLbl.setText(_fromUtf8(""))
        self.msgLbl.setObjectName(_fromUtf8("msgLbl"))
        self.buttonBoxLayout.addWidget(self.msgLbl)
        self.buttonBox = QtGui.QDialogButtonBox(geopunt4QgisPoiDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Help)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.buttonBoxLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.buttonBoxLayout)
        self.actionZoomtoSelection = QtGui.QAction(geopunt4QgisPoiDlg)
        self.actionZoomtoSelection.setObjectName(_fromUtf8("actionZoomtoSelection"))
        self.actionAddTSeltoMap = QtGui.QAction(geopunt4QgisPoiDlg)
        self.actionAddTSeltoMap.setObjectName(_fromUtf8("actionAddTSeltoMap"))

        self.retranslateUi(geopunt4QgisPoiDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), geopunt4QgisPoiDlg.close)
        QtCore.QObject.connect(self.filterBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.filterWgt.setVisible)
        QtCore.QObject.connect(self.currentBoundsVink, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.filterLbl0.setDisabled)
        QtCore.QObject.connect(self.currentBoundsVink, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.filterPoiNIS.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(geopunt4QgisPoiDlg)

    def retranslateUi(self, geopunt4QgisPoiDlg):
        geopunt4QgisPoiDlg.setWindowTitle(_translate("geopunt4QgisPoiDlg", "Zoek een interessante plaats via Geopunt", None))
        self.filterBox.setTitle(_translate("geopunt4QgisPoiDlg", "Filters", None))
        self.currentBoundsVink.setText(_translate("geopunt4QgisPoiDlg", "Beperk zoekresultaten tot huidige zoomniveau", None))
        self.filterLbl0.setText(_translate("geopunt4QgisPoiDlg", "Gemeente:", None))
        self.filterLbl1.setText(_translate("geopunt4QgisPoiDlg", "Thema:", None))
        self.filterLbl2.setText(_translate("geopunt4QgisPoiDlg", "Categorie:", None))
        self.filterLbl3.setText(_translate("geopunt4QgisPoiDlg", "Type:", None))
        self.label.setText(_translate("geopunt4QgisPoiDlg", "Sleutelwoord:", None))
        self.zoekKnop.setText(_translate("geopunt4QgisPoiDlg", "Zoek", None))
        self.resultLijst.setSortingEnabled(True)
        item = self.resultLijst.horizontalHeaderItem(0)
        item.setText(_translate("geopunt4QgisPoiDlg", "id", None))
        item = self.resultLijst.horizontalHeaderItem(1)
        item.setText(_translate("geopunt4QgisPoiDlg", "Thema", None))
        item = self.resultLijst.horizontalHeaderItem(2)
        item.setText(_translate("geopunt4QgisPoiDlg", "Categorie", None))
        item = self.resultLijst.horizontalHeaderItem(3)
        item.setText(_translate("geopunt4QgisPoiDlg", "Type", None))
        item = self.resultLijst.horizontalHeaderItem(4)
        item.setText(_translate("geopunt4QgisPoiDlg", "Naam", None))
        item = self.resultLijst.horizontalHeaderItem(5)
        item.setText(_translate("geopunt4QgisPoiDlg", "CRAB adres", None))
        self.addToMapKnop.setText(_translate("geopunt4QgisPoiDlg", "Voeg selectie toe aan kaart", None))
        self.zoomSelKnop.setText(_translate("geopunt4QgisPoiDlg", "Zoom naar selectie", None))
        self.addMinModelBtn.setToolTip(_translate("geopunt4QgisPoiDlg", "Voeg alle POI’s toe die voldoen aan de criteria. \n"
"Indien meer dan 1000 punten zal een gedeelte geclusterd worden", None))
        self.addMinModelBtn.setText(_translate("geopunt4QgisPoiDlg", "Voeg alle punten toe", None))
        self.actionZoomtoSelection.setText(_translate("geopunt4QgisPoiDlg", "Zoom naar Selectie", None))
        self.actionAddTSeltoMap.setText(_translate("geopunt4QgisPoiDlg", "Voeg selectie toe aan kaart", None))

import resources_rc
