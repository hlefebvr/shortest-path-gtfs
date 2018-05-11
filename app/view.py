#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random


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
        self.dijkstra_condensed = QPushButton(
            "Algorithme de Dijkstra (Condensed Model)")
        self.bellman_condensed = QPushButton(
            "Algorithme de Bellman (Condensed Model)")
        self.bellman_expanded = QPushButton(
            "Algorithme de Bellman (Time Expanded Model)")
        self.table = QTableView()

        vertical_frame = QWidget()
        vertical_layout = QVBoxLayout()
        horizontal_frame = QWidget()
        horizontal_layout = QHBoxLayout()
        menu = QWidget()
        menu_layout = QVBoxLayout()

        figure = plt.figure()
        canvas = FigureCanvas(figure)
        plt.plot()
        plt.axis('off')
        plt.text(0, 0, "...")

        vertical_layout.addWidget(horizontal_frame)
        horizontal_layout.addWidget(canvas)
        horizontal_layout.addWidget(menu)
        menu_layout.addWidget(self.dijkstra_condensed)
        menu_layout.addWidget(self.bellman_condensed)
        menu_layout.addWidget(self.bellman_expanded)
        vertical_layout.addWidget(self.table)

        menu.setLayout(menu_layout)
        horizontal_frame.setLayout(horizontal_layout)
        vertical_frame.setLayout(vertical_layout)
        self.main_window.setCentralWidget(vertical_frame)
        self.main_window.show()

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
        plt.plot(x, y, 'o', markersize=1)

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
