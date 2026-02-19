import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QTableWidget, QLabel, QSizePolicy, QHeaderView, QMessageBox, QFileDialog, QTableWidgetItem, QPushButton, QHBoxLayout, QTabWidget


class BaseTable(QTableWidget):
    BLUE = '#0000FF'
    RED = '#FF0000'
    GREEN = '#006400'

    def __init__(self, headers, colour):
        super().__init__()
        self.setRowCount(0)
        self.setColumnCount(len(headers))
        self.setVerticalHeaderLabels([str(i + 1) for i in range(1000)])
        self.setHorizontalHeaderLabels(headers)  
        self.colour_headers(colour)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def colour_headers(self, colour): 
        self.horizontalHeader().setStyleSheet(f"QHeaderView::section {{background-color: {colour}; color: white; font-weight: bold; }}")
        self.verticalHeader().setStyleSheet(f"QHeaderView::section {{ background-color: {colour}; color: white;font-weight: bold; }}")

    def populate(self, content):
        self.setRowCount(len(content))
        for row, row_data in enumerate(content): #for row in all the data number the rows 
            for col, value in enumerate(row_data): #take each row and match it witha column 
                self.setItem(row, col, QTableWidgetItem(str(value)))


    #     self.headers = headers

    #     self.setMaximumWidth = MAX_WIDTH

    # def change_header_name(self, idx, new_name):
    #     self.headers[idx] = new_name