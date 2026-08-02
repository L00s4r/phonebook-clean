from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from random import randint
app = QApplication([])
main_win = QWidget()
vbox = QVBoxLayout()
winner = QLabel('Нажми, чтобы участвовать')
textas = QLabel('?')
textas1 = QLabel('?')
btn = QPushButton('Испытать удачу')
winner.setAlignment(Qt.AlignCenter)
textas.setAlignment(Qt.AlignCenter)
textas1.setAlignment(Qt.AlignCenter)
vbox.addWidget(winner)
vbox.addWidget(textas)
vbox.addWidget(textas1)
vbox.addWidget(btn)
vbox.setAlignment(Qt.AlignCenter)
main_win.setLayout(vbox)
def on_button_click():
    num1 = randint(0, 9)
    num2 = randint(0, 9)
    textas.setText(str(num1))
    textas1.setText(str(num2))
    if num1 == num2:
        winner.setText('Вы выиграли! Сыграйте снова')
    else:
        winner.setText('Вы проиграли! Сыграйте снова')
btn.clicked.connect(on_button_click)
main_win.setWindowTitle('Лотерея')
main_win.move(960, 512)
main_win.resize(400, 400)
main_win.show()
app.exec_()