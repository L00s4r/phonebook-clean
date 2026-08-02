import sys
import time
import threading
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QLabel, 
                           QDoubleSpinBox, QComboBox, QSpinBox)
import mouse
import keyboard

class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.clicking = False
        self.click_thread = None
        self.hotkey = 'f6'
        self.initUI()
        self.setup_hotkey()
        
    def initUI(self):
        self.setWindowTitle("Автокликер")
        self.setFixedSize(300, 250)
        
        # Основные настройки
        self.label_interval = QLabel("Интервал (секунды):")
        self.interval_spin = QDoubleSpinBox()  # ← ИСПРАВЛЕНО: используем QDoubleSpinBox
        self.interval_spin.setMinimum(0.01)
        self.interval_spin.setMaximum(10)
        self.interval_spin.setSingleStep(0.1)
        self.interval_spin.setValue(0.1)
        
        self.label_button = QLabel("Кнопка мыши:")
        self.button_combo = QComboBox()
        self.button_combo.addItems(["Левая", "Правая", "Средняя"])
        
        self.label_clicks = QLabel("Количество кликов (0 = бесконечно):")
        self.clicks_spin = QSpinBox()  # Это оставляем QSpinBox, т.к. клики - целые числа
        self.clicks_spin.setMinimum(0)
        self.clicks_spin.setMaximum(10000)
        self.clicks_spin.setValue(0)
        
        # Кнопки управления
        self.start_btn = QPushButton("▶ Старт (F6)")
        self.start_btn.clicked.connect(self.start_clicking)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        
        self.stop_btn = QPushButton("■ Стоп (F7)")
        self.stop_btn.clicked.connect(self.stop_clicking)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        
        self.status_label = QLabel("Статус: Остановлен")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        
        # Компоновка
        layout = QVBoxLayout()
        
        # Добавляем виджеты
        layout.addWidget(self.label_interval)
        layout.addWidget(self.interval_spin)
        layout.addWidget(self.label_button)
        layout.addWidget(self.button_combo)
        layout.addWidget(self.label_clicks)
        layout.addWidget(self.clicks_spin)
        
        # Кнопки в ряд
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)
        
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def setup_hotkey(self):
        """Настройка горячих клавиш"""
        keyboard.add_hotkey('f6', self.start_clicking)
        keyboard.add_hotkey('f7', self.stop_clicking)
        
    def get_mouse_button(self):
        """Получение кода кнопки мыши"""
        button_text = self.button_combo.currentText()
        if button_text == "Левая":
            return 'left'
        elif button_text == "Правая":
            return 'right'
        else:
            return 'middle'
            
    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status_label.setText("Статус: Кликаем...")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            
            # Запускаем клики в отдельном потоке
            self.click_thread = threading.Thread(target=self.click_loop)
            self.click_thread.daemon = True
            self.click_thread.start()
            
    def stop_clicking(self):
        self.clicking = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Статус: Остановлен")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        
    def click_loop(self):
        """Основной цикл кликов"""
        interval = self.interval_spin.value()  # ← ТЕПЕРЬ РАБОТАЕТ: получаем float
        button = self.get_mouse_button()
        max_clicks = self.clicks_spin.value()
        clicks_done = 0
        
        while self.clicking:
            # Делаем клик
            mouse.click(button)
            clicks_done += 1
            
            # Проверяем, достигли ли лимита кликов
            if max_clicks > 0 and clicks_done >= max_clicks:
                self.stop_clicking()
                break
                
            # Ждем указанный интервал
            time.sleep(interval)
            
    def closeEvent(self, event):
        """При закрытии программы останавливаем клики"""
        self.stop_clicking()
        keyboard.unhook_all()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoClicker()
    window.show()
    sys.exit(app.exec_())