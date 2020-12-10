import sys
import time
import threading
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
mainwindow_form = uic.loadUiType("MainWindow.ui")[0]
subwindow_form = uic.loadUiType("SubWindow.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QWidget, mainwindow_form) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.createSubWindow()

        self.count = 0

        self.setWindowTitle("Yacht Dice!") # MainWindow의 타이틀 설정
        self.setWindowIcon(QIcon('dice-152179_1280.png')) # MainWindow의 아이콘 설정

        self.Monster_1 = QPixmap()
        self.Monster_1.load("monster_5.png")
        self.monsterLabel.setPixmap(self.Monster_1) # 디폴트 몬스터 Window에 표시

        self.healthpointBar.setValue(100)

        self.diceList = []  # 주사위 담을 리스트 생성 후, 주사위 객체 담기
        self.firstdice = QPixmap()
        self.seconddice = QPixmap()
        self.thirddice = QPixmap()
        self.fourthdice = QPixmap()
        self.fifthdice = QPixmap()
        self.diceList.append(self.firstdice)
        self.diceList.append(self.seconddice)
        self.diceList.append(self.thirddice)
        self.diceList.append(self.fourthdice)
        self.diceList.append(self.fifthdice)

        for i in range(5): # 주사위를 1부터 5까지 초기화
            self.diceList[i].load("dice_{}".format(i+1))
        self.firstdiceLabel.setPixmap(self.firstdice)
        self.seconddiceLabel.setPixmap(self.seconddice)
        self.thirddiceLabel.setPixmap(self.thirddice)
        self.fourthdiceLabel.setPixmap(self.fourthdice)
        self.fifthdiceLabel.setPixmap(self.fifthdice)

        self.rollButtonCount = 3 # 주사위를 ROLL 할 수 있는 횟수 제한 표시 (한턴에 3번 제한)
        self.rollButton.setText("ROLL! (3)")

        self.diceMainToSubList = []

        self.rollButton.clicked.connect(self.rollButtonClicked) # rollButton 동작 연결
        self.pushButton.clicked.connect(self.pushButtonClicked)


    # ROLL 버튼 눌렸을 때 수행할 동작
    def rollButtonClicked(self):

        if self.rollButtonCount == 1: # 주사위를 굴릴수 있는 횟수가 하나 남았을 때, 누르면 다시 세개로 초기화
            self.rollButtonCount = 4

        self.randomList = [] # 랜덤 상수 리스트 선언
        for i in range(5):
            self.randomList.append(np.random.randint(1, 7))

        self.diceMainToSubList = self.randomList # 생성자에 있는 서브윈도우로 전달할 리스트를 랜덤리스트와 동일하게 만들어줌.


        for i in range(5): # 랜덤 리스트에서 생성된 상수들로 주사위 지정
            self.diceList[i].load("dice_{}".format(self.randomList[i]))

        self.firstdiceLabel.setPixmap(self.firstdice)
        self.seconddiceLabel.setPixmap(self.seconddice)
        self.thirddiceLabel.setPixmap(self.thirddice)
        self.fourthdiceLabel.setPixmap(self.fourthdice)
        self.fifthdiceLabel.setPixmap(self.fifthdice)

        self.rollButtonCount -= 1
        self.rollButton.setText("ROLL! ({})".format(self.rollButtonCount))


    def pushButtonClicked(self):
        self.count += 1
        self.subWindow.pushButton_1.setText(str(self.count))


    def diceButtonCliked(self):
        print("clicked")

    def createSubWindow(self):
        self.subWindow = SubWindow()
        self.subWindow.show()


class SubWindow(QDialog, subwindow_form):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Yacht Dice!")


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    mainWindow = MainWindow()

    #SubWindowClass의 인스턴스 생성
    #subWindow = SubWindow()

    #프로그램 화면을 보여주는 코드
    mainWindow.show()
    #subWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
