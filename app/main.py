#!/usr/bin/python
# -*- coding: utf-8 -*-

from controller import App
import sys
from PyQt4.QtGui import QApplication

qApp = QApplication(sys.argv)
App(qApp)

qApp.exec_()
