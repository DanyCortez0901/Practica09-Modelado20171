# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore, uic
from random import randint

class Snake():
    def __init__(self, red, green, blue):
        self.color = (red, green, blue)
        self.position = [[5,10],[6,10],[7,10], [8,10], [9,10], [10,10], [11,10],[12,10], [13,10]]
        self.large = len(self.position)
        self.direction = "Down"

class Interfaz_server(QtGui.QMainWindow):

    def __init__(self):
        super(Interfaz_server, self).__init__()
        uic.loadUi('servidor.ui', self)
        self.snakes = []
        self.pushButton_3.hide()
        self.start = False
        self.pausa = False
        self.timer = None
        self.change_table()
        self.fill()
        self.spinBox.valueChanged.connect(self.update_timer)
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.spinBox_2.valueChanged.connect(self.update)
        self.pushButton_2.clicked.connect(self.start_game)
        self.spinBox_3.valueChanged.connect(self.update)
        self.pushButton_3.clicked.connect(self.end_game)
        self.show()

    def start_game(self):
        if not self.start:
            snake = Snake(1,201,70)
            self.snakes.append(snake)
            self.paint_snakes()
            self.pushButton_2.setText("Stop")
            self.pushButton_3.show()
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.move_snakes)
            self.timer.start(100)
            self.tableWidget.installEventFilter(self)
            self.start = True
        elif self.start and not self.pausa:
            self.timer.stop()
            self.pausa = True
            self.pushButton_2.setText("Reanudar el Juego")
        elif self.pausa:
            self.timer.start()
            self.pausa = False
            self.pushButton_2.setText("Stop")

    def end_game(self):
        self.snakes = []
        self.timer.stop()
        self.start = False
        self.pushButton_2.setText("Play")
        self.pushButton_3.hide()
        self.fill()

    def update_timer(self):
        valor = self.spinBox.value()
        self.timer.setInterval(valor)

    def fill(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
                self.tableWidget.item(i,j).setBackground(QtGui.QColor(251,251,251))

    def change_table(self):
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def update(self):
        self.tableWidget.setColumnCount(self.spinBox_2.value())
        self.tableWidget.setRowCount(self.spinBox_3.value())
        self.fill()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress and source is self.tableWidget:
                direction = event.key()
                snake = self.snakes[0]
                if direction == QtCore.Qt.Key_Up:
                    if snake.direction is not "Down":
                        snake.direction = "Up"
                elif direction == QtCore.Qt.Key_Down:
                    if snake.direction is not "Up":
                        snake.direction = "Down"
                elif direction == QtCore.Qt.Key_Right:
                    if snake.direction is not "Left":
                        snake.direction = "Right"
                elif direction == QtCore.Qt.Key_Left:
                    if snake.direction is not "Right":
                        snake.direction = "Left"
        return QtGui.QMainWindow.eventFilter(self, source, event)

    def paint_snakes(self):
        snake = self.snakes[0]
        for box in snake.position:
            self.tableWidget.item(box[0], box[1]).setBackground(QtGui.QColor(snake.color[0], snake.color[1], snake.color[2]))


    def crash(self, snake):
        for box in snake.position[0:len(snake.position)-2]:
            if snake.position[-1][0] == box[0] and snake.position[-1][1] == box[1]:
                return True
        return False

    def move_snakes(self):
        snake = self.snakes[0]
        if self.crash(snake):
            self.snakes.remove(snake)
            self.fill()
            r,g,b = randint(0,255),randint(0,255),randint(0,255)
            snake_1 = Snake(r,g,b)
            self.snakes = [snake_1]
        self.tableWidget.item(snake.position[0][0],snake.position[0][1]).setBackground(QtGui.QColor(251,251,251))
        i = 0
        for box in snake.position[0: len(snake.position)-1]:
            i += 1
            box[0] = snake.position[i][0]
            box[1] = snake.position[i][1]

        rows = self.tableWidget.rowCount()
        columns =  self.tableWidget.columnCount()
        if snake.direction is "Down":
            if snake.position[-1][0] + 1 < rows:
                snake.position[-1][0] += 1
            else:
                snake.position[-1][0] = 0
        if snake.direction is "Right":
            if snake.position[-1][1] + 1 < columns:
                snake.position[-1][1] += 1
            else:
                snake.position[-1][1] = 0
        if snake.direction is "Up":
            if snake.position[-1][0] != 0:
                snake.position[-1][0] -= 1
            else:
                snake.position[-1][0] = rows-1
        if snake.direction is "Left":
            if snake.position[-1][1] != 0:
                snake.position[-1][1] -= 1
            else:
                snake.position[-1][1] = columns-1
        self.paint_snakes()


servidor = QtGui.QApplication(sys.argv)
interfaz = Interfaz_server()
sys.exit(servidor.exec_())
