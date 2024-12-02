import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.QtGui import QPixmap
import sqlite3
import mainForm
import menuForm


class Book(QMainWindow, menuForm.Ui_MainWindow):
    def __init__(self, index):
        super().__init__()

        self.setupUi(self)

        self.id = index

        self.con = sqlite3.connect("works.sqlite")
        self.cur = self.con.cursor()
        self.list = list(self.cur.execute(f"Select * from Works where Works.id = {self.id}").fetchall())[0]
        self.con.close()
        if self.list[-1]:
            self.pixmap = QPixmap(self.list[-1]).scaled(150, 150)
        else:
            self.pixmap = QPixmap("images/default.png").scaled(150, 150)

        self.labelName.setText(self.list[1])
        self.labelAuthor.setText(self.list[2])
        self.labelYear.setText(str(self.list[3]))
        self.labelGenre.setText(self.list[4])
        
        self.image.setPixmap(self.pixmap)


class MyWidget(QMainWindow, mainForm.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton.clicked.connect(self.updateTable)

        self.pushButton.setText("Искать")
    
    def updateTable(self):
        con = sqlite3.connect("works.sqlite")
        cur = con.cursor()
        if self.comboBox.currentIndex() == 1:
            text = f"""SELECT * FROM Works where Works.title like '%{self.lineEdit.text()}%'"""
        else:
            text = f"""SELECT * FROM Works where Works.author like '%{self.lineEdit.text()}%'"""
        self.p = cur.execute(text).fetchall()
        con.close()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(len(self.p))
        self.tableWidget.setColumnWidth(0, 450)
        for i, v in enumerate(self.p):
            button = QPushButton(v[1])
            button.clicked.connect(self.toggle)
            button.name = v[0]
            self.tableWidget.setCellWidget(i, 0, button)

    def toggle(self):
        obj = self.sender()
        self.form = Book(obj.name)
        self.form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
