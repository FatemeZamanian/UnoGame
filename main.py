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
        self.color = None
        self.ui.btnuno.clicked.connect(partial(self.check_uno,True))
        self.start()
        self.ui.show()

    def change_color(self):
        self.color_window = ColorForm()
        self.label_color()

    def start(self):
        self.turn='user'
        self.over_bank=[]
        global c2pls
        c2pls=0
        self.bank=['+41','+42','b00','b11','b21','b31','b41','b51','b61','b71','b81','b91','b+21','br1','bs1',
        'g00','g11','g21','g31','g41','g51','g61','g71','g81','g91','g+21','gr1','gs1',
        'r00','r11','r21','r31','r41','r51','r61','r71','r81','r91','r+21','rr1','rs1',
        'y00','y11','y21','y31','y41','y51','y61','y71','y81','y91','y+21','yr1','ys1',
        'w1','w2']
        self.special_cards=['+41','+42','w1','w2']
        card=None
        self.player_cards=[]
        self.pc_cards=[]
        self.uno_flag_user=False
        self.uno_flag_pc=False
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
                self.over_bank.append(self.center_card)
                break
        self.show_cards()
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
            if self.turn=='user':
                btn.isEnabled=True
            self.ui.l_player.addWidget(btn, i)

        for i in reversed(range(self.ui.l_pc.count())):
            self.ui.l_pc.itemAt(i).widget().setParent(None)

        for i,c in enumerate(self.pc_cards):
            btn = QPushButton()
            btn.setMinimumSize(75, 121)
            btn.setMaximumSize(75, 121)
            btn.setStyleSheet(f'background-image: url(cart/{c}.jpg);')
            btn.setFixedHeight(121)
            btn.isEnabled=False
            self.ui.l_pc.addWidget(btn, i)
        self.ui.lbl_center.setStyleSheet(f'background-image: url(cart/{self.center_card}.jpg);')
        self.ui.lbl_turn.setText(str(self.turn)+'s turn')
        

    def check2p(self):
        s=self.center_card
        self.turn='user'
        if s[1]=='+':
                for x in self.player_cards:
                    if x[1]=='+':
                        self.ui.lbl_status.setText('user 2pluse checked')
                        break
                else:
                    self.twoplus(flag=False)
        # print('user 2pluse checked')
        
            


    def twoplus(self,flag=None,p=None):
        global c2pls
        
        if self.turn=='user':
            if flag:
                self.center_card=p
                self.player_cards.remove(p)
                self.over_bank.append(p)
                self.color=self.center_card[0]
                self.show_cards()
                self.check_bank()
                c2pls+=2
                self.turn='pc'
                # print('user have 2pluse ')
                self.ui.lbl_status.setText('user have 2pluse')
                self.twoplus()
                # self.pc_play()
            else:
                for _ in range(c2pls):
                    x=random.choice(self.bank)
                    self.player_cards.append(x)
                    self.check_bank()
                    self.bank.remove(x)
                c2pls=0
                # print('user NOT have 2pluse ')
                self.ui.lbl_status.setText('user Not have 2pluse')
                self.turn='pc'
                self.pc_play()
                self.show_cards()
                
            
        else:
            for x in self.pc_cards:
                if x[1]=='+':
                    self.pc_cards.remove(x)
                    self.center_card=x
                    self.show_cards()
                    self.turn='user'
                    c2pls +=2
                    # print('pc have 2pluse ')
                    self.ui.lbl_status.setText('pc have 2pluse')
                    self.check2p()
                    break

            else:
                #اگر کامپیوتر ۲پلاس نداشت
                for _ in range(c2pls):
                    x=random.choice(self.bank)
                    self.pc_cards.append(x)
                    self.check_bank()
                    self.bank.remove(x)
                c2pls=0
                self.turn='user'
                # print('pc NOT have 2pluse ')
                self.ui.lbl_status.setText('pc Not have 2pluse')
                
                # self.turn='pc'
                self.play()
                # self.pc_play()
                
                self.show_cards()


    def fourplus(self):
        if self.turn=='user':
            self.change_color()
            for _ in range(4):
                x=random.choice(self.bank)
                self.pc_cards.append(x)
                self.check_bank()
                self.bank.remove(x)
            self.turn='user'
        elif self.turn=='pc':
            self.color=random.choice(['r','b','g','y'])
            self.label_color()
            for _ in range(4):
                x=random.choice(self.bank)
                self.player_cards.append(x)
                self.check_bank()
                self.bank.remove(x)
            self.turn='user'
        self.show_cards()

    def play(self):
        s=self.center_card
        if s[0] !='w':
            self.color=s[0]
            self.label_color()
        if self.turn=='user':
            for x in self.player_cards:
                if x[0]==self.color or x[1]==s[1] or x in self.special_cards and len(self.player_cards) !=0:
                    #self.ui.lbl_status.setText('done for user')
                    break
            else:
                if len(self.player_cards) !=0:
                    x=random.choice(self.bank)
                    self.player_cards.append(x)
                    self.bank.remove(x)
                    self.ui.lbl_status.setText('one card for user :D')
                    # print('NOT done for user')
                    self.turn='pc'
                    self.pc_play()
                    self.show_cards()

                
        else:
            for x in self.pc_cards:
                if x[0]==self.color or x[1]==s[1] or x in self.special_cards:
                    #self.ui.lbl_status.setText('done for pc')
                    # print('done for pc')
                    break
            else:
                if len(self.pc_cards) !=0:
                    x=random.choice(self.bank)
                    self.pc_cards.append(x)
                    self.bank.remove(x)
                    self.ui.lbl_status.setText('one card for pc :D')
                    # print('NOT done for pc')
                    self.turn='user'
                    self.show_cards()
                



    def player_play(self,num_pic):
        global c2pls
        p=self.player_cards[num_pic]
        s=self.center_card
        if s[0]=='w':
            s='---'
            self.label_color()
        if self.turn=='user' and c2pls==0:
            if p[0]==self.color or p[1]==s[1] or p in self.special_cards or s in self.special_cards :
                self.center_card=p
                self.player_cards.remove(p)
                self.over_bank.append(p)
                if self.center_card[0] !='w':
                    self.color=self.center_card[0]
                self.show_cards()
                self.check_bank()
                self.turn='pc'
                if p[1]=='+':
                    self.turn='pc'
                    c2pls+=2
                    self.twoplus()
                    # return
                elif p[0]=='w':
                    self.turn='user'
                    self.color='-'
                    s='-'
                    self.change_color()
                    if self.color !='-':
                        self.turn='pc'
                        self.label_color()
                        self.pc_play()
                elif p[0]=='+':
                    self.turn='user'
                    self.fourplus()
                    self.label_color()
              
                elif p[1]=='r' or p[1]=='s':
                    self.turn='user'
                    self.play()
                
        elif self.turn=='user' and p[1]=='+' and s[1]=='+':
                self.twoplus(p=p,flag=True)
        self.play()
        self.pc_play()
        self.check_win() 
        # self.shw_res()



    def pc_play(self):
        global c2pls
        s=self.center_card
        if s[0]=='w':
            s='---'
        if self.turn=='pc' and c2pls==0:
            for p in self.pc_cards:
                if p[0]==self.color or p[1]==s[1] or p in self.special_cards or s in self.special_cards :
                    self.center_card=p
                    if self.center_card[0] !='w':
                        self.color=self.center_card[0]
                    self.pc_cards.remove(p)
                    self.over_bank.append(p)
                    self.show_cards()
                    self.check_bank()
                    self.turn='user'
                    if p[1]=='+':
                        self.turn='user'
                        c2pls+=2
                        self.check2p()
                    elif p[0]=='w':
                        self.color=random.choice(['r','b','g','y'])
                        self.label_color()
                        self.turn='user'
                    elif p[0]=='+':
                        self.turn='pc'
                        self.fourplus()
                    elif p[1]=='r' or p[1]=='s':
                        self.turn='pc'
                        self.pc_play()
                    self.shw_res()
                    self.check_bank()
                    self.play() 
                    break
        elif s[1]=='+' and  self.turn=='pc':
            for p in self.pc_cards:
                if p[1]=='+':
                    self.twoplus()
        self.check_uno()
        self.check_win()   
        self.play() 
                    
             
        self.shw_res()
            

    def check_bank(self):
        if len(self.bank)==0:
            self.bank=self.over_bank
            self.over_bank=[]



    def check_win(self):
        if self.turn=='user' and self.uno_flag_user and len(self.player_cards)==0:
            self.ui.lbl_status.setText('player win :)')
            time.sleep(5)
            self.start()
        elif self.turn=='user' and self.uno_flag_user==False and len(self.player_cards)==0:
            self.ui.lbl_status.setText('player win but not press uno...')
            x=random.choice(self.bank)
            self.player_cards.append(x)
            self.bank.remove(x)
            self.show_cards()
        elif self.turn=='pc' and self.uno_flag_pc and len(self.pc_cards)==0:
            self.ui.lbl_status.setText('pc win :)')
            time.sleep(5)
            self.start()
        

    def check_uno(self,click=False):
        if click==True and len(self.player_cards)==1:
            self.uno_flag_user=True
            self.ui.lbl_status.setText('user said uno...')
        elif len(self.pc_cards)==1:
            self.uno_flag_pc=True
            self.ui.lbl_status.setText('pc said uno...')
            

    def shw_res(self):
        global c2pls
        print('c2pls: ',c2pls)
        # print('center: ',self.center_card)
        # print('turn : ',self.turn)
        # print('player :',self.player_cards)
        # print('pc: ',self.pc_cards)

    def label_color(self):
        if self.color=='r':
            self.ui.lbl_status.setStyleSheet('background-image: url(red.png);')
            print('red')
        if self.color=='g':
            self.ui.lbl_status.setStyleSheet('background-image: url(green.png);')
        if self.color=='b':
            self.ui.lbl_status.setStyleSheet('background-image: url(blue.jpg);')
        if self.color=='y':
            self.ui.lbl_status.setStyleSheet('background-image: url(yellow.jpg);')

if __name__ == "__main__":
    app = QApplication([])
    widget =uno()
    sys.exit(app.exec())