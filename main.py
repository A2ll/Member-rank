import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from loguru import logger

from UI import Ui_Form
from csv_pretreatment import DataPre
from open_file import MyWindow
from query_Thread import WorkThread

import openpyxl


class MainForm(Ui_Form):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.obj = None
        self.WorkThread = None
        logger.add('event.log')

    def setupUi(self, MainForm):
        super().setupUi(MainForm)
        self.pushButton.clicked.connect(self.main)
        self.toolButton.clicked.connect(self.set)

    def main(self):
        if self.radioButton_1.isChecked() and self.obj is not None:
            self.obj.start()
        elif self.radioButton_2.isChecked() and self.obj is not None:
            key_id = self.lineEdit_3.text()
            if key_id != '':
                self.WorkThread = WorkThread()
                self.WorkThread.trigger.connect(self.print_return)
                self.WorkThread.set(key_id, self.file_path, self.lineEdit.text(), self.lineEdit_2.text())
                self.WorkThread.start()
            else:
                self.textBrowser.append('输入关键人物id')

        elif self.obj is None:
            self.textBrowser.append('选择需要分析的文件')
        else:
            self.textBrowser.append('选择需要的功能')

    def set(self):
        a = MyWindow()
        key_id = self.lineEdit.text()
        sid = self.lineEdit_2.text()
        if key_id != '' and sid != '':
            self.file_path = a.msg()
            self.textBrowser_2.clear()
            self.textBrowser_2.append(str(self.file_path))
            self.obj = DataPre(self.file_path, key_id, sid)
            self.obj.trigger.connect(self.print_return)
        else:
            self.textBrowser.append('输入用户id字段名和推荐id字段名')

    def print_return(self, pr):
        self.textBrowser.append(pr)


if __name__ == '__main__':
    # 创建一个App实例
    app = QApplication(sys.argv)
    # 创建一个主窗口
    mainWin = QMainWindow()
    # 使用我们生成的UI窗口实例
    ui = MainForm()
    # 将主窗口传递进去，让Ui_MainWindow帮我们向主窗口上放置组件
    ui.setupUi(mainWin)
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())
