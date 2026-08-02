from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.user_data = {}
        self.load_data()
    def initUI(self):
        self.setWindowTitle('Register')
        icon_path = 'images/youtube1.ico'
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)
        self.resize(400, 400)
        self.label = QLabel('Зарегистрируйтесь:', self) 
        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(200, 200, 100, 40)
        self.line_edit.setStyleSheet('font-size: 14px; font-family: Comic Sans MS; background: light grey;')
        self.slow_line = QLineEdit(self)
        self.slow_line.setGeometry(200, 200, 100, 40)
        self.slow_line.setStyleSheet('font-size: 14px; font-family: Comic Sans MS')
        self.n_line = QLineEdit(self)
        self.n_line.setGeometry(200, 140, 100, 40)
        self.n_line.setStyleSheet('font-size: 14px; font-family: Comic Sans MS')
        self.button = QPushButton('Готово', self)
        self.button.setGeometry(210, 200, 200, 40)
        self.button.setStyleSheet('font-size: 25px; font-family: Comic Sans MS; background: green; border: none; border-radius: 8px')
        self.button3 = QPushButton('Да', self)
        self.button3.setGeometry(100, 337, 100, 40)
        self.button3.setStyleSheet('font-size: 25px; font-family: Comic Sans MS; background-color: green; border: none; border-radius: 8px')
        self.button2 = QPushButton('Нет', self)
        self.button2.setGeometry(350, 337, 100, 40)
        self.button2.setStyleSheet('font-size: 25px; font-family: Comic Sans MS; background-color: red; border: none; border-radius: 8px')
        self.button4 = QPushButton('Готово', self)
        self.button4.setGeometry(300, 337, 100, 40)
        self.button4.setStyleSheet('font-size: 25px; font-family: Comic Sans MS; background-color: green; border: none; border-radius: 8px')
        self.button1 = QPushButton('Готово', self)
        self.button1.setGeometry(210, 200, 200, 40)
        self.button1.setStyleSheet('font-size: 25px; font-family: Comic Sans MS; background-color: red; border: none; border-radius: 8px')
        self.lay = QVBoxLayout()
        self.label.setStyleSheet('font-size: 25px; font-family: Comic Sans MS')
        self.line_edit.setPlaceholderText('Вот тут')
        self.slow_line.setPlaceholderText('Тут введи текст')
        self.lay.addWidget(self.label, alignment=Qt.AlignCenter)
        self.lay.addWidget(self.line_edit, alignment=Qt.AlignCenter)
        self.lay.addWidget(self.slow_line, alignment=Qt.AlignCenter)
        self.lay.addWidget(self.n_line, alignment=Qt.AlignCenter)
        self.lay.addWidget(self.button, alignment=Qt.AlignCenter)        
        self.lay.addWidget(self.button1, alignment=Qt.AlignCenter)
        self.slow_line.hide()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.n_line.hide()
        self.setLayout(self.lay)
        self.button.clicked.connect(self.check_user)
    def close_win(self):
        self.close()
    def load_data(self):
        try:
            with open('for_lesson6.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        name, message = line.strip().split(':', 1)
                        self.user_data[name] = message
        except FileNotFoundError:
            pass
    def save_data(self):
        with open('for_lesson6.txt',  'a', encoding='utf-8') as file:
            for name, message in self.user_data.items():
                file.write(f'{name}:{message}\n')
    def update_user_message(self, name):
        self.n_line.show()
        self.button2.hide() 
        self.button3.hide()
        self.button4.show()
        self.n_line.clear()
        self.button4.clicked.connect(lambda: self.save_new_message(name))
    def save_new_message(self, name):
        try:
            new_message = self.n_line.text().strip()
            if new_message:
                self.user_data[name] = new_message
                self.save_update_data()
                self.label.setText(f'Сообщение пользователя {name} обновлено!')
                self.n_line.clear()
                self.n_line.hide()
                self.button4.hide()
            else:
                self.label.setText('Пожалуйста, введите новое сообщение!')
        except Exception as e:
            self.label.setText(f'Произошла ошибка: {str(e)}')

    def save_update_data(self):
        temp_data = {}
        try:
            # Читаем текущие данные из файла
            with open('for_lesson6.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        name, message = line.strip().split(':', 1)
                        temp_data[name] = message
            
            # Обновляем данные в временном словаре
            for name, message in self.user_data.items():
                temp_data[name] = message
            
            # Записываем обновленные данные обратно в файл
            with open('for_lesson6.txt', 'w', encoding='utf-8') as file:
                for name, message in temp_data.items():
                    file.write(f'{name}:{message}\n')
        except IOError as e:
            self.label.setText(f"Ошибка при сохранении данных: {str(e)}")

    def check_user(self):
        name = self.line_edit.text().strip()
        if not name:
            self.label.setText('Пожалуйста, введи свое имя!')
            return
        
        if name in self.user_data:
            self.line_edit.hide()
            self.button.hide()
            self.label.setGeometry(200,200, 10, 10)
            self.label.setText(f'Привет, {name}! Вы писали сообщение: {self.user_data[name]},\n хотите изменить его?')
            
            # Показываем кнопки выбора
            self.button2.show()  # Кнопка "Нет"
            self.button3.show()  # Кнопка "Да"
            
            # Подключаем обработчики
            self.button2.clicked.connect(self.close_win)
            self.button3.clicked.connect(lambda: self.update_user_message(name))
                
        else:
            self.label.setText(f'Вы, {name}, ещё не были в приложении.\n Введите что угодно:')
            self.line_edit.hide()
            self.button.hide()
            self.slow_line.show()
            self.button1.show()
            self.button1.clicked.connect(lambda: self.register_user(name))

    def register_user(self, name):
        try:
            message = self.slow_line.text().strip()
            if not message:
                self.label.setText('Пожалуйста, введите сообщение!')
                return
            
            # Проверяем, не существует ли уже такой пользователь
            if name in self.user_data:
                self.label.setText('Пользователь с таким именем уже существует!')
                return
            
            # Добавляем нового пользователя
            self.user_data[name] = message
            self.save_update_data()  # Используем обновленный метод сохранения
            
            # Обновляем интерфейс
            self.slow_line.hide()
            self.button1.hide()
            self.label.setText(f'Пользователь {name} успешно зарегистрирован!')
            
        except Exception as e:
            self.label.setText(f'Произошла ошибка при регистрации: {str(e)}')

    def close_win(self):
        # Возвращаем интерфейс в исходное состояние
        self.n_line.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.label.setText('Зарегистрируйтесь:')
        self.line_edit.show()
        self.button.show()
        self.line_edit.clear()  # Очищаем поле ввода имени

    # Дополнительно добавим метод очистки всех полей при закрытии
    def clear_fields(self):
        self.line_edit.clear()
        self.slow_line.clear()
        self.n_line.clear()
        self.label.setText('Зарегистрируйтесь:')
        self.line_edit.show()
        self.button.show()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.slow_line.hide()
        self.button1.hide()
        self.n_line.hide()

# Запускаем приложение
if __name__ == '__main__':
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec_()