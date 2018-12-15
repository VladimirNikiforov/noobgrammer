import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import backend
#from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QVBoxLayout, QPushButton, QLabel, QFileDialog, QAction
#from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
#from PyQt5.QtWidgets import QInputDialog, QLineEdit
#from PyQt5.QtGui import QIcon, QPixmap
#from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):

    def __init__(self, title='PyQt5 Untitled', windowSize=(800, 600), loc=(100, 100),
                 status='This is the status bar (show cancer or not cancer)'):
        super().__init__()

        # <settings>
        self.title = title
        self.windowSize = windowSize
        self.loc = loc
        self.status = status
        # </settings>
        self.initUI()

    def initUI(self):

    # <edit>

        # <window config>
        self.setWindowTitle(self.title)
        self.setGeometry(*self.loc, *self.windowSize)
        self.statusBar().showMessage(self.status)


        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')

        openButton = QAction('Open', self)
        openButton.triggered.connect(self.open_file)
        fileMenu.addAction(openButton)

        #recButton = QAction('Recognise', self)
        #recButton.triggered.connect(self.recognise_image)
        #fileMenu.addAction(recButton)

        exitButton = QAction('Exit', self)
        exitButton.triggered.connect(self.exit_program)
        fileMenu.addAction(exitButton)

        # </window config>

    # </edit>
        self.show()

    def get_name(self):
        name, okPressed = QInputDialog.getText(self, "stupid", "Enter your name")
        return name
    # n = self.get_name()

    def open_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Image', r'C:\Users\Admin\Desktop', 'All Files (*);;JPG (*.jpg);;JPEG (*.jpeg)', options=options)
        
        self.show_image(fileName)
        result = backend.predict(fileName)

        if(result == 1):
        	self.message_box(msg = 'Cancer!!')
        elif(result == 0):
        	self.message_box(msg = 'All safe!!')
                
    # path = self.open_file()

    def show_image(self, path):
        label = QLabel(self)
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        border = 50
        label.setGeometry(border,border,pixmap.width(),pixmap.height())
        self.setGeometry(*self.loc, pixmap.width()+2*border,pixmap.height()+2*border)
        label.show()
    
    def message_box(self, title = 'Status', msg = 'default_show'):
        answer = QMessageBox.question(self, title, msg, QMessageBox.Ok)
        return answer
    # a = self.message_box()

    def exit_program(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(title="RataTapTap", windowSize=(800, 600), loc=(150, 150), status='noice')
    sys.exit(app.exec_())