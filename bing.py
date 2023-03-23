import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# A custom label class that shows a slideshow of images
class SlideShowLabel(QLabel):
    def __init__(self, filenames):
        super().__init__()
        self.filenames = filenames # A list of image file names
        self.index = 0 # The current index of the image to show
        self.timer = QTimer(self) # A timer to change the image periodically
        self.timer.timeout.connect(self.nextImage) # Connect the timer signal to a slot method
        self.timer.start(1000) # Start the timer with 1 second interval
        self.setPixmap(QPixmap(self.filenames[self.index])) # Set the initial pixmap

    def nextImage(self):
        # Increment the index and wrap around if it exceeds the length of the list
        self.index = (self.index + 1) % len(self.filenames)
        # Set the pixmap to the next image file name
        self.setPixmap(QPixmap(self.filenames[self.index]))

# A main widget class that contains a grid layout with slide show labels
class GridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout(self) # Create a grid layout and set it as the main layout

        # Create some sample lists of image file names for demonstration purposes
        images1 = ["images/1.jpg", "images/2.jpg", "images/3.jpg"]
        images2 = ["images/4.jpg", "images/5.jpg", "images/6.jpg"]
        images3 = ["images/7.jpg", "images/8.jpg", "images/9.jpg"]
        images4 = ["images/10.jpg", "images/11.jpg", "images/12.jpg"]

        # Create four slide show labels with different lists of images and add them to the grid layout at different positions
        self.grid_layout.addWidget(SlideShowLabel(images1), 0, 0)
        self.grid_layout.addWidget(SlideShowLabel(images2), 0, 1)
        self.grid_layout.addWidget(SlideShowLabel(images3), 1, 0)
        self.grid_layout.addWidget(SlideShowLabel(images4), 1, 1)

# A main function that creates an application and a grid widget and shows it
def main():
    app = QApplication(sys.argv)
    widget = GridWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()