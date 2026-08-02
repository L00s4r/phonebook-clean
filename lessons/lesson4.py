import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QGridLayout, QMessageBox

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройки окна
        self.setWindowTitle('Конкурс от Crazy People')
        self.setGeometry(100, 100, 400, 200)

        # Вопрос
        question = QLabel('Как звали первого ютуб-блогера, набравшего 100000000 подписчиков?')

        # Варианты ответа
        self.radio2005 = QRadioButton('PewDiePie ')
        self.radio2010 = QRadioButton('Рэт и Линк')
        self.radio2015 = QRadioButton('SlivkiShow')
        self.radio2020 = QRadioButton('TheBrianMaps')
        self.radio1= QRadioButton('Mister Max')
        self.radio2 = QRadioButton('EeOneGuy')

        # Подключение сигналов к слотам
        self.radio2005.clicked.connect(self.check_answer)
        self.radio2010.clicked.connect(self.check_answer)
        self.radio2015.clicked.connect(self.check_answer)
        self.radio2020.clicked.connect(self.check_answer)
        self.radio1.clicked.connect(self.check_answer)
        self.radio2.clicked.connect(self.check_answer)
        # Макет
        grid = QGridLayout()
        grid.addWidget(question, 0, 0, 1, 2)  # Вопрос занимает две колонки
        grid.addWidget(self.radio2005, 1, 0)
        grid.addWidget(self.radio2010, 1, 1)
        grid.addWidget(self.radio2015, 2, 0)
        grid.addWidget(self.radio2020, 2, 1)
        grid.addWidget(self.radio1, 3, 0)
        grid.addWidget(self.radio2, 3, 1)

        self.setLayout(grid)

    def check_answer(self):
        sender = self.sender()  # Получаем объект, который вызвал сигнал
        if sender == self.radio2005:
            QMessageBox.information(self, 'Результат', 'Вы выиграли встречу с создателями канала!')
        else:
            QMessageBox.information(self, 'Результат', 'Повезёт в другой раз!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())