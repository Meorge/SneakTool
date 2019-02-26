import os
import struct
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

class Window(QtWidgets.QMainWindow):
    """Main Window"""
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        


if __name__ == '__main__':
    global app, window
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec_())

    
