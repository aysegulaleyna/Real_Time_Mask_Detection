from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import sys
import numpy as np
import cv2

# https://github.com/muratbahadir/Mask_Detection 
# bu linkteki gibi bağlanmalı

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # başlığı ayarla
        self.setWindowTitle("Label")
 
        # windowun geometrisini ayarlama
        self.setGeometry(0, 0, 650, 400)
        
        self.pixmap = QPixmap('d.jpg')

 
        # bir label oluşturma ve özellikleri ayarlama
        self.label_1 = QLabel(self) #sol1
        self.label_1.move(20, 100)
        self.label_1.resize(60, 60)
        self.label_1.setStyleSheet("border: 1px solid green;")
    
        # texti merkeze hizalama
        self.label_1.setAlignment(Qt.AlignCenter)
 
        # bir label oluşturma ve özellikleri ayarlama
        self.label_2 = QLabel(self) #sol2
        self.label_2.move(20, 160)
        self.label_2.resize(60, 60)
        self.label_2.setStyleSheet("border: 1px solid green;")
 
        # texti merkeze hizalama
        self.label_2.setAlignment(Qt.AlignCenter)
 
        # bir label oluşturma ve özellikleri ayarlama
        self.label_3 = QLabel(self) #sol3
        self.label_3.move(20, 220)
        self.label_3.resize(60, 60)
        self.label_3.setStyleSheet("border: 1px solid green;")
 
        # texti merkeze hizalama
        self.label_3.setAlignment(Qt.AlignCenter)
 
        # bir label oluşturma ve özellikleri ayarlama
        self.label_4 = QLabel(self) #orta
        self.label_4.move(20, 100)
        self.label_4.resize(180, 180)
        self.label_4.setStyleSheet("border: 1px solid black;")
        self.label_1.setPixmap(self.pixmap)
        # texti merkeze hizalama
        self.label_4.setAlignment(Qt.AlignCenter)
 
        # bir label oluşturma ve özellikleri ayarlama
        self.label_5 = QLabel(self) #sag1
        self.label_5.move(200, 100)
        self.label_5.resize(60, 60)
        self.label_5.setStyleSheet("border: 1px solid red;")
 
        # texti merkeze hizalama
        self.label_5.setAlignment(Qt.AlignCenter)
 
        # bir label oluşturma ve özellikleri ayarlama
        self.label_6 = QLabel(self)#sag2
        self.label_6.move(200, 160)
        self.label_6.resize(60, 60)
        self.label_6.setStyleSheet("border: 1px solid red;")
 
        # texti merkeze hizalama
        self.label_6.setAlignment(Qt.AlignCenter)
 
        # bir label oluşturma ve özellikleri ayarlama
        self.label_7 = QLabel(self)#sag3
        self.label_7.move(200, 220)
        self.label_7.resize(60, 60)
        self.label_7.setStyleSheet("border: 1px solid red;")
 
        # texti merkeze hizalama
        self.label_7.setAlignment(Qt.AlignCenter)
 
        # tüm widget'ları göster
        self.show()
 
 

if __name__ == '__main__':
    # pyqt5 app i oluştur
    App = QApplication(sys.argv)
 
    # window u oluştur
    window = Window()
 
    # app start
    sys.exit(App.exec()) #pencere kapanana kadar çalıştır