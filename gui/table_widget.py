import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QTableWidget, QLabel, QSizePolicy, QHeaderView, QMessageBox, QFileDialog, QTableWidgetItem, QPushButton, QHBoxLayout, QTabWidget
from gui.base_table import BaseTable

class LabeledTableWidget(QVBoxLayout):
    def __init__(self, label_text, headers, colour):
        super().__init__()
        self.addWidget(QLabel(label_text))
        self.table = BaseTable(headers, colour)
        self.addWidget(self.table, 1)
    
    def populate(self, content):
        self.table.populate(content)