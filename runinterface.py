import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QTableWidget, QLabel, QSizePolicy, QHeaderView, QMessageBox, QFileDialog, QTableWidgetItem, QPushButton, QHBoxLayout, QTabWidget
from backend.autocorrect import *
from gui.base_table import BaseTable
from gui.table_widget import LabeledTableWidget


class MyWindow(QMainWindow):
    def __init__(self):
            super(MyWindow, self).__init__()
            self.setGeometry(0, 0, 1920, 1000)
            self.setWindowTitle('MJHInterface')
            self.original_filepath = None   
            self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget() #create and store tab 1
        self.tab1_grid = QGridLayout()

        top_spacer = QWidget() # Add top spacer to center buttons vertically
        self.tab1_grid.addWidget(top_spacer, 0, 0, 1, 2)

        hbox1 = QHBoxLayout()

        self.Button1 = self.create_buttons('Import File', self.import_dxf_file, hbox1, "QPushButton {background-color: #0000FF; color: white;} QPushButton:hover{background-color:  #00008B;}")
        self.Button2 = self.create_buttons('Fix Errors', self.fix_errors, hbox1, "QPushButton {background-color: #0000FF; color: white;} QPushButton:hover{background-color:  #00008B;}")

        self.tab1_grid.addLayout(hbox1, 1, 0, 1, 2) # add buttons
        
        bottom_spacer = QWidget() #botton spacer 
        self.tab1_grid.addWidget(bottom_spacer, 2, 0, 1, 2)
       
        self.tab1_grid.setRowStretch(0, 1) 
        self.tab1_grid.setRowStretch(1, 0)  
        self.tab1_grid.setRowStretch(2, 1)  

        self.tab1.setLayout(self.tab1_grid)
        self.tabs.addTab(self.tab1, "Import")

    def create_buttons(self, Text, command, box: QHBoxLayout, Colour): 
        Button = QPushButton()
        Button.setText(Text)
        Button.clicked.connect(command)
        box.addWidget(Button)
        Button.setStyleSheet(Colour)
        Button.setMaximumWidth(200)
        return Button 
    
    def create_vbox(self, table, labelname):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(labelname))
        vbox.addWidget(table, 1)
        return vbox 
        
    def create_results_tab(self): 
        tab2 = QWidget()
        grid = QGridLayout()

        headers_list_table1 = ['Name', 'x', 'y', 'Angle', 'Wall', 'Type', 'On Line', 'Mistake', 'On Channel Outline']
        headers_list_table2 = ['Length', 'Slope', 'Y Intercepts']
        headers_list_table3 = ['Name', 'X Start', 'Y Start', 'X End', 'Y End', 'On Channel Outline']
        headers_list_table4 = ['X', 'Y']

        vbox1 = LabeledTableWidget('Block Reference Points', headers_list_table1, BaseTable.BLUE)
        vbox2 = LabeledTableWidget('Wall Properties', headers_list_table2, BaseTable.BLUE)
        vbox3 = LabeledTableWidget('Line Properties', headers_list_table3, BaseTable.BLUE)
        vbox4 = LabeledTableWidget('Corner Points', headers_list_table4, BaseTable.BLUE)

        self.table1 = vbox1.table  #pulling the table out of the vbox
        self.table2 = vbox2.table
        self.table3 = vbox3.table
        self.table4 = vbox4.table

        #Defining the layout
        grid.addLayout(vbox1, 0, 0, 2, 1)
        grid.addLayout(vbox4, 2, 0, 1, 1)
        grid.addLayout(vbox2, 0, 1, 1, 1)
        grid.addLayout(vbox3, 1, 1, 2, 1)

        grid.setRowStretch(0, 1)   
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        tab2.setLayout(grid)
        
        self.tabs.addTab(tab2, "Results") #add tab 2 to the widget
        
        self.populate_results_table()
        
        self.tabs.setCurrentIndex(1) # swapping to results tab

    def results_fixation(self): 
        tab3 = QWidget()
        grid = QGridLayout()

        block_ref_headers = ['Name', 'x', 'y']
        line_headers = ['Name', 'x start', 'y start', 'x end', 'y end']

        vbox1 = LabeledTableWidget('Insert Block Reference Errors Located at Points:',block_ref_headers,BaseTable.RED)
        vbox2 = LabeledTableWidget('Block Reference Errors Fixed to Points:',block_ref_headers, BaseTable.GREEN)
        vbox3 = LabeledTableWidget('Insert Line Errors Located at Points: ',line_headers, BaseTable.RED)
        vbox4 = LabeledTableWidget('Line Insert Errors fixed to Points:',line_headers, BaseTable.GREEN)

        self.table5 = vbox1.table
        self.table6 = vbox2.table
        self.table7 = vbox3.table
        self.table8 = vbox4.table

        grid.addLayout(vbox1, 0, 0, 1, 1)
        grid.addLayout(vbox2, 0, 1, 1, 1)
        grid.addLayout(vbox3, 1, 0, 1, 1)
        grid.addLayout(vbox4, 1, 1, 1, 1)

        grid.setRowStretch(0, 1)   
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        tab3.setLayout(grid)
        
        self.tabs.addTab(tab3, "Error Fixation") #Add tab2 to tab Widget
        
        self.populate_fixation() #Populate the tables 
        
        self.tabs.setCurrentIndex(2) # Switch to the Results tab

    def populate_results_table(self): 
        #populate the results table  
        self.table1.populate(self.on_line_points)
        self.table2.populate(self.wall_slope_intercept)
        self.table3.populate(self.all_lines_table)
        self.table4.populate(self.filtered_walls)            

    def populate_fixation(self): 
        #Populate the fixed tables 
        self.table5.populate(self.mistake_points)
        self.table6.populate(self.corrected_blocks)
        self.table7.populate(self.line_mistakes)
        self.table8.populate(self.fixed_lines)

    def import_dxf_file(self):
        """Opens file dialog and returns selected DXF file path"""
        filepath, _ = QFileDialog.getOpenFileName(None, "Select DXF File","", "DXF Files (*.dxf);;All Files (*)")
    
        if filepath:
            self.original_filepath = filepath

            (_, self.on_line_points, 
             self.all_lines_table, self.wall_slope_intercept, 
             self.filtered_walls, self.mistake_points, 
            self.corrected_blocks, self.line_mistakes, 
            self.fixed_lines, _, _, _, _) = autocad_points(filepath)

            self.create_results_tab()

            self.results_fixation()
            self.populate_fixation()
            QMessageBox.information(None, "Success", f"File loaded:\n{filepath}")

    def fix_errors(self):
        if not self.original_filepath: 
            QMessageBox.warning(None, "Error", "Please import a file first!")
            return
        
        output_filepath, _ = QFileDialog.getSaveFileName(
            None,
            "Save Corrected DXF File",
            self.original_filepath.replace('.dxf', '_corrected.dxf'),
            "DXF Files (*.dxf)"
        )
        
        if output_filepath:
            try:
                # NEW FUNCTION - modifies file in place
                update_dxf_in_place(self.original_filepath, output_filepath)
                QMessageBox.information(None, "Success", f"Corrections applied and saved to:\n{output_filepath}")
                
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to apply corrections:\n{str(e)}")

def window(): 
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()