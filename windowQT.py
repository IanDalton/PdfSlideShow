import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel,QMainWindow,QFileDialog
from PyQt5.QtGui import QPixmap,QIntValidator,QDragEnterEvent,QDropEvent
from PyQt5.QtCore import QTimer,Qt,QMimeData
from random import randint
from PyQt5 import QtWidgets
import sys,ctypes,os
from functions import get_largest_screen,extract_images,generate_image_list

#Se le asigna un id al programa para que use el icono que le asignamos

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('ibalton.pdfSlideShow.v1') 



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.widget = GridWidget(2,1)
        #self.widget.show()

    def init_ui(self):
        self.row_label = QtWidgets.QLabel('Rows:')
        self.row_input = QtWidgets.QLineEdit()
        self.row_input.setText('3')
        self.row_input.setValidator(QIntValidator())
        self.column_label = QtWidgets.QLabel('Columns:')
        self.column_input = QtWidgets.QLineEdit()
        self.column_input.setText('4')
        self.column_input.setValidator(QIntValidator())
        self.file_label = QtWidgets.QLabel('')
        self.upload_button = QtWidgets.QPushButton('Upload File')
        self.generate_slideshow = QtWidgets.QPushButton('Enabledsss Button')
        self.generate_slideshow.setEnabled(False)

        wid = QWidget()
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.row_label)
        v_box.addWidget(self.row_input)
        v_box.addWidget(self.column_label)
        v_box.addWidget(self.column_input)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.upload_button)
        h_box.addWidget(self.file_label)

        v_box.addLayout(h_box)
        v_box.addWidget(self.generate_slideshow)

        wid.setLayout(v_box)
        self.setCentralWidget(wid)
        self.setWindowTitle('PyQt5 Window')

        self.upload_button.clicked.connect(self.upload_file)
        self.generate_slideshow.clicked.connect(self.generate_grid_widget)
        print(self.setAcceptDrops(True))

        

    def upload_file(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='PDF Files (*.pdf)', options=QFileDialog.DontUseNativeDialog)
        if self.file_name:
            print(f'File uploaded: {self.file_name}')
            self.generate_slideshow.setEnabled(True)
            self.file_label.setText(self.file_name)
        

    def dragEnterEvent(self, e):
        print("dragEnterEvent")
        if e.mimeData().hasUrls():
            e.accept()
            print("Accepted")
            
        else:
            e.ignore()
            print("Ignored")

    def dropEvent(self, e):
        print("dropEvent")
        for url in e.mimeData().urls():
            self.file_name = str(url.toLocalFile())
            self.file_label.setText(self.file_name)
        if self.file_name:
            self.generate_slideshow.setEnabled(True)
        


      
    
    def generate_grid_widget(self):
        
        self.grid_widget =GridWidget(dim_x=int(self.column_input.text()),dim_y=int(self.row_input.text()),pdf_dir=self.file_name) 
        self.grid_widget.showFullScreen()
        self.hide()

    


class GridWidget(QWidget):
    def __init__(self,dim_x:int,dim_y:int,dir:str='images',pdf_dir:str='pdf.pdf'):
        super().__init__()

        extract_images(pdf_dir) #Extracting all images from pdf

        self.grid_layout = QGridLayout(self) # Create a grid layout and set it as the main layout
        images = generate_image_list(dim_x,dim_y,dir)
        #print(images)
        # Create four slide show labels with different lists of images and add them to the grid layout at different positions
        for y,listsx in enumerate(images):
            for x,image_list in enumerate(listsx):
                print(image_list,y,x)
                self.grid_layout.addWidget(SlideShowLabel(image_list),y,x)
        display = get_largest_screen()
        self.move(display.x,display.y)
        #self.showFullScreen()
        


# A custom label class that shows a slideshow of images
class SlideShowLabel(QLabel):
    def __init__(self, filenames):
        super().__init__()
        self.filenames = filenames # A list of image file names
        self.index = 0 # The current index of the image to show
        self.timer = QTimer(self) # A timer to change the image periodically
        self.timer.timeout.connect(self.nextImage) # Connect the timer signal to a slot method
        self.timer.start(5000) # Start the timer with 5 second interval
        self.setPixmap(QPixmap(self.filenames[self.index])) # Set the initial pixmap
        self.setAlignment(Qt.AlignCenter)

    def nextImage(self):
        # Increment the index and wrap around if it exceeds the length of the list
        self.index = (self.index + 1) % len(self.filenames)
        # Set the pixmap to the next image file name

        self.setPixmap(QPixmap(self.filenames[self.index]))
        self.setPixmap(QPixmap(self.filenames[self.index]).scaled(self.size(), Qt.KeepAspectRatio))
    def resizeEvent(self, event):
        # Get the current size of the label
        size = self.size()
        # Scale and set a new pixmap according to that size and keep aspect ratio
        self.setPixmap(QPixmap(self.filenames[self.index]).scaled(size, Qt.KeepAspectRatio))

    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
    
    
