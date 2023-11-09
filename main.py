import sqlite3
import sys
from inpgialog import InputDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QMainWindow
from deldialog import DelDial


class NoCorrectInput(Exception):
    pass


class Spravochnik(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.addbutton.clicked.connect(self.add)
        self.delbutton.clicked.connect(self.remove)
        self.connection = sqlite3.connect("guns.db")
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.out_data()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def add(self):
        self.inp_sp_win = InputDialog()
        self.inp_sp_win.exec()
        self.out_data()

    def remove(self):
        self.rem = DelDial()
        self.rem.exec()
        self.out_data()

    def out_data(self):
        query = "SELECT * FROM guns_info"
        res = self.connection.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row[1:]):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Spravochnik()
    ex.show()
    sys.exit(app.exec_())
