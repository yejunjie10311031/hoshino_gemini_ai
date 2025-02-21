from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QTextBrowser, QLabel, QMessageBox, QCheckBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
import gemini
import MoeGoe
from MoeGoe import speak
import re
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
    '必须先填写google api key,没有的可以去aistudio.google.com注册账号并获取一个key。\n如果没有出现回答结果，可能key有问题或回答的内容无法通过google ai的安全审核。\n发送语句之后，会调用cpu进行处理，把回答合成语音并播放，因此等待语音的时间取决于你的cpu性能，有时候需要等很长时间。')

def tx():
    QMessageBox.information(
    window,
    '提醒',
    '未选择回答语言')

about.clicked.connect(gy)

apikey = QPlainTextEdit(window)
apikey.setPlaceholderText("请输入google api key")
apikey.move(10,5)
apikey.resize(350,30)

qd = QPushButton('确定', window)
qd.move(365,5)
qd.setEnabled(True)

key="null"
re_lan="未选择"

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

label3 = QLabel("回答语言："+re_lan, window)
label3.move(15,340)
label3.adjustSize()
label3.setStyleSheet("font-size: 18px;")
label3.resize(150,80)

label4 = QLabel("", window)
label4.move(350,495)
label4.adjustSize()
label4.setStyleSheet("font-size: 18px;")
label4.resize(250,55)

def changelan(lan, selecte, other):
    global re_lan
    re_lan = lan
    label3.setText("回答语言：" + re_lan)
    if selecte.isChecked():
        other.setChecked(False)

qc1 = QCheckBox("中文", window)
qc1.move(15,380)
qc1.adjustSize()
qc1.setStyleSheet("font-size: 20px;")
qc1.resize(85,40)

qc2 = QCheckBox("日语", window)
qc2.move(15,405)
qc2.adjustSize()
qc2.setStyleSheet("font-size: 20px;")
qc2.resize(85,40)

qc1.setChecked(False)
qc2.setChecked(False)
qc1.clicked.connect(lambda: changelan("中文", qc1, qc2))
qc2.clicked.connect(lambda: changelan("日语", qc2, qc1))

qc3 = QCheckBox("回复时不读括号内的字", window)
qc3.move(100,505)
qc3.adjustSize()
qc3.setStyleSheet("font-size: 16px;")
qc3.resize(180,35)

reply = QTextBrowser(window)
reply.setPlaceholderText("")
reply.move(10,540)
reply.resize(950,150)

fs = QPushButton('发送', window)
fs.move(870,450)
fs.setEnabled(True)

def before_send():
    global re_lan
    if re_lan=="未选择":
        tx()
    else:
        send()

def send():
    global key
    global reply
    global re_lan
    global qc3
    global label4
    global fs
    fs.setEnabled(False)
    send=talk.toPlainText()
    rep = gemini.reply(key,send)
    if qc3.isChecked():
        rep_read = re.sub(r'\([^)]*\)|（[^）]*）', '', rep, flags=re.DOTALL)
    else:
        rep_read = rep
    def speak_reply():
        if re_lan=="中文":
            speak("[ZH]"+rep_read+"[ZH]",label4,fs)
        if re_lan=="日语":
            speak("[JA]"+rep_read+"[JA]",label4,fs)
    
    thread1 = Thread(
        reply.setText(rep))
    thread1.start()
    thread3 = Thread(
        label4.setText("正在合成语音中，请等待"))
    thread2 = Thread(target=speak_reply)
    thread1.join()
    thread3.start()
    thread3.join()
    thread2.start()

fs.clicked.connect(before_send)

window.show()

app.exec()
