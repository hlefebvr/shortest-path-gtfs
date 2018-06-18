#!/usr/bin/python3
# -*- coding: utf-8 -*-

# PyQt Graphical imports
from PyQt4.QtGui import QMainWindow, QSplitter, QWidget, \
                        QHBoxLayout, QVBoxLayout, QTableWidget, QCheckBox, \
                        QLabel, QComboBox, QPushButton, QHeaderView, \
                        QMessageBox, QFileDialog, QProgressBar, QTableWidgetItem, \
                        QErrorMessage, QColor, QHeaderView, QAction
from PyQt4.QtCore import Qt, QCoreApplication

# MatPlotLib imports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.basemap import Basemap

# Standard imports
from random import randint

# Local imports
from .functions import str0, strh
from .graphics import ProgressWindow, ReduceStopsWindow

class View(QMainWindow):
    
    class UI():
        def __init__(self):
            self.centralWidget = QSplitter(Qt.Vertical)

            # Query Panel
            self.queryPanel = QWidget()
            self.queryPanelLayout = QHBoxLayout()
            self.queryPanel.setLayout(self.queryPanelLayout)

            ## Query Graphic Panel
            self.figure = plt.figure()
            self.canvas = FigureCanvas(self.figure)
            self.queryPanelLayout.addWidget(self.canvas, 75)
            self.highlightPlot = None

            ## Query Configuration Panel
            self.queryConfigurationPanel = QWidget()
            self.queryPanelLayout.addWidget(self.queryConfigurationPanel, 25)

            self.queryConfigurationPanelLayout = QVBoxLayout()
            self.queryConfigurationPanel.setLayout(self.queryConfigurationPanelLayout)

            ## Label for query configuration
            self.queryConfigurationTitleLabel = QLabel('<b>Configuration : </b>')
            self.queryConfigurationPanelLayout.addWidget(self.queryConfigurationTitleLabel)

            ### Mode selector
            #### First line
            self.queryModeSelector = QWidget()
            self.queryConfigurationPanelLayout.addWidget(self.queryModeSelector)
            
            self.queryModeSelectorLayout = QHBoxLayout()
            self.queryModeSelector.setLayout(self.queryModeSelectorLayout)
            
            self.queryModeTramway = QCheckBox("Tramway")
            self.queryModeSelectorLayout.addWidget(self.queryModeTramway)
            self.queryModeMetro = QCheckBox("Metro")
            self.queryModeSelectorLayout.addWidget(self.queryModeMetro)
            self.queryModeBus = QCheckBox("Bus")
            self.queryModeSelectorLayout.addWidget(self.queryModeBus)
            self.queryModeTrain = QCheckBox("Train")
            self.queryModeSelectorLayout.addWidget(self.queryModeTrain)

            #### Second line
            self.queryModeSelector2 = QWidget()
            self.queryConfigurationPanelLayout.addWidget(self.queryModeSelector2)
            
            self.queryModeSelectorLayout2 = QHBoxLayout()
            self.queryModeSelector2.setLayout(self.queryModeSelectorLayout2)
            
            self.queryModeFerry = QCheckBox("Ferry")
            self.queryModeSelectorLayout2.addWidget(self.queryModeFerry)
            self.queryModeTramwayCable = QCheckBox("Tramway à cable")
            self.queryModeSelectorLayout2.addWidget(self.queryModeTramwayCable)
            self.queryModeTelepherique = QCheckBox("Téléphérique")
            self.queryModeSelectorLayout2.addWidget(self.queryModeTelepherique)
            self.queryModeFuniculaire = QCheckBox("Funiculaire")
            self.queryModeSelectorLayout2.addWidget(self.queryModeFuniculaire)

            #### Check all modes
            self.queryModeTramway.setCheckState(Qt.Checked)
            self.queryModeMetro.setCheckState(Qt.Checked)
            self.queryModeBus.setCheckState(Qt.Checked)
            self.queryModeTrain.setCheckState(Qt.Checked)
            self.queryModeTramwayCable.setCheckState(Qt.Checked)
            self.queryModeFerry.setCheckState(Qt.Checked)
            self.queryModeFuniculaire.setCheckState(Qt.Checked)
            self.queryModeTelepherique.setCheckState(Qt.Checked)

            ### Stops selector
            self.queryStopSelector = QWidget()
            self.queryConfigurationPanelLayout.addWidget(self.queryStopSelector)

            self.queryStopSelectorLayout = QHBoxLayout()
            self.queryStopSelector.setLayout(self.queryStopSelectorLayout)

            self.queryStopStartLabel = QLabel("Départ : ")
            self.queryStopSelectorLayout.addWidget(self.queryStopStartLabel)

            self.queryStopStartNode = QComboBox()
            self.queryStopSelectorLayout.addWidget(self.queryStopStartNode)

            self.queryStopStartTime = QComboBox()
            self.queryStopSelectorLayout.addWidget(self.queryStopStartTime)
            self.queryStopStartTime.addItem('')
            for h in range(7, 22):
                for m in range(0, 60, 5):
                    self.queryStopStartTime.addItem(str0(h) + ':' + str0(m))

            self.queryStopStartLabel = QLabel("Arrivée : ")
            self.queryStopSelectorLayout.addWidget(self.queryStopStartLabel)

            self.queryStopEndNode = QComboBox()
            self.queryStopSelectorLayout.addWidget(self.queryStopEndNode)

            ## Label for query execution
            self.queryConfigurationExecutionLabel = QLabel('<b>Exécuter : </b>')
            self.queryConfigurationPanelLayout.addWidget(self.queryConfigurationExecutionLabel)

            ## Query buttons
            self.queryDijkstraButton = QPushButton('Chercher')
            self.queryConfigurationPanelLayout.addWidget(self.queryDijkstraButton)

            ## Stretch
            self.queryConfigurationPanelLayout.addStretch(100)

            # Result Panel
            self.resultPanel = QTableWidget()

            # Add panels to splitter
            self.centralWidget.addWidget(self.queryPanel)
            self.centralWidget.addWidget(self.resultPanel)

    def __init__(self, controller):
        QMainWindow.__init__(self)

        self.controller = controller
        self.ui = self.UI()
        
        self.setWindowTitle('TX : Exploitation de données pour algorithmes de graphes multimodaux')
        self.setCentralWidget(self.ui.centralWidget)
        self.progressBar = None

        # Menu
        # exitAction.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()

        ## Fichier
        self.changeWorkspaceAction = QAction("Changer de dossier source", self)
        self.exitAction = QAction("Quitter", self)
        self.fileMenu = menubar.addMenu('&Fichier')
        self.fileMenu.addAction(self.changeWorkspaceAction)
        self.fileMenu.addAction(self.exitAction)

        ## A propos
        self.showReportAction = QAction("Voir le rapport (pdf)", self)
        self.aboutAction = QAction("À propos", self)
        self.aboutMenu = menubar.addMenu('À propos')
        self.aboutMenu.addAction(self.showReportAction)
        self.aboutMenu.addAction(self.aboutAction)

        # Connect SLOTS and SIGNALS
        self.ui.queryModeTramway.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))
        self.ui.queryModeBus.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))
        self.ui.queryModeMetro.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))
        self.ui.queryModeFerry.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))
        self.ui.queryModeFuniculaire.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))
        self.ui.queryModeTelepherique.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))
        self.ui.queryModeTrain.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))
        self.ui.queryModeTramwayCable.stateChanged.connect(lambda _ : self.controller.reloadStops(self.getSelectedModes()))

        self.ui.queryStopStartNode.currentIndexChanged.connect(self.highlightSlectedStops)
        self.ui.queryStopEndNode.currentIndexChanged.connect(self.highlightSlectedStops)

        self.ui.queryDijkstraButton.clicked.connect(lambda _ : self.controller.runShortestPath(self.getSelectedModes(), self.getExecutionConfiguration()))

        self.changeWorkspaceAction.triggered.connect(self.controller.changeWorkspace)
        self.exitAction.triggered.connect(self.controller.exit)

        # Let the show begin
        self.show()

    # OTHER WINDOWS

    def askNewWorkspace(self, default, confirm = False):
        if not confirm or QMessageBox.Yes == QMessageBox.question(self, 'Dossier de travail', 'Vous n\'avez pas encore séléctionné d\'espace de travail.\nVoulez vous sélectionner un dossier GTFS ?', QMessageBox.No | QMessageBox.Yes):
            return QFileDialog.getExistingDirectory(self, "Choisissez votre espace de travail", default)
        else: self.controller.exit()

    def askInitWorkspace(self):
        reply = QMessageBox.question(self, 'Dossier de travail non initialisé', 'Le dossier séléctionné est valide mais n\'a pas encore été initialisé.\nVoulez-vous le faire maintenant ?', QMessageBox.No | QMessageBox.Yes)
        return True if reply == QMessageBox.Yes else self.controller.exit()
    
    def askInitWorkspaceParameters(self, lat, lon, r):
        window = ReduceStopsWindow(lat, lon, r)
        return window.get()

    def showLoading(self, txt): print(txt)

    def showError(self, errorMsg = "ERROR"):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Erreur")
        msg.setInformativeText(errorMsg)
        msg.setWindowTitle("Erreur")
        msg.show()

    # INTERFACE

    def fillStopSelectors(self, ids, names):
        self.ui.queryStopStartNode.clear()
        self.ui.queryStopEndNode.clear()
        n = len(ids)
        for i in range(n):
            self.ui.queryStopStartNode.addItem(names[i], userData = ids[i])
            self.ui.queryStopEndNode.addItem(names[i], userData = ids[i])
        self.ui.queryStopStartNode.setCurrentIndex(randint(0, n))
        self.ui.queryStopEndNode.setCurrentIndex(randint(0, n))

    def getSelectedModes(self):
        modes = []
        if self.ui.queryModeTramway.checkState() == Qt.Checked: modes += [0]
        if self.ui.queryModeMetro.checkState() == Qt.Checked: modes += [1]
        if self.ui.queryModeTrain.checkState() == Qt.Checked: modes += [2]
        if self.ui.queryModeBus.checkState() == Qt.Checked: modes += [3]
        if self.ui.queryModeFerry.checkState() == Qt.Checked: modes += [4]
        if self.ui.queryModeTramwayCable.checkState() == Qt.Checked: modes += [5]
        if self.ui.queryModeTelepherique.checkState() == Qt.Checked: modes += [6]
        if self.ui.queryModeFuniculaire.checkState() == Qt.Checked: modes += [7]
        return modes

    def getExecutionConfiguration(self):
        return {
            'from_stop_id' : self.ui.queryStopEndNode.itemData(self.ui.queryStopEndNode.currentIndex()),
            'to_stop_id' : self.ui.queryStopStartNode.itemData(self.ui.queryStopStartNode.currentIndex()),
            'departure_time' : self.ui.queryStopStartTime.currentText()
        }

    def fillResultTable(self, stop_times, stop_names, route_types, route_names, route_colors):
        route_type_str = { 0: 'Tramway/Métro Léger', 1: 'Metro', 2: 'Train', 3: 'Bus', 4: 'Ferry', 5: 'Tramway cable', 6: 'Téléphérique', 7: 'Funiculaire' }
        n = len(stop_times)
        
        self.ui.resultPanel.clear()
        for i in reversed(range(self.ui.resultPanel.columnCount())): self.ui.resultPanel.removeColumn(i)
        for i in reversed(range(self.ui.resultPanel.rowCount())): self.ui.resultPanel.removeRow(i)
        for i in range(3): self.ui.resultPanel.insertRow(i)
        self.ui.resultPanel.setRowHeight(0, 10)
        
        current_route = ( route_types[0], route_names[0] )
        current_route_index = 0
        
        for i in range(n):
            if current_route != ( route_types[i], route_names[i] ):
                span_width = i - current_route_index
                if span_width != 1:
                    self.ui.resultPanel.setSpan(0, current_route_index, 1, span_width)
                    self.ui.resultPanel.setSpan(1, current_route_index, 1, span_width)
                current_route = ( route_types[i], route_names[i] )
                current_route_index = i
            
            self.ui.resultPanel.insertColumn(i)
            # Stop times
            self.ui.resultPanel.setHorizontalHeaderItem(i, QTableWidgetItem(strh(stop_times[i])))
            
            # Routes
            self.ui.resultPanel.setItem(0, i, QTableWidgetItem())
            color = route_colors[i]
            try: color = '#%s' % color if color[0] != '#' else color
            except: color = '#ffffff'
            self.ui.resultPanel.item(0, i).setBackground(QColor(color))
            route = '%s, ligne %s' % ( route_type_str[route_types[i]], route_names[i] )
            self.ui.resultPanel.setItem(1, i, QTableWidgetItem(route))
            self.ui.resultPanel.item(1, i).setTextAlignment(Qt.AlignCenter)
            
            # Stop names
            self.ui.resultPanel.setItem(2, i, QTableWidgetItem(stop_names[i]))
        span_width = i - current_route_index + 1
        if span_width != 1:
            self.ui.resultPanel.setSpan(0, current_route_index, 1, span_width)
            self.ui.resultPanel.setSpan(1, current_route_index, 1, span_width)
            
        self.ui.resultPanel.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

    def disableModes(self, allowedModes):
        self.ui.queryModeTramway.setDisabled(0 not in allowedModes)
        self.ui.queryModeMetro.setDisabled(1 not in allowedModes)
        self.ui.queryModeTrain.setDisabled(2 not in allowedModes)
        self.ui.queryModeBus.setDisabled(3 not in allowedModes)
        self.ui.queryModeFerry.setDisabled(4 not in allowedModes)
        self.ui.queryModeTramwayCable.setDisabled(5 not in allowedModes)
        self.ui.queryModeTelepherique.setDisabled(6 not in allowedModes)
        self.ui.queryModeFuniculaire.setDisabled(7 not in allowedModes)

    # PLOTS AND GRAPHS

    def drawStops(self, lat, lon, types):
        plt.clf()
        plt.axis('off')
        bot_left_lat = min(lat)
        bot_left_lon = min(lon)
        top_right_lat = max(lat)
        top_right_lon = max(lon)
        self.map = plt
        # self.map = Basemap(resolution='i', projection='cyl', \
        #     llcrnrlon=bot_left_lon, llcrnrlat=bot_left_lat, \
        #     urcrnrlon=top_right_lon, urcrnrlat=top_right_lat)
        # self.map.arcgisimage(service='World_Street_Map', xpixels = 1000, ypixels=1000, verbose= False)
        palette = ['#efefef', '#5289c2', '#f99625', '#f52828', 'y','b', 'r', '#000000']
        colors = [ palette[t] for t in types ]
        self.map.scatter(lon, lat, color=colors, s=2)
        self.ui.canvas.draw()

    def highlightSlectedStops(self):
        start = self.ui.queryStopEndNode.itemData(self.ui.queryStopEndNode.currentIndex())
        end = self.ui.queryStopStartNode.itemData(self.ui.queryStopStartNode.currentIndex())
        if start is not None and end is not None:
            self.controller.drawStopPath([start, end])

    def drawStopPath(self, lats, lons):
        try: self.ui.highlightPlot[0].remove()
        except: pass
        self.ui.highlightPlot = self.map.plot(lons, lats, 'o--', markersize = 4, color="black")
        self.ui.canvas.draw()
