from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QTextBrowser, QLabel, QMessageBox 
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
import gemini
import MoeGoe
from MoeGoe import speak
import time
from threading import Thread
from threading import Timer

app = QApplication([])

window = QMainWindow()
window.resize(1000, 700)
window.move(200, 100)
window.setWindowTitle("hoshino-gemini-ai")

l1=QLabel(window)
p1 = QPixmap("main.png")
l1.setPixmap(p1)
l1.resize(1000,650)
l1.move(15,0)

l2=QLabel(window)
p2 = QPixmap("hoshino.png")
l2.setPixmap(p2)
l2.setScaledContents(True)
l2.adjustSize()
l2.resize(p2.width()*0.6,p2.height()*0.6)
l2.move(250,-40)

about = QPushButton('关于', window)
about.move(900,5)
about.setEnabled(True)

def gy():
    QMessageBox.information(
    window,
    '关于',
    '必须先填写google api key,没有的可以去ai.google.dev注册账号并获取一个key。\n如果没有出现回答结果，可能key有问题或回答的内容无法通过google ai的安全审核。\n发送语句之后，会调用cpu进行处理，把回答合成语音并播放，因此等待语音的时间取决于你的cpu性能，有时候需要等很长时间。')

about.clicked.connect(gy)

apikey = QPlainTextEdit(window)
apikey.setPlaceholderText("请输入google api key")
apikey.move(10,5)
apikey.resize(350,30)

qd = QPushButton('确定', window)
qd.move(365,5)
qd.setEnabled(True)

key="null"

label1 = QLabel("当前密钥："+key, window)
label1.move(470,10)
label1.adjustSize()
label1.resize(400,20)

def getkey():
    global key
    global label1
    key = apikey.toPlainText()
    label1.setText("当前密钥："+key)
    gemini.start(key)

qd.clicked.connect(getkey)

talk = QPlainTextEdit(window)
talk.setPlaceholderText("请输入:")
talk.move(10,450)
talk.resize(850,60)

label2 = QLabel("回答：", window)
label2.move(10,510)
label2.setStyleSheet("font-size: 24px;")

reply = QTextBrowser(window)
reply.setPlaceholderText("")
reply.move(10,540)
reply.resize(950,150)

fs = QPushButton('发送', window)
fs.move(870,450)
fs.setEnabled(True)

def send():
    global reply
    send=talk.toPlainText()
    re = gemini.reply(send)  
    
    def speak_reply():
        speak(re)
    
    thread1 = Thread(
    reply.setText(re))
    thread1.start()
    thread2 = Thread(target=speak_reply)
    thread1.join()
    thread2.start()

fs.clicked.connect(send)

window.show()

app.exec()