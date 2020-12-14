import sys
import time
import threading
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *

import ScoreFunction

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
mainwindow_form = uic.loadUiType("MainWindow.ui")[0]
subwindow_form = uic.loadUiType("SubWindow.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QWidget, mainwindow_form) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.createSubWindow() # subwindow 서브 윈도우 생성

        self.diceMainToSubList = [] # 메인 윈도우에서 가진 주사위 배열을 서브 윈도우에서 활용할 임시 리스트

        self.setWindowTitle("Yacht Dice!") # MainWindow의 타이틀 설정
        self.setWindowIcon(QIcon('dice-152179_1280.png')) # MainWindow의 아이콘 설정

        # 몬스터의 QPixmap 객체와 healthpoint를 담을 리스트 생성

        self.monstercount = 0

        self.monsterList = []

        self.Monster_1 = QPixmap()
        self.monster_1_healthpoint = 100

        self.Monster_2 = QPixmap()
        self.monster_2_healthpoint = 120

        self.Monster_3 = QPixmap()
        self.monster_3_healthpoint = 140

        self.Monster_4 = QPixmap()
        self.monster_4_healthpoint = 160

        self.Monster_5 = QPixmap()
        self.monster_5_healthpoint = 180

        self.Monster_6 = QPixmap()
        self.monster_6_healthpoint = 200

        self.monsterList.append([self.Monster_1, self.monster_1_healthpoint])
        self.monsterList.append([self.Monster_2, self.monster_2_healthpoint])
        self.monsterList.append([self.Monster_3, self.monster_3_healthpoint])
        self.monsterList.append([self.Monster_4, self.monster_4_healthpoint])
        self.monsterList.append([self.Monster_5, self.monster_5_healthpoint])
        self.monsterList.append([self.Monster_6, self.monster_6_healthpoint])

        self.totalDamage = self.subWindow.total

        self.randomList = [1, 1, 1, 1, 1]

        self.maintextBrowser.setFontPointSize(10)

        # 주사위 담을 리스트 생성 후, 주사위 객체 담기
        self.diceList = []
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

        # 시작 화면에서 주사위를 1부터 5까지 초기화
        for i in range(5):
            self.diceList[i].load("dice_{}".format(i+1))

        self.firstdiceLabel.setPixmap(self.firstdice)
        self.seconddiceLabel.setPixmap(self.seconddice)
        self.thirddiceLabel.setPixmap(self.thirddice)
        self.fourthdiceLabel.setPixmap(self.fourthdice)
        self.fifthdiceLabel.setPixmap(self.fifthdice)

        self.diceButtonList = []
        self.diceButtonList.append(self.firstdiceButton)
        self.diceButtonList.append(self.seconddiceButton)
        self.diceButtonList.append(self.thirddiceButton)
        self.diceButtonList.append(self.fourthdiceButton)
        self.diceButtonList.append(self.fifthdiceButton)

        self.rollButtonCount = 3 # 주사위를 ROLL 할 수 있는 횟수 제한 표시 (한턴에 3번 제한)
        self.rollButton.setText("ROLL! (3)")

        # 백그라운드 동작 연결
        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.createMonster)
        self.timer.start()

        #즉사버튼 연결
        self.killButton.clicked.connect(self.killButtonClicked)

        # rollButton 동작 연결
        self.rollButton.clicked.connect(self.rollButtonClicked)

        # 주사위 고정 버튼 동작 연결
        self.firstdiceButton.clicked.connect(self.diceButtonClicked)
        self.seconddiceButton.clicked.connect(self.diceButtonClicked)
        self.thirddiceButton.clicked.connect(self.diceButtonClicked)
        self.fourthdiceButton.clicked.connect(self.diceButtonClicked)
        self.fifthdiceButton.clicked.connect(self.diceButtonClicked)

        # 플레이 버튼 동작 연결
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.playButtonClicked)

    # ROLL 버튼 눌렸을 때 수행할 동작
    def rollButtonClicked(self):
        if self.subWindow.rollButtonCount == 1: # 주사위를 굴릴수 있는 횟수가 하나 남았을 때, 누르면 다시 누르지 못하는 상태로 변환
            self.rollButton.setEnabled(False)

        # 랜덤 상수 리스트 선언
        for i in range(5):
            if self.diceButtonList[i].text() == "Fix!":
                self.randomList[i] = np.random.randint(1, 7)
            else: continue

        # 랜덤 리스트에서 생성된 상수들로 주사위 지정
        for i in range(5):
                self.diceList[i].load("dice_{}".format(self.randomList[i]))

        self.firstdiceLabel.setPixmap(self.firstdice)
        self.seconddiceLabel.setPixmap(self.seconddice)
        self.thirddiceLabel.setPixmap(self.thirddice)
        self.fourthdiceLabel.setPixmap(self.fourthdice)
        self.fifthdiceLabel.setPixmap(self.fifthdice)

        self.subWindow.rollButtonCount -= 1
        self.rollButton.setText("ROLL! ({})".format(self.subWindow.rollButtonCount))

        self.diceMainToSubList = self.randomList # 생성자에 있는 서브윈도우로 전달할 리스트를 랜덤리스트와 동일하게 만들어줌
        self.subWindow.diceList = self.diceMainToSubList # Roll 버튼 누를 때마다 subwindow의 diceList에 변화가 있도록 해준다

        self.subWindow.setButtons()


    def diceButtonClicked(self):
        if self.sender().text() == "Fixed!":
            self.sender().setText("Fix!")
        elif self.sender().text() == "Fix!":
            self.sender().setText("Fixed!")

    def createSubWindow(self):
        self.subWindow = SubWindow()
        self.subWindow.show()

    def playButtonClicked(self):
        self.subWindow.List1.append(0)

        for button in self.diceButtonList:
            button.setText("Fix!")
        self.subWindow.rollButtonCount = 3
        self.rollButton.setText("ROLL! ({})".format(self.subWindow.rollButtonCount))

        # 랜덤 상수 리스트 선언
        for i in range(5):
            if self.diceButtonList[i].text() == "Fix!":
                self.randomList[i] = np.random.randint(1, 7)
            else: continue


        # 랜덤 리스트에서 생성된 상수들로 주사위 지정
        for i in range(5):
                self.diceList[i].load("dice_{}".format(self.randomList[i]))

        self.firstdiceLabel.setPixmap(self.firstdice)
        self.seconddiceLabel.setPixmap(self.seconddice)
        self.thirddiceLabel.setPixmap(self.thirddice)
        self.fourthdiceLabel.setPixmap(self.fourthdice)
        self.fifthdiceLabel.setPixmap(self.fifthdice)

        self.diceMainToSubList = self.randomList # 생성자에 있는 서브윈도우로 전달할 리스트를 랜덤리스트와 동일하게 만들어줌
        self.subWindow.diceList = self.diceMainToSubList # Roll 버튼 누를 때마다 subwindow의 diceList에 변화가 있도록 해준다

        self.subWindow.setButtons()

        self.rollButton.setEnabled(True)


    # 치트키 생성 메소드
    def killButtonClicked(self):
        self.subWindow.attackDamage = self.monsterList[self.monstercount][1]

    # 몬스터 생성 메소드
    def createMonster(self):
        if self.subWindow.List1 == self.subWindow.List2:
            self.playButton.setEnabled(False)
        else:
            self.rollButton.setEnabled(False)
            self.playButton.setEnabled(True)

        if self.subWindow.List1 == [] and self.subWindow.List2 == [] and self.subWindow.total != 0:
            self.rollButton.setEnabled(True)

        if self.monstercount == 0:
            self.monsterList[self.monstercount][0].load("monster_{}".format(self.monstercount + 1))
            self.monsterLabel.setPixmap(self.monsterList[self.monstercount][0])

            self.healthpointBar.setMaximum(self.monsterList[self.monstercount][1])
            self.healthpointBar.setValue(self.monsterList[self.monstercount][1] - self.subWindow.total)

            if self.subWindow.total >= self.monsterList[self.monstercount][1]:
                self.healthpointBar.setValue(0)

            self.maintextBrowser.setText("Round: {}\n\n"
                                            "HP: {}\n\n주사위를 굴려 몬스터를 쓰러트리세요!".
                                            format(self.monstercount + 1, self.monsterList[self.monstercount][1]))

            if self.monsterList[self.monstercount][1] <= self.subWindow.attackDamage:
                self.monstercount += 1
                self.subWindow.attackDamage = 0

        if self.monstercount == 1:
            self.monsterList[self.monstercount][0].load("monster_{}".format(self.monstercount + 1))
            self.monsterLabel.setPixmap(self.monsterList[self.monstercount][0])

            self.healthpointBar.setMaximum(self.monsterList[self.monstercount][1])
            self.healthpointBar.setValue(self.monsterList[self.monstercount][1] - self.subWindow.total)

            if self.subWindow.total >= self.monsterList[self.monstercount][1]:
                self.healthpointBar.setValue(0)

            self.maintextBrowser.setText("Round: {}\n\n"
                                         "HP: {}\n\n주사위를 굴려 몬스터를 쓰러트리세요!".
                                         format(self.monstercount + 1, self.monsterList[self.monstercount][1]))

            if self.monsterList[self.monstercount][1] <= self.subWindow.attackDamage:
                self.monstercount += 1
                self.subWindow.attackDamage = 0

        if self.monstercount == 2:
            self.monsterList[self.monstercount][0].load("monster_{}".format(self.monstercount + 1))
            self.monsterLabel.setPixmap(self.monsterList[self.monstercount][0])

            self.healthpointBar.setMaximum(self.monsterList[self.monstercount][1])
            self.healthpointBar.setValue(self.monsterList[self.monstercount][1] - self.subWindow.total)

            if self.subWindow.total >= self.monsterList[self.monstercount][1]:
                self.healthpointBar.setValue(0)

            self.maintextBrowser.setText("Round: {}\n\n"
                                         "HP: {}\n\n주사위를 굴려 몬스터를 쓰러트리세요!".
                                         format(self.monstercount + 1, self.monsterList[self.monstercount][1]))

            if self.monsterList[self.monstercount][1] <= self.subWindow.attackDamage:
                self.monstercount += 1
                self.subWindow.attackDamage = 0

        if self.monstercount == 3:
            self.monsterList[self.monstercount][0].load("monster_{}".format(self.monstercount + 1))
            self.monsterLabel.setPixmap(self.monsterList[self.monstercount][0])

            self.healthpointBar.setMaximum(self.monsterList[self.monstercount][1])
            self.healthpointBar.setValue(self.monsterList[self.monstercount][1] - self.subWindow.total)

            if self.subWindow.total >= self.monsterList[self.monstercount][1]:
                self.healthpointBar.setValue(0)

            self.maintextBrowser.setText("Round: {}\n\n"
                                         "HP: {}\n\n주사위를 굴려 몬스터를 쓰러트리세요!".
                                         format(self.monstercount + 1, self.monsterList[self.monstercount][1]))

            if self.monsterList[self.monstercount][1] <= self.subWindow.attackDamage:
                self.monstercount += 1
                self.subWindow.attackDamage = 0

        if self.monstercount == 4:
            self.monsterList[self.monstercount][0].load("monster_{}".format(self.monstercount + 1))
            self.monsterLabel.setPixmap(self.monsterList[self.monstercount][0])

            self.healthpointBar.setMaximum(self.monsterList[self.monstercount][1])
            self.healthpointBar.setValue(self.monsterList[self.monstercount][1] - self.subWindow.total)

            if self.subWindow.total >= self.monsterList[self.monstercount][1]:
                self.healthpointBar.setValue(0)

            self.maintextBrowser.setText("Round: {}\n\n"
                                         "HP: {}\n\n주사위를 굴려 몬스터를 쓰러트리세요!".
                                         format(self.monstercount + 1, self.monsterList[self.monstercount][1]))

            if self.monsterList[self.monstercount][1] <= self.subWindow.attackDamage:
                self.monstercount += 1
                self.subWindow.attackDamage = 0

        if self.monstercount == 5:
            self.monsterList[self.monstercount][0].load("monster_{}".format(self.monstercount + 1))
            self.monsterLabel.setPixmap(self.monsterList[self.monstercount][0])

            self.healthpointBar.setMaximum(self.monsterList[self.monstercount][1])
            self.healthpointBar.setValue(self.monsterList[self.monstercount][1] - self.subWindow.total)
            
            if self.subWindow.total >= self.monsterList[self.monstercount][1]:
                self.healthpointBar.setValue(0)

            self.maintextBrowser.setText("Round: {}\n\n"
                                         "HP: {}\n\n주사위를 굴려 몬스터를 쓰러트리세요!".
                                         format(self.monstercount + 1, self.monsterList[self.monstercount][1]))

            if self.monsterList[self.monstercount][1] <= self.subWindow.attackDamage:
                self.monstercount += 1
                self.subWindow.attackDamage = 0

        if self.monstercount == 6:

            self.ending = QPixmap()
            self.ending.load("Ending.png")
            self.monsterLabel.setPixmap(self.ending)

            self.healthpointBar.setValue(200)
            self.maintextBrowser.setText("Yacht Attack의 마지막 몬스터를 쓰러뜨렸습니다! 축하합니다!")

