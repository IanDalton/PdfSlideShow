import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel,QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,Qt
from random import randint
import sys,ctypes,os
from functions import get_largest_screen
#Se le asigna un id al programa para que use el icono que le asignamos

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('ibalton.pdfSlideShow.v1') 



class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Test')
        
        
    pass


class GridWidget(QWidget):
    def __init__(self,dim_x:int,dim_y:int,dir:str='images'):
        super().__init__()
        self.grid_layout = QGridLayout(self) # Create a grid layout and set it as the main layout
        images = generate_image_list(dim_x,dim_y,dir)
        print(images)
        # Create four slide show labels with different lists of images and add them to the grid layout at different positions
        for y,listsx in enumerate(images):
            for x,image_list in enumerate(listsx):
                print(image_list,y,x)
                self.grid_layout.addWidget(SlideShowLabel(image_list),y,x)
        display = get_largest_screen()
        self.move(display.x,display.y)
        self.showFullScreen()
        


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

def generate_image_list(x:int,y:int,dir:str)->list:
    images = list()
    for i in range(y):
            images.append([])
            for _ in range(x):
                images[i].append([])
    sort = list()
    for i in range(y):
        sort.append([])
    for i,image in enumerate(os.listdir(dir)):
        sort[i%y].append(f'{dir}/{image}')
    for yi,db in enumerate(sort):
        for i, image in enumerate(db):
              images[yi][i%x].append(image)
    return images
    
def main():
    app = QApplication(sys.argv)
    widget = GridWidget(2,1)
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
    
    
