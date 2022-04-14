from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import QtWidgets


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

    def msg(self):
        # directory1 = QFileDialog.getExistingDirectory(self,"选取文件夹","./")   #起始路径
        # print(directory1)
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取csv文件",
                                                         "./", "All Files (*);;Excel Files (*.csv)")
        return fileName
        # 设置文件扩展名过滤,注意用双分号间隔
        # print(fileName1, filetype)
        # files, ok1 = QFileDialog.getOpenFileNames(self,"多文件选择", "./", "All Files (*);;Text Files (*.txt)")
        # print(files,ok1)
        # fileName2, ok2 = QFileDialog.getSaveFileName(self,"文件保存", "./","All Files (*);;Text Files (*.txt)")
