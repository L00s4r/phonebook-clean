from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from random import randint
class MainWin(QWidget):
    def __init__(self, ):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('JustApp')
        self.button = QPushButton('Сгенерировать файл', self)
        self.button.setGeometry(210, 200, 200, 40)
        self.button.setStyleSheet('''QPushButton {
        font-size: 20px; 
        font-family: Comic Sans MS; 
        background-color: green; 
        border: none; 
        border-radius: 8px;
    }

    QPushButton:hover {
        opacity: 0.8; 
    }

    QPushButton:pressed {
        background-color: lightgreen;
        border: 2px solid white;
        border-radius: 8px;
    }''')
        self.button.clicked.connect(self.GenerateFile)
    def GenerateFile(self):
        with open('for_lesson8.txt', 'w', encoding='utf-8') as file:
            for i in range(100):
                a = randint(0, 100)
                file.write(f'{a}\n')
if __name__ == '__main__':
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec_()