from requests import get
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit
import json
class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        icon_path = 'images/youtube1.ico'
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)
        self.setWindowTitle("Weather app")
        self.resize(500, 600)
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Введите город (например: Moscow)")
        self.btn = QPushButton("Узнать погоду")
        self.btn.clicked.connect(self.get_weather)
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Город:"))
        layout.addWidget(self.city_input)
        layout.addWidget(self.btn)
        layout.addWidget(self.result)
        self.setLayout(layout)
    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.result.setText("Введите город")
            return
        try:
            url = f"https://wttr.in/{city}?format=%t+%c+%w+%h"
            response = get(url, timeout=5)
            if response.status_code == 200 and response.text.strip():
                text = response.text.strip()
                self.result.setText(f"Погода в {city}:\n{text}")
            else:
                self.result.setText("Город не найден или ошибка сети")
        except Exception as e:
            self.result.setText(f"Ошибка: {e}")
if __name__ == '__main__':
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec_()