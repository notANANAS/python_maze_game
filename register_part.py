import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

CONST_INDEX_PASS = 0

flag_done = False


class MyWidget(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        uic.loadUi('form.ui', self)
        self.con = sqlite3.connect("score.db")
        self.cur = self.con.cursor()
        self.names = {}
        self.res = ''
        self.level = ''
        for el in self.cur.execute(f"""SELECT * FROM account_scores""").fetchall():
            self.names[el[0]] = [el[1], el[0]]
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_register.clicked.connect(self.register)

    def login(self):
        global flag_done
        self.name = self.lineEdit_name.text()
        self.password = self.lineEdit_pass.text()
        if self.name in self.names.keys() and int(self.lineEdit_level.text()) in (1, 2, 3):
            if self.password == self.names[self.name][CONST_INDEX_PASS]:
                flag_done = True
                self.name_that_return = self.name
                self.level = int(self.lineEdit_level.text())
                print('Done')
                self.app.exit()
            else:
                self.lineEdit_name.setText('')
                self.lineEdit_pass.setText('')
        else:
            self.lineEdit_name.setText('')
            self.lineEdit_pass.setText('')

    def register(self):
        global flag_done
        self.name = self.lineEdit_name.text()
        self.password = self.lineEdit_pass.text()
        if self.name not in self.names.keys() and int(self.lineEdit_level.text()) in (1, 2, 3):
            self.res = f"""INSERT INTO account_scores (name, pass, score1, score2, score3) VALUES ('{self.name}', '{self.password}', 999, 999, 999)"""
            self.name_that_return = self.name
            self.cur.execute(self.res).fetchall()
            self.con.commit()
            flag_done = True
            self.level = int(self.lineEdit_level.text())
            print('Registered')
            self.app.exit()
        else:
            self.lineEdit_name.setText('')
            self.lineEdit_pass.setText('')
            self.lineEdit_level.setText('')

    def return_level(self):
        return self.level

    def return_name(self):
        return self.name_that_return
