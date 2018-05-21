#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random


def route_type_str(i):
    return ['metro', 'train', 'bus'][int(i) - 1]


def bind_zero(n):
    return str(n) if n > 9 else '0' + str(n)


class View:
    def __init__(self,
                 controller,
                 qApp
                 ):
        self.controller = controller
        self.app = qApp
        self.main_window = QMainWindow(None)
        self.main_window.setWindowTitle(
            "TX : Exploitation de donnees pour algorithmes de graphes multimodaux")
        self.dijkstra = QPushButton("Algorithme de Dijkstra")
        self.bellman = QPushButton("Algorithme de Bellman")
        self.table = QTableWidget()
        self.metro = QCheckBox("Metro")
        self.bus = QCheckBox("Bus")
        self.train = QCheckBox("Train")
        self.metro.setCheckState(Qt.Checked)
        self.train.setCheckState(Qt.Checked)
        self.bus.setCheckState(Qt.Checked)
        self.start = QComboBox()
        self.end = QComboBox()
        self.time = QComboBox()
        self.last_plot = None
        self.exec_reports = {
            'n': QLabel(),
            'm': QLabel(),
            'max_k': QLabel(),
            'k': QLabel(),
            'state': QLabel()
        }
        t = ['None']
        for i in range(7, 22):
            for j in range(0, 60, 5):
                def bind_zero(n): return str(n) if n > 9 else '0' + str(n)
                t.append(bind_zero(i) + ':' + bind_zero(j))
        self.time.addItems(t)

        columns = ['Heure', "Nom de l\'arret", "Ligne", "Mode"]
        n_col = len(columns)
        for i in range(n_col):
            self.table.insertColumn(i)
        self.table.setHorizontalHeaderLabels(columns)
        header = self.table.horizontalHeader()

        for i in range(len(header)):
            header.setResizeMode(i, QHeaderView.ResizeToContents)

        self.vertical_frame = QWidget()
        self.vertical_layout = QVBoxLayout()
        self.horizontal_frame = QWidget()
        self.horizontal_layout = QHBoxLayout()
        self.menu = QWidget()
        self.menu_layout = QVBoxLayout()
        self.route_types_select = QWidget()
        self.route_types_layout = QHBoxLayout()
        self.stops_select = QWidget()
        self.stops_layout = QHBoxLayout()
        self.meta = QWidget()
        self.meta_layout = QHBoxLayout()

        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.meta_layout.setContentsMargins(15, 0, 0, 15)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        # plt.axis('off') # caused problems with LMDB
        # plt.text(0, 0, "...")
        # self.canvas.draw()

        self.vertical_layout.addWidget(self.horizontal_frame, 100)
        self.horizontal_layout.addWidget(self.canvas, 100)
        self.horizontal_layout.addWidget(self.menu, 50)
        self.menu_layout.addWidget(QLabel("<b>Configuration du graphe : </b>"))
        self.menu_layout.addWidget(self.route_types_select)
        self.route_types_layout.addWidget(QLabel("Modes : "))
        self.route_types_layout.addWidget(self.metro)
        self.route_types_layout.addWidget(self.bus)
        self.route_types_layout.addWidget(self.train)
        self.stops_layout.addWidget(QLabel("Depart : "))
        self.stops_layout.addWidget(self.start)
        self.stops_layout.addWidget(self.time)
        self.stops_layout.addWidget(QLabel("Arrivee : "))
        self.stops_layout.addWidget(self.end)
        self.menu_layout.addWidget(self.stops_select)
        self.menu_layout.addSpacing(50)
        self.menu_layout.addWidget(QLabel("<b>Plus court chemin :</b>"))
        self.menu_layout.addWidget(self.dijkstra)
        self.menu_layout.addWidget(self.bellman)
        self.menu_layout.addStretch(100)
        self.meta_layout.addWidget(QLabel("n ="), 5)
        self.meta_layout.addWidget(self.exec_reports['n'], 5)
        self.meta_layout.addWidget(QLabel("m ="), 5)
        self.meta_layout.addWidget(self.exec_reports['m'], 5)
        self.meta_layout.addWidget(QLabel("k ="), 5)
        self.meta_layout.addWidget(self.exec_reports['k'], 5)
        self.meta_layout.addWidget(QLabel("max k ="), 5)
        self.meta_layout.addWidget(self.exec_reports['max_k'], 5)
        self.meta_layout.addWidget(self.exec_reports['state'], 5)
        self.vertical_layout.addWidget(self.meta)
        self.vertical_layout.addWidget(self.table, 40)

        self.meta.setLayout(self.meta_layout)
        self.route_types_select.setLayout(self.route_types_layout)
        self.stops_select.setLayout(self.stops_layout)
        self.menu.setLayout(self.menu_layout)
        self.horizontal_frame.setLayout(self.horizontal_layout)
        self.vertical_frame.setLayout(self.vertical_layout)
        self.main_window.setCentralWidget(self.vertical_frame)

        menubar = self.main_window.menuBar()
        menubar.addMenu('Fichier')  # changer d'espace de travail, quitter
        menubar.addMenu('Edition')  # reinitialiser l'espace de travail
        menubar.addMenu('Aide')  # a propos, rapport TX

        for cbox in [self.bus, self.metro, self.train]:
            QObject.connect(cbox, SIGNAL(
                "stateChanged(int)"), self.refresh)
        for cbox in [self.start, self.end]:
            QObject.connect(cbox, SIGNAL(
                "currentIndexChanged(int)"), self.on_stop_selected)

        QObject.connect(self.bellman, SIGNAL("clicked()"), self.ask_bellman)

        self.main_window.show()

    def get_modes_prefix(self):
        filename = ''
        if self.metro.checkState() == 2:
            filename += '-metro'
        if self.train.checkState() == 2:
            filename += '-train'
        if self.bus.checkState() == 2:
            filename += '-bus'
        return filename

    def refresh(self):
        filename = 'stops' + self.get_modes_prefix()
        if filename == 'stops':
            plt.clf()
            plt.axis('off')
            self.canvas.draw()
            return False
        self.controller.ask_plot_xy(filename)
        self.controller.refresh_stops(filename)

    def _dialog(self, type, txt, complementaryText):
        msg = QMessageBox()
        msg.setIcon(type)
        msg.setText(txt)
        msg.setInformativeText(complementaryText)
        msg.setWindowTitle(txt)
        msg.exec_()

    def show_error(self, error, errorMsg):
        return self._dialog(QMessageBox.Critical, error, errorMsg)

    def inform(self, title, text):
        return self._dialog(QMessageBox.Information, title, text)

    def open_workspace_selector(self, workspace):
        return QFileDialog.getExistingDirectory(None, "Choisissez votre espace de travail", workspace)

    def plot_xy(self, x, y):
        plt.clf()
        plt.axis('off')
        plt.plot(x, y, 'o', markersize=1)
        self.canvas.draw()

    def ask_reduce_stops(self, lat, lon, radius):
        widget = QDialog(self.main_window)
        widget.setWindowTitle("Reduction des stops par zone geographique")
        options = QWidget()
        buttons = QWidget()
        vertical_layout = QVBoxLayout()
        options_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        lat = QLineEdit(lat)
        lon = QLineEdit(lon)
        radius = QLineEdit(radius)
        validate = QPushButton("Valider")
        refuse = QPushButton("Je ne souhaite pas reduire")

        vertical_layout.addWidget(QLabel(
            "<b>Avant d'importer le graphe, souhaitez-vous reduire le nombre de stops ?</b><br />" +
            "Nous vous proposons de ne garder que les stops se situant dans un cercle defini <br />" +
            "par son centre et son rayon : "))

        options_layout.addWidget(QLabel("Latitude : "))
        options_layout.addWidget(lat)
        options_layout.addWidget(QLabel("Longitude : "))
        options_layout.addWidget(lon)
        options_layout.addWidget(QLabel("Rayon : "))
        options_layout.addWidget(radius)

        vertical_layout.addWidget(options)
        help = QLabel("Le centre par defaut est le centre de Paris")
        help.setFont(QFont('arial', 8))
        vertical_layout.addWidget(help)

        button_layout.addWidget(validate)
        button_layout.addWidget(refuse)

        vertical_layout.addWidget(buttons)

        buttons.setLayout(button_layout)
        options.setLayout(options_layout)
        widget.setLayout(vertical_layout)
        widget.show()

        def on_validate():
            widget.close()
            _lat = float(lat.text())
            _lon = float(lon.text())
            _radius = float(radius.text())
            self.controller.build(_lat, _lon, _radius)

        def on_cancel():
            widget.close()
            self.controller.build(False, False, False)

        QObject.connect(validate, SIGNAL("clicked()"), on_validate)
        QObject.connect(refuse, SIGNAL("clicked()"), on_cancel)

    def fill_stops(self, stops):
        self.start.clear()
        self.end.clear()
        for stop in stops:
            self.start.addItem(stop['name'], userData=stop['id'])
            self.end.addItem(stop['name'], userData=stop['id'])

    def on_stop_selected(self):
        start_id = str(self.start.itemData(
            self.start.currentIndex()))
        end_id = str(self.end.itemData(
            self.end.currentIndex()))
        self.controller.highlight_stops([start_id, end_id])

    def ask_bellman(self):
        start_id = str(self.start.itemData(
            self.start.currentIndex()))
        end_id = str(self.end.itemData(
            self.end.currentIndex()))
        mode_prefix = self.get_modes_prefix()
        start_time = str(self.time.itemText(self.time.currentIndex()))
        self.controller.bellman(mode_prefix, start_id, end_id, start_time)

    def show_result(self, path):
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)
        x, y = [], []
        for i in range(len(path)):
            self.table.insertRow(i)
            time, name, route, route_type, cx, cy, = path[i]
            if time != '':
                time = int(time)
                h = int(time / 60)
                m = time % 60
                time = bind_zero(h) + ':' + bind_zero(m)
            self.table.setItem(i, 0, QTableWidgetItem(time))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(route))
            self.table.setItem(i, 3, QTableWidgetItem(
                route_type_str(route_type)))
            x.append(cx)
            y.append(cy)
        self.draw_path(x, y)

    def draw_path(self, x, y, dots=False):
        style = 'r-'
        markersize = 1
        if dots:
            style = 'ro'
            markersize = 3
        try:
            self.last_plot[0].remove()
        except:
            pass
        self.last_plot = plt.plot(x, y, style, markersize=markersize)
        self.canvas.draw()
        self.canvas.draw_idle()

    def report_exec(self, key, value):
        if key == 'state':
            value = '<b>' + str(value) + '</b>'
        self.exec_reports[key].setText(str(value))
        self.app.processEvents()
