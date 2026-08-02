from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QLabel, QMessageBox
import re
import pygame  
class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
        self.initSound()
    def initUI(self):
        icon_path = 'images/youtube1.ico'
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)
        self.setWindowTitle("Timer")
        self.resize(400, 400)
        self.setStyleSheet(''' 
            QWidget {
                background-color: black;
                font-family: Comic Sans MS;
            }
            QPushButton {
                background-color: green;
            }
            QPushButton:hover {
                background-color: #267333;
            }
            QLabel{
                color:green;
                font-size:30px;
            }
            QLineEdit {
                color: red;
                selection-background-color: green; 
                font-size: 16px;
            }        
''')
        self.lay = QVBoxLayout()
        self.But = QPushButton("Set time")
        self.But.setStyleSheet("border: none;border-radius: 5px;height: 21px;font-size:19px;")
        self.start_pause_btn = QPushButton("Start")
        self.start_pause_btn.setStyleSheet("border: none;border-radius: 5px;height: 21px;font-size:19px;")
        self.start_pause_btn.setEnabled(False)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setStyleSheet("border: none;border-radius: 5px;height: 21px;font-size:19px;")
        self.reset_btn.setEnabled(False) 
        self.Clock = QLabel("00:00:00")
        self.Clock.setStyleSheet("font-size: 50px;")
        self.lay.addWidget(self.Clock, alignment=Qt.AlignCenter)
        self.lay.addWidget(self.But)
        self.lay.addWidget(self.start_pause_btn)
        self.lay.addWidget(self.reset_btn)
        self.setLayout(self.lay)
        self.But.clicked.connect(self.set_timer)
        self.start_pause_btn.clicked.connect(self.toggle_timer)
        self.reset_btn.clicked.connect(self.reset_timer)
    def initTimer(self):
        self.total_seconds = 0  
        self.remaining_seconds = 0  
        self.is_running = False  
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(1000)
    
    def initSound(self):
        pygame.mixer.init()
        self.sound = pygame.mixer.music.load('211.mp3')
    def set_timer(self):
        inputdialog, ok = QInputDialog.getText(self, 'Set timer', 'Enter time: HH:MM:SS')
        if ok and inputdialog.strip():
            if self.is_valid_time_format(inputdialog):
                hours, minutes, seconds = map(int, inputdialog.split(':'))
                self.total_seconds = hours * 3600 + minutes * 60 + seconds
                self.remaining_seconds = self.total_seconds
                self.update_display()
                self.start_pause_btn.setEnabled(True)
                self.reset_btn.setEnabled(True)
                self.start_pause_btn.setText("Start")
                self.is_running = False
            else:
                self.show_time_error()
                self.set_timer()
    
    def toggle_timer(self):
        if not self.is_running:
            self.timer.start()
            self.is_running = True
            self.start_pause_btn.setText("Pause")
        else:
            self.timer.stop()
            self.is_running = False
            self.start_pause_btn.setText("Start")
    
    def reset_timer(self):
        self.timer.stop()
        self.remaining_seconds = self.total_seconds
        self.is_running = False
        self.start_pause_btn.setText("Start")
        self.update_display()
    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            if self.total_seconds > 0:
                remaining_percent = (self.remaining_seconds / self.total_seconds) * 100
                if remaining_percent <= 10 and remaining_percent > 0:
                    self.Clock.setStyleSheet("font-size: 50px; color: yellow;")
        else:
            self.timer.stop()
            self.is_running = False
            self.start_pause_btn.setText("Start")
            self.Clock.setStyleSheet("font-size: 50px; color: red;")
            self.show_time_up_message()
    def update_display(self):
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.Clock.setText(time_str)
    def show_time_up_message(self):
        self.Clock.setStyleSheet("font-size: 50px; color: green;")        
        self.play_sound()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Timer")
        msg.setText("⏰ Время вышло!")
        msg.setInformativeText("Таймер завершил работу")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    def play_sound(self):
        try:
            pygame.mixer.music.play(-1)
        except:
            pass
    
    def is_valid_time_format(self, time_str):
        pattern = r'^\d+:[0-5][0-9]:[0-5][0-9]$'
        return re.match(pattern, time_str) is not None
    def show_time_error(self):
        QMessageBox.critical(
            self, 
            'Ошибка!', 
            '❌ Неверный формат времени!\n\n'
            'Правильный формат: ЧЧ:ММ:СС\n'
            '• Часы: любое число (0, 5, 10, 100...)\n'
            '• Минуты: от 00 до 59\n'
            '• Секунды: от 00 до 59\n\n'
            'Примеры: 05:30:00, 100:00:00, 24:59:59'
        )
    def closeEvent(self, event):
        self.timer.stop()
        pygame.mixer.quit()
        event.accept()
if __name__ == '__main__':
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec_()