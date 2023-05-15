from PyQt5.QtWidgets import (QApplication, QWidget,
                              QGridLayout, QLabel,
                              QMainWindow,QFileDialog,
                              QStackedWidget,QHBoxLayout,
                              QGraphicsOpacityEffect,QSizePolicy)
from PyQt5.QtGui import QPixmap,QIntValidator, QFont
from PyQt5.QtCore import QTimer,Qt,QUrl,QPropertyAnimation,QPoint
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer

from PyQt5 import QtWidgets
import json

import sys,ctypes,os
from files.functions import get_largest_screen,extract_images,generate_image_list,del_images,check_new_packages

#Se le asigna un id al programa para que use el icono que le asignamos

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('ibalton.pdfSlideShow.v1') 



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        dpi = self.screen().physicalDotsPerInch()
        font = QFont()
        font.setPointSizeF(12*dpi/72)

        self.row_label = QtWidgets.QLabel('Filas:')
        self.row_input = QtWidgets.QLineEdit()
        self.row_label.setFont(font)
        self.row_input.setText('3')
        self.row_input.setFont(font)
        self.row_input.setValidator(QIntValidator())
        self.column_label = QtWidgets.QLabel('Columnas:')
        self.column_label.setFont(font)
        self.column_input = QtWidgets.QLineEdit()
        self.column_input.setFont(font)
        self.column_input.setText('4')
        self.column_input.setValidator(QIntValidator())
        self.file_label = QtWidgets.QLabel('')
        self.file_label.setFont(font) 
        self.upload_button = QtWidgets.QPushButton('Subir PDF')
        self.upload_button.setFont(font)
        self.generate_slideshow = QtWidgets.QPushButton('Crear Video')
        self.generate_slideshow.setFont(font)
        self.generate_slideshow.setEnabled(False)
        self.video_folder_label = QtWidgets.QLabel('')
        self.video_folder_label.setFont(font)
        self.select_folder_button = QtWidgets.QPushButton('Seleccionar carpeta de videos')
        self.select_folder_button.setFont(font)


        # Create a label, slider, and line edit for controlling the duration
        duration_box = QHBoxLayout()
        self.duration_label = QtWidgets.QLabel('Duración:')
        self.duration_label.setFont(font)
        self.duration_slider = QtWidgets.QSlider(Qt.Horizontal)
        duration_units = QtWidgets.QLabel('s')
        self.duration_slider.setRange(1, 60)
        self.duration_slider.setValue(5)
        self.duration_input = QtWidgets.QLineEdit()
        self.duration_input.setFont(font)
        self.duration_input.setText('15')
        self.duration_input.setValidator(QIntValidator())

        # Connect the slider and line edit signals to update each other
        self.duration_slider.valueChanged.connect(lambda value: self.duration_input.setText(str(value)))
        self.duration_input.textChanged.connect(lambda text: self.duration_slider.setValue(int(text)))

        wid = QWidget()
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.row_label)
        v_box.addWidget(self.row_input)
        v_box.addWidget(self.column_label)
        v_box.addWidget(self.column_input)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.upload_button)
        h_box.addWidget(self.file_label)

        v_folder_box = QHBoxLayout()
        v_folder_box.addWidget(self.select_folder_button)
        v_folder_box.addWidget(self.video_folder_label)

        # Add the duration widgets to the layout
        
        duration_box.addWidget(self.duration_label)
        duration_box.addWidget(self.duration_input)
        duration_box.addWidget(duration_units)
        
        v_box.addLayout(duration_box)
        v_box.addWidget(self.duration_slider)
        

        v_box.addLayout(h_box)
        v_box.addLayout(v_folder_box)
        v_box.addWidget(self.generate_slideshow)

        wid.setLayout(v_box)
        self.setCentralWidget(wid)
        self.setWindowTitle('PyQt5 Window')

        self.upload_button.clicked.connect(self.upload_file)
        self.select_folder_button.clicked.connect(self.select_folder)
        self.generate_slideshow.clicked.connect(self.generate_grid_widget)
        self.setAcceptDrops(True)
        self.folder_name = None
        self.file_name = None
        moverbtn = QtWidgets.QPushButton()
        moverbtn.setText('MOVER')
        moverbtn.clicked.connect(self.mover)
        #v_box.addWidget(moverbtn)
        

        
    def mover(self):
        s = get_largest_screen()
        self.move(s.x,s.y)
    def select_folder(self):
        self.folder_name = QFileDialog.getExistingDirectory(self , options=QFileDialog.DontUseNativeDialog)
        if self.folder_name:
            print(f'File uploaded: {self.folder_name}')
            self.video_folder_label.setText(self.folder_name)
    def upload_file(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Seleccionar PDF', filter='PDF Files (*.pdf)', options=QFileDialog.DontUseNativeDialog)
        if self.file_name:
            print(f'File uploaded: {self.file_name}')
            self.generate_slideshow.setEnabled(True)
            self.file_label.setText(self.file_name)
        

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()


    def dropEvent(self, e):

        for url in e.mimeData().urls():
            self.file_name = str(url.toLocalFile())
            self.file_label.setText(self.file_name)
        if self.file_name:
            self.generate_slideshow.setEnabled(True)
        
    
    def generate_grid_widget(self):
        
        self.grid_widget =GridWidget(dim_x=int(self.column_input.text()),dim_y=int(self.row_input.text()),pdf_dir=self.file_name,duration=self.duration_slider.value(),videos=self.folder_name) 
        
        self.hide()
    
    def save(self):
        with open('.\\files\\data.json','w') as file:
            json.dump({
                'row':self.row_input.text(),
                'column':self.column_input.text(),
                'pdf':self.file_name,
                'videos':self.folder_name,
                'seconds':self.duration_input.text()
            },file)
    def load(self):
        try:
            with open('.\\files\\data.json','r') as file:
                data = json.load(file)
                self.row_input.setText(data['row'])
                self.column_input.setText(data['column'])
                self.duration_input.setText(data['seconds'])
                self.file_name = data['pdf']
                self.folder_name = data['videos']

                #Change the text so the selected folder appears in the UI
                self.file_label.setText(self.file_name)
                self.video_folder_label.setText(self.folder_name)

                #Change the slider value
                self.duration_slider.setValue(int(self.duration_input.text()))
                
                #Enable the button
                self.generate_slideshow.setEnabled(True)
        except:
            pass
    


class GridWidget(QWidget):
    def __init__(self,dim_x:int,dim_y:int,dir:str='images',pdf_dir:str='pdf.pdf',duration:int=10,videos:str=None):
        super().__init__()
        pdf = None
        try:
            with open('.\\files\\data.json','r') as file:
                datos = json.load(file)
                pdf = datos["pdf"]
        except:
            pass
        if pdf_dir != pdf or not os.path.exists('images'):
            print('Generando imagenes')
            del_images()
            extract_images(pdf_dir) #Extracting all images from pdf
        
        self.grid_layout = QGridLayout(self) # Create a grid layout and set it as the main layout
        images = generate_image_list(dim_x,dim_y,dir,videos)
        # Create four slide show labels with different lists of images and add them to the grid layout at different positions
        prev_label:SlideShowLabel = None
        i=0

        display = get_largest_screen()
        print(display)
        
        self.move(QPoint(display.x,display.y))
        self.show()
        
        self.showFullScreen()
        for y,listsx in enumerate(images):
            for x,image_list in enumerate(listsx):
                #print(image_list,y,x)
                label = SlideShowLabel(image_list,duration,i)
                self.grid_layout.addWidget(label,y,x)
                if prev_label:
                    prev_label.get_next(label)
                prev_label = label
                i+=1
                
        
        
        


# A custom label class that shows a slideshow of images

class SlideShowLabel(QStackedWidget):
    def __init__(self, filenames,duration,index):
        super().__init__()
        
        self.us_index = index
        self.filenames = filenames
        self.index = 0
        self.default_duration = duration*1000
        self.setStyleSheet('background-color:white;')
        # Pre-load and pre-scale all the images
        self.pixmaps = []
        self.filenames = filenames
        for filename in filenames:
            if not filename.endswith(('.mp4', '.avi', '.mov')):
                pixmap = QPixmap(filename).scaled(self.size(), Qt.KeepAspectRatio,Qt.SmoothTransformation)
                self.pixmaps.append(pixmap)
            else:
                self.pixmaps.append(None)
        # Create a QLabel to display images
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.addWidget(self.imageLabel)
        

        # Create a QGraphicsOpacityEffect to control the opacity of the image label
        self.imageOpacityEffect = QGraphicsOpacityEffect(self.imageLabel)
        self.imageLabel.setGraphicsEffect(self.imageOpacityEffect)

        # Create a QPropertyAnimation to animate the opacity of the image label
        self.imageOpacityAnimation = QPropertyAnimation(self.imageOpacityEffect, b'opacity')
        self.imageOpacityAnimation.setDuration(1000)
        self.imageOpacityAnimation.setStartValue(0.0)
        self.imageOpacityAnimation.setEndValue(1.0)


        # Create a QVideoWidget to display videos
        self.videoWidget = QVideoWidget()
        
        self.addWidget(self.videoWidget)

        # Create a QGraphicsOpacityEffect to control the opacity of the video widget
        self.videoOpacityEffect = QGraphicsOpacityEffect(self.videoWidget)
        self.videoWidget.setGraphicsEffect(self.videoOpacityEffect)

        # Create a QPropertyAnimation to animate the opacity of the video widget
        self.videoOpacityAnimation = QPropertyAnimation(self.videoOpacityEffect, b'opacity')
        self.videoOpacityAnimation.setDuration(1000)
        self.videoOpacityAnimation.setStartValue(0.0)
        self.videoOpacityAnimation.setEndValue(1.0)


        # Create a QMediaPlayer to control video playback
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Create a QTimer to change the media periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextMedia)
        self.timer.start(self.default_duration)

        # Set the initial media
        self.setMedia(self.filenames[self.index])
        self.lastSize = self.size()
        self.next_label = None
    def get_next(self,label):
        self.next_label:SlideShowLabel = label
        self.next_label.timer.stop()

    def setMedia(self, filename):
        if filename.endswith(('.mp4', '.avi', '.mov')):
            # If the file is a video, set the media source and play it
            
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

            self.mediaPlayer.setVolume(0)
            self.mediaPlayer.play()
            # Show the video widget and hide the image label
            self.setCurrentWidget(self.videoWidget)
            # Start the video opacity animation
            self.videoOpacityAnimation.start()
            # Reset the image opacity for next time it is shown
            self.imageOpacityEffect.setOpacity(0.0)

        else:
            # If the file is an image, use the pre-scaled pixmap and show it
            pixmap = self.pixmaps[self.index]
            self.imageLabel.setPixmap(pixmap)


            # Show the image label and hide the video widget
            self.setCurrentWidget(self.imageLabel)
            # Start the image opacity animation
            self.imageOpacityAnimation.start()
            # Reset the video opacity for next time it is shown
            self.videoOpacityEffect.setOpacity(0.0)

    def nextMedia(self):
        def change_media():
            # Increment the index and wrap around if it exceeds the length of the list
            self.index = (self.index + 1) % len(self.filenames)
            # Set the media to the next file name
            self.setMedia(self.filenames[self.index])
        
        print(f'{self.us_index}: ',end='')
        # Check if a video is playing, if it isn't go to the next file
        if self.mediaPlayer.state() != QMediaPlayer.PlayingState:
            change_media()
        
        print(self.filenames[self.index])
        # wait a second, then go to the next one
        if self.next_label:
            print(f'{self.us_index} --> ',end='')
            QTimer.singleShot(1000,lambda:self.next_label.nextMedia())
            

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Get the current size of the widget
        size = self.size()
        # Scale and set a new pixmap according to that size and keep aspect ratio
        if abs(size.width() - self.lastSize.width()) > 10 or abs(size.height() - self.lastSize.height()) > 10:
        # Scale and set a new pixmap according to that size and keep aspect ratio
            self.pixmaps = list()
            for filename in self.filenames:
                if not filename.endswith(('.mp4', '.avi', '.mov')):
                    pixmap = QPixmap(filename).scaled(self.size(), Qt.KeepAspectRatio,Qt.SmoothTransformation)
                    self.pixmaps.append(pixmap)
                else:
                    self.pixmaps.append(None)
                # Update the last size
            self.lastSize = size
    
def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.load()
    window.show()
    while app.exec_():
        pass
    window.save()
    sys.exit()
    
    


if __name__ == "__main__":
    main()
    
    
    
