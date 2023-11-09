import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QAbstractItemView


class InputDialog(QDialog):
    def __init__(self):
        self.data = []
        super().__init__()
        uic.loadUi('inputdialog.ui', self)
        self.ok.clicked.connect(self.ret)
        self.no.clicked.connect(self.close_win)
        self.con = sqlite3.connect('guns.db')
        self.dict = {0: 'Наименование', 1: 'Класс', 2: 'Ранг', 3: 'Бартер', 4: 'Вес', 5: 'Урон', 6: 'Макс. дистанция',
                     7: 'Скорострельность', 8: 'Перезарядка', 9: 'Разброс', 10: 'Разброс от бедра', 11: 'Отдача',
                     12: 'Гориз. Отдача', 13: 'Доставание', 14: 'Прицеливание', 15: 'Шанс клина'}
        self.data = False
        self.znach = False

    def close_win(self):
        self.close()

    def ret(self):
        self.send = self.sender().text()
        if self.send == 'no':
            self.data = False
        else:
            self.data = True
            FLAG = True
            data = []
            pola = list()
            for i in range(self.tableWidget.rowCount()):
                try:
                    if self.tableWidget.item(i, 0).text() == '':
                        FLAG = False
                        pola.append(self.dict[i])
                    else:
                        data.append(self.tableWidget.item(i, 0).text())
                except:
                    FLAG = False
                    pola.append(self.dict[i])
            if FLAG:
                self.znach = True
                cur = self.con.cursor()
                ids = list(cur.execute("""SELECT id from guns_info"""))
                if ids:
                    id = max([int(i[0]) for i in ids]) + 1
                else:
                    id = 1
                params = (int(id), str(data[0]), str(data[1]), str(data[2]), str(data[3]),
                          str(data[4]), str(data[5])
                          , str(data[6]), str(data[7]), str(data[8]), str(data[9]), str(data[10]), str(data[11]),
                          str(data[12]),
                          str(data[13]), str(data[14]),
                          str(data[15]))
                cur.execute(
                    f'''INSERT INTO guns_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', params)
                self.con.commit()
            else:
                if len(pola) == 1:
                    pipipu = f'Не заполнено поле со значением:'+'\n'+' {pola[0]}'
                    self.errlabel.setText(pipipu)
                else:
                    self.errlabel.setText('Не заполнено поля со значениями: '+'\n' + '\n'.join(pola))
                return

            # self.data = data
            self.accept()
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.ret()
        if event.key() == Qt.Key_Escape:
            self.close()
