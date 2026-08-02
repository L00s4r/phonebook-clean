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
        question = QLabel('В каком году канал получил "золотую кнопку" от YouTube?')

        # Варианты ответа
        self.radio2005 = QRadioButton('2005')
        self.radio2010 = QRadioButton('2010')
        self.radio2015 = QRadioButton('2015')
        self.radio2020 = QRadioButton('2020')

        # Подключение сигналов к слотам
        self.radio2005.clicked.connect(self.check_answer)
        self.radio2010.clicked.connect(self.check_answer)
        self.radio2015.clicked.connect(self.check_answer)
        self.radio2020.clicked.connect(self.check_answer)

        # Макет
        grid = QGridLayout()
        grid.addWidget(question, 0, 0, 1, 2)  # Вопрос занимает две колонки
        grid.addWidget(self.radio2005, 1, 0)
        grid.addWidget(self.radio2010, 1, 1)
        grid.addWidget(self.radio2015, 2, 0)
        grid.addWidget(self.radio2020, 2, 1)

        self.setLayout(grid)

    def check_answer(self):
        sender = self.sender()  # Получаем объект, который вызвал сигнал
        if sender == self.radio2015:
            QMessageBox.information(self, 'Результат', 'Верно! Вы выиграли гироскутер')
        else:
            QMessageBox.information(self, 'Результат', 'Нет, в 2015 году. Вы выиграли фирменный плакат')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())