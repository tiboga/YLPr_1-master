import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView


class AskDelDial(QDialog):
    def __init__(self, id):
        super().__init__()
        uic.loadUi('askdeldialog.ui', self)
        self.yes.clicked.connect(self.update_out)
        self.no.clicked.connect(self.update_out)
        self.con = sqlite3.connect('guns.db')
        self.out = False
        self.id = id
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.update_table()

    def update_table(self):
        self.id = tuple([int(i) for i in self.id])
        qry = "SELECT * FROM guns_info WHERE id IN (" + ", ".join('?' * len(self.id)) + ")"
        cur = self.con.cursor()
        res = cur.execute(qry, self.id).fetchall()
        self.table.setColumnCount(17)
        self.table.setRowCount(0)
        for i, row in enumerate(res):
            self.table.setRowCount(
                self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.con.commit()

    def update_out(self):
        send = self.sender()
        if send.text() == 'Да':
            self.out = True
        else:
            self.out = False
        self.close()

    def ret(self):
        return self.out
