from PyQt5.QtWidgets import QApplication,QLabel,QPushButton
import sys,ctypes
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QScrollArea,QFrame,QMainWindow,QVBoxLayout,QLabel,QPushButton,QHBoxLayout,QWidget,QComboBox  
from qtwidgets import AnimatedToggle
from datetime import datetime
from functions import get_largest_screen
#Se le asigna un id al programa para que use el icono que le asignamos

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('ibalton.pdfSlideShow.v1') 



class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Test')
        display = get_largest_screen()

        wid = QWidget()
        self.layouts = QVBoxLayout()

        t = QLabel()
        t.setText(f"{display.name[-1:]}")
        self.layouts.addWidget(t)
        
        self.setStyleSheet("background-color: red;")
        self.setCentralWidget(wid)
        wid.setLayout(self.layouts)
        print(display.y,display.name[-1:])
     

        # Moves the Widget to the correct screen and then sets it to full screen
        self.move(display.x,display.y)
        self.showFullScreen()
        
        
    pass



app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec()


   