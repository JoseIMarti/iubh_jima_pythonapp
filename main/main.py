'''
Created on Dec 6, 2020

@author: jima
'''
import sys
from helpers.forms import *
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
