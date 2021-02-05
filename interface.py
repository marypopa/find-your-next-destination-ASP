import sys
from PyQt5.QtWidgets import QApplication, QPlainTextEdit,QWidget, QPushButton,QLabel, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from clyngor import ASP, solve
import os
import re

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Choose your destination'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 500

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        intro_label = QLabel(self)
        intro_label.setText("Choose your next destination")
        intro_label.move(75,20)

        continent_label = QLabel('&continent',self)
        continent_label.setText("Continent")
        continent_label.move(50,50)
        island_label = QLabel(self)
        island_label.setText('Island?')
        island_label.move(200, 50)

        self.combo_continent = QComboBox(self)
        self.combo_island = QComboBox(self)
        self.combo_continent.addItems(['Europe', 'Asia','America', 'Oceania'])
        self.combo_continent.move(40, 70)

        self.combo_island.addItems(['Yes', 'No'])
        self.combo_island.move(200, 70)

        button = QPushButton('Search', self)
        button.move(100, 150)
        button.clicked.connect(self.on_click)

        self.textarea = QPlainTextEdit(self)
        self.textarea.move(30, 200)
        #self.textarea.resize(100, 250)

        self.show()


    @pyqtSlot()
    def on_click(self):
        self.textarea.clear()
        island = self.combo_island.currentText()
        continent = self.combo_continent.currentText()
        query = 'available_destinations(X):-'
        if island == 'Yes':
            query = query + 'islands(X),'
        if island == 'No':
            query = query + 'not islands(X),'
        if continent == 'Europe':
            query = query + 'is_in_europe(X),'
        if continent == 'America':
            query = query + 'is_in_america(X),'
        if continent == 'Asia':
            query = query + 'is_in_asia(X),'
        if continent == 'Oceania':
            query = query + 'is_in_oceania(X),'
        query = query + 'incidence_rate(X, L1), incidence_rate(romania, L2), L1+50<L2.'
        with open("countries_and_incidance_rate.lp","r") as myfile:
            lines = myfile.readlines()
            myfile.close()
            print(lines)
        with open("asp.lp","w") as myfile:
            myfile.writelines(lines)
            myfile.write("\n" + query + "\n")
            myfile.write("#show available_destinations/1.")
        cmd = 'clingo asp.lp 0 > out_file.txt'
        os.system(cmd)
        with open("out_file.txt", "r") as myfile:
            lines = myfile.readlines()
            for line in lines:
                if 'available_destinations' in line:
                    answers = re.findall('\((.*?)\)',line)
            print(answers)
            myfile.close()
        self.textarea.insertPlainText(str(answers))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())