import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QComboBox, QTextEdit,
                             QScrollArea, QFrame, QMessageBox, QStackedWidget, QCheckBox, QFileDialog, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QElapsedTimer, QThread, pyqtSignal, QDateTime, QUrl
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QBrush
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import webbrowser
import nodriver as nd
import asyncio as asy
import os
from re import finditer
import shutil
from qasync import QEventLoop, asyncSlot 

import psycopg

DB = {
    "dbname": "my_local_db",
    "user": "postgres",
    "password": "Sakuromoti3!",
    "host": "127.0.0.1",
    "port": "5432"
}
def default_data():
    try:
        conn = psycopg.connect(**DB)
        with conn.cursor() as cursor:
            cursor.execute("""
                DROP TABLE IF EXISTS offers;
                CREATE TABLE IF NOT EXISTS offers (
                    id SERIAL PRIMARY KEY,
                    price INT,
                    link VARCHAR(512)
                )
                """)
            conn.commit()
        conn.close()
    except Exception as e:
        print("Sinisterrr in DB) ", e)

class f_home_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("f-home")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(600, 600, 45, 45)
        layout.setSpacing(16)
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("город")
        self.city_input.setMinimumHeight(40)
        layout.addWidget(self.city_input)
        
        check_city_btn = QPushButton("Посмотреть цены")
        check_city_btn.setObjectName("cityCheck")
        check_city_btn.setMinimumHeight(40)
        check_city_btn.clicked.connect(self.parse)
        layout.addWidget(check_city_btn)

    def goToPage(self, url):
        webbrowser.open_new_tab(url)
    
    def debugFunc(self,d1,d2):
        print("price) ", d1)
        print("///")
        print("link) ", d2)
        print("///")
        
    @asyncSlot()
    async def parse(self):
        city_to_search = self.city_input.text().strip()
        
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
            sandbox = False,
            no_sandbox = True)
        
        url = f"https://www.avito.ru/moskva?localPriority=0&q=cъем+{city_to_search}"
        
        page = await browser.get(url)
        await page.sleep(10)
        htmll = await page.get_content()
        m = []
        price_cm = ['><span data-marker="item-price-value"', '>', '<#comment']
        link_cm = ['a class="sliderLink-',"href=", '?']
        try:
            s = 0
            items = await page.select_all('div[data-marker="item"]')
            c=0
            for item in items:
                item = str(item).encode('utf-8', errors='ignore').decode('utf-8')
                
                price = item[item.find(price_cm[0])+1: len(item)]; price = price[price.find(price_cm[1])+len(price_cm[1]): price.find(price_cm[2])]
                link = item[item.find(link_cm[0]): len(item)]; link = link[link.find(link_cm[1])+len(link_cm[1])+1: link.find(link_cm[2])]
                if len(price)<15 and "от" not in price:
                    price = int("".join(price.split()))
                    c +=1
                    s += price
                    #DEBUG FUNC
                    #self.debugFunc(price,link)

                    self.arr([c,price,link])
            s//=c
            self.analyze(s)
            
        except Exception as e:
            print(f"sinisterrrrr on html fuck: {e} and the er itself {link, price}")
        await browser.stop()
    
    def analyze(self,s):
        with psycopg.connect(**DB) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""SELECT price, link, {s} FROM offers WHERE price <= {s}/100*80"""
                )
                print(cursor.fetchall())
    
    def arr(self, args):
        with psycopg.connect(**DB) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO offers (id, price, link) VALUES (%s, %s, %s);""",(args[0],args[1],args[2])
                )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    default_data()
    
    loop = QEventLoop(app)
    asy.set_event_loop(loop)
    controller = f_home_window()
    
    controller.show()
    with loop:
        loop.run_forever()