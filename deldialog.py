import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from askdeldialog import AskDelDial


class DelDial(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('deldialog.ui', self)
        self.con = sqlite3.connect('guns.db')
        self.delbt.clicked.connect(self.remove)
        self.close_bt.clicked.connect(self.close)
        self.out_data()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def out_data(self):
        query = "SELECT * FROM guns_info"
        res = self.con.cursor().execute(query).fetchall()
        self.table.setColumnCount(17)
        self.table.setRowCount(0)
        for i, row in enumerate(res):
            self.table.setRowCount(
                self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def remove(self):
        rows = list(set([i.row() for i in self.table.selectedItems()]))
        ids = [self.table.item(i, 0).text() for i in rows]
        if not ids:
            self.err_label.setText('Нет выделенных элементов')
            return
        self.err_label.setText('')
        self.ask = AskDelDial(ids)
        self.ask.exec()
        self.ret = self.ask.ret()
        if self.ret:
            cur = self.con.cursor()
            cur.execute("DELETE FROM guns_info WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.remove()
        if event.key() == Qt.Key_Escape:
            self.close()
