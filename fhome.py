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

import webbrowser
import requests
import nodriver as nd
import asyncio as asy
import os
from re import finditer
import shutil

cost_pat = ""
link_pat = ""

class f_home_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("f-home")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(600, 600, 45, 45)
        layout.setSpacing(16)
    
    def goToPage(url):
        webbrowser.open_new_tab(url)
    
    async def parse(city):
        live_user_data = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
        bot_user_data = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data Bot')
        
        try:
            os.makedirs(os.path.join(bot_user_data, "Default"), exist_ok=True)
            files_to_copy = ['Network', 'Cookies', 'Login Data', 'Local Storage', 'Secure Preferences']
            live_default_path = os.path.join(live_user_data, "Default")
            bot_default_path = os.path.join(bot_user_data, "Default")

            for item in os.listdir(live_default_path):
                if item in files_to_copy or "Preferences" in item:
                    src = os.path.join(live_default_path, item)
                    dst = os.path.join(bot_default_path, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copyfile(src, dst)
            print("Profile successfully cloned!")
        except Exception as e:
            print(f"Note: Some profile files were locked, skipping them: {e}")
            
        browser = await nd.start(
            user_data_dir = bot_user_data,
            headless = False,
            sandbox = False
        )
        
        page = await browser.get(url.string)
        await page.sleep(1)
        htmll = await page.get_content()
        m = []
        z = 0
        for i in finditer(cost_pat,htmll):
            m.append([i.group()])
        for i in finditer(link_pat,htmll):
            m[z].append([i.group()])
            z+=1
        arr(m)
        browser.stop()
    
    #def arr(args):

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = f_home_window()
    controller.show()
    sys.exit(app.exec())