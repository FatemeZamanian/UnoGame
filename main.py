# This Python file uses the following encoding: utf-8

import sys
import os
import random
import time

from functools import partial

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *


class uno(QWidget):
    def __init__(self):
        super(uno, self).__init__()
        loader=QUiLoader()
        self.ui=loader.load("form.ui")
        self.ui.btnexit.clicked.connect(self.ext)
        self.ui.btnnewgame.clicked.connect(self.new)
        self.ui.show()
        
    
    def ext(self):
        exit()
    
    def new(self):
        global main_window
        self.hide()
        main_window = MainForm(self)
        main_window.show()
        main_window.show_cards()


class ColorForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loader=QUiLoader()
        self.ui=loader.load("colors.ui")
        self.ui.show()

        self.ui.btn_blue.clicked.connect(partial(self.func_color,'b'))
        self.ui.btn_red.clicked.connect(partial(self.func_color,'r'))
        self.ui.btn_yellow.clicked.connect(partial(self.func_color,'y'))
        self.ui.btn_green.clicked.connect(partial(self.func_color,'g'))

    def func_color(self,c):
        main_window.color =c
        self.ui.hide()

class MainForm(QWidget):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        loader=QUiLoader()
        self.ui=loader.load("form2.ui")
        self.ui.show()
        self.color = None
        self.start()

    def change_color(self):
        self.color_window = ColorForm()

    def start(self):
        self.turn='user'
        self.flagTwo=False
        self.over_bank=[]
        self.bank=['+41','+42','b00','b11','b21','b31','b41','b51','b61','b71','b81','b91','b+21','br1','bs1',
        'g00','g11','g21','g31','g41','g51','g61','g71','g81','g91','g+21','gr1','gs1',
        'r00','r11','r21','r31','r41','r51','r61','r71','r81','r91','r+21','rr1','rs1',
        'y00','y11','y21','y31','y41','y51','y61','y71','y81','y91','y+21','yr1','ys1',
        'w1','w2']
        self.special_cards=['+41','+42','w1','w2']
        card=0
        self.player_cards=[]
        self.pc_cards=[]
        for _ in range(7):
            card=random.choice(self.bank)
            self.bank.remove(card)
            self.player_cards.append(card)

            card=random.choice(self.bank)
            self.bank.remove(card)
            self.pc_cards.append(card)
        while True:      
            self.center_card=random.choice(self.bank)
            if self.center_card not in(self.special_cards) and self.center_card[1]!='+' and self.center_card[1]!='r' and self.center_card[1]!='s':
                self.color=self.center_card[0]
                self.bank.remove(self.center_card)
                self.ui.lbl_center.setStyleSheet(f'background-image: url(cart/{self.center_card}.jpg);')
                break
        self.play()
    def show_cards(self):
        for i in reversed(range(self.ui.l_player.count())):
            self.ui.l_player.itemAt(i).widget().setParent(None)

        for i,c in enumerate(self.player_cards):
            btn = QPushButton()
            btn.setMinimumSize(75, 121)
            btn.setMaximumSize(75, 121)
            btn.clicked.connect(partial(self.player_play,i))
            btn.setStyleSheet(f'background-image: url(cart/{c}.jpg);')
            btn.setFixedHeight(121)
            self.ui.l_player.addWidget(btn, i)

        for i in reversed(range(self.ui.l_pc.count())):
            self.ui.l_pc.itemAt(i).widget().setParent(None)

        for i,c in enumerate(self.pc_cards):
            btn = QPushButton()
            btn.setMinimumSize(75, 121)
            btn.setMaximumSize(75, 121)
            btn.setStyleSheet(f'background-image: url(cart/{c}.jpg);')
            btn.setFixedHeight(121)
            self.ui.l_pc.addWidget(btn, i)
        self.ui.lbl_center.setStyleSheet(f'background-image: url(cart/{self.center_card}.jpg);')
        self.ui.lbl_turn.setText(str(self.turn)+'s turn')
        time.sleep(1)
        

    def twoplus(self):
        if self.turn=='user':
            pass
        else:
            for x in self.pc_cards:
                if x[1]=='+':
                    self.pc_cards.remove(x)
                    self.turn=True
                    self.twoplus()
                    return

            else:
                #اگر کامپیوتر ۲پلاس نداشت
                for i in range(2):
                    x=random.choice(self.bank)
                    self.player_cards.append(x)
                    self.check_bank()
                    self.bank.remove(x)


       
    def fourplus(self):
        for i in range(4):
            x=random.choice(self.bank)
            self.player_cards.append(x)
            self.check_bank()
            self.bank.remove(x)

        
        
    def play(self):
        s=self.center_card
        self.color=s[0]
        if self.turn=='user':
            for x in self.player_cards:
                if x[0]==self.color or x[1]==s[1] or x in self.special_cards:
                    break
            else:
                x=random.choice(self.bank)
                self.player_cards.append(x)
                self.bank.remove(x)
                self.turn='pc'
                self.pc_play()
        else:
            for x in self.pc_cards:
                if x[0]==self.color or x[1]==s[1] or x in self.special_cards:
                    break
            else:
                x=random.choice(self.bank)
                self.pc_cards.append(x)
                self.bank.remove(x)
                self.turn='user'



    def player_play(self,num_pic):
        p=self.player_cards[num_pic]
        s=self.center_card
        if self.turn=='user':
            if p[0]==self.color or p[1]==s[1] :
                self.center_card=p
                self.player_cards.remove(p)
                self.over_bank.append(p)
                self.color=self.center_card[0]
                self.show_cards()
                self.check_bank()
                if p[1]=='+':
                    self.twoplus()
                    self.turn='pc'
                    self.play()
                # if p[0]=='w':
                #     self.change_color()
                #     print(self.color)
                #     self.turn=False 
                #     self.play()
                #     self.pc_play()
                # if p[0]=='+':
                #     self.fourplus(p)
                #     self.turn=False
                #     self.play()
                #     self.pc_play()
                if p[1]=='r' or p[1]=='s':
                    self.turn='user'
                    self.play()
        self.pc_play()

    def pc_play(self):
        s=self.center_card
        for p in self.pc_cards:
            if p[0]==self.color or p[1]==s[1] and self.turn=='pc':
                self.center_card=p
                self.pc_cards.remove(p)
                self.over_bank.append(p)
                self.show_cards()
                self.check_bank()
                if p[1]=='+':
                    self.twoplus()
                    self.turn='user'
                # if p[0]=='w':
                #     self.change_color()
                #     print(self.color)
                #     self.turn=True
                #     self.player_play()
                # if p[0]=='+':
                #     self.fourplus(p)
                #     self.turn=True
                #     self.player_play()
                if p[1]=='r' or p[1]=='s':
                    self.turn='pc'
                    self.play()
                break
        else:
            self.check_bank()
            self.play()
            time.sleep(1)      
        

    def check_bank(self):
        if len(self.bank)==0:
            self.bank=self.over_bank
            self.over_bank=[]

if __name__ == "__main__":
    app = QApplication([])
    widget =uno()
    sys.exit(app.exec())