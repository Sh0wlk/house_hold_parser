import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QComboBox, QTextEdit,
                             QScrollArea, QFrame, QMessageBox, QStackedWidget, QCheckBox, QFileDialog, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QElapsedTimer, QThread, pyqtSignal, QDateTime, QUrl
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QBrush
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

#import psycopg2
#from psycopg2.extras import RealDictCursor

def parse(city):
    

class f_home_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("f-home")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(600, 600, 45, 45)
        layout.setSpacing(16)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = f_home_window()
    controller.show()
    sys.exit(app.exec())