#서브 윈도우 객체 클래스 정의
class SubWindow(QDialog, subwindow_form):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Yacht Dice!")
        self.setWindowIcon(QIcon('dice-152179_1280.png'))
        self.setGeometry(155, 120, 300, 800)

        self.List1 = []
        self.List2 = []

        self.diceList = []
        self.total = 0
        self.rollButtonCount = 3
        self.attackButtoncount = 0
        self.playcount = 0
        self.attackDamage = 0

        self.attackButton.setVisible(False)

        self.acesButton.clicked.connect(self.clickscoreButton)
        self.twosButton.clicked.connect(self.clickscoreButton)
        self.threesButton.clicked.connect(self.clickscoreButton)
        self.foursButton.clicked.connect(self.clickscoreButton)
        self.fivesButton.clicked.connect(self.clickscoreButton)
        self.sixesButton.clicked.connect(self.clickscoreButton)
        self.choiceButton.clicked.connect(self.clickscoreButton)
        self.fourofakindButton.clicked.connect(self.clickscoreButton)
        self.fullhouseButton.clicked.connect(self.clickscoreButton)
        self.littlestraightButton.clicked.connect(self.clickscoreButton)
        self.bigstraightButton.clicked.connect(self.clickscoreButton)
        self.yachtButton.clicked.connect(self.clickscoreButton)

        self.attackButton.clicked.connect(self.attackButtonClicked)

    def setButtons(self):
        if self.acesButton.isEnabled():
            self.acesButton.setText(str(ScoreFunction.acesCalc(self.diceList)))
        if self.twosButton.isEnabled():
            self.twosButton.setText(str(ScoreFunction.twosCalc(self.diceList)))
        if self.threesButton.isEnabled():
            self.threesButton.setText(str(ScoreFunction.threesCalc(self.diceList)))
        if self.foursButton.isEnabled():
            self.foursButton.setText(str(ScoreFunction.foursCalc(self.diceList)))
        if self.fivesButton.isEnabled():
            self.fivesButton.setText(str(ScoreFunction.fivesCalc(self.diceList)))
        if self.sixesButton.isEnabled():
            self.sixesButton.setText(str(ScoreFunction.sixesCalc(self.diceList)))
        if self.choiceButton.isEnabled():
            self.choiceButton.setText(str(ScoreFunction.choiceCalc(self.diceList)))
        if self.fourofakindButton.isEnabled():
            self.fourofakindButton.setText(str(ScoreFunction.fourofakindCalc(self.diceList)))
        if self.fullhouseButton.isEnabled():
            self.fullhouseButton.setText(str(ScoreFunction.fullhouseCalc(self.diceList)))
        if self.littlestraightButton.isEnabled():
            self.littlestraightButton.setText(str(ScoreFunction.littlestraightCalc(self.diceList)))
        if self.bigstraightButton.isEnabled():
            self.bigstraightButton.setText(str(ScoreFunction.bigstraightCalc(self.diceList)))
        if self.yachtButton.isEnabled():
            self.yachtButton.setText(str(ScoreFunction.yachtCalc(self.diceList)))

    def clickscoreButton(self):
        self.count = self.sender().text()
        self.total += int(self.count)
        self.List2.append(0)
        self.playcount += 1
        self.attackButtoncount += 1

        if self.attackButtoncount == 12:
            self.attackButton.setVisible(True)
            self.attackButton.setEnabled(True)
            self.attackButtoncount = 0

        self.totalTextBrowser.setText(str(self.total))

        self.sender().setEnabled(False)
        self.sender().setText("Checked as {}".format(self.count))


    def attackButtonClicked(self):
        self.List1 = []
        self.List2 = []
        self.attackButtoncount = 1
        self.attackButton.setVisible(False)
        self.attackDamage = self.total
        self.total = 0
        self.totalTextBrowser.setText(str(self.total))

        self.acesButton.setEnabled(True)
        self.twosButton.setEnabled(True)
        self.threesButton.setEnabled(True)
        self.foursButton.setEnabled(True)
        self.fivesButton.setEnabled(True)
        self.sixesButton.setEnabled(True)
        self.choiceButton.setEnabled(True)
        self.fourofakindButton.setEnabled(True)
        self.fullhouseButton.setEnabled(True)
        self.littlestraightButton.setEnabled(True)
        self.bigstraightButton.setEnabled(True)
        self.yachtButton.setEnabled(True)

        self.acesButton.setText("0")
        self.twosButton.setText("0")
        self.threesButton.setText("0")
        self.foursButton.setText("0")
        self.fivesButton.setText("0")
        self.sixesButton.setText("0")
        self.choiceButton.setText("0")
        self.fourofakindButton.setText("0")
        self.fullhouseButton.setText("0")
        self.littlestraightButton.setText("0")
        self.bigstraightButton.setText("0")
        self.yachtButton.setText("0")

        self.attackButtoncount = 0


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    mainWindow = MainWindow()

    #프로그램 화면을 보여주는 코드
    mainWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
