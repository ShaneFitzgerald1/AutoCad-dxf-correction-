import sys
from PyQt5.QtWidgets import QApplication
from gui.runinterface import MyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())



    # pyinstaller --onefile --windowed --add-data "objectdatabase.db;." --hidden-import=ezdxf --hidden-import=sqlalchemy --hidden-import=sqlalchemy.dialects.sqlite --exclude-module PySide6 --exclude-module PyQt6 main.py