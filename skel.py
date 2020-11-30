from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Yacht Dice!")
        self.setWindowIcon(QIcon('dice-152179_1280.png'))
        self.setGeometry(600, 200, 600, 700)
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())