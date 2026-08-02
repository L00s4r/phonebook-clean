from PyQt5.QtWidgets import * 
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QTimer, QRect, QEasingCurve
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPen
import pyperclip 
from GlowButton import GlowButton

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connect_buttons()
        QTimer.singleShot(100, self.show_animation)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        radius = 20 
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(135, 192, 245))  
        gradient.setColorAt(1.0, QColor(26, 95, 180))   
        painter.fillPath(path, gradient)
        pen = QPen(QColor(0,0,0,100))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, radius, radius)
    def show_animation(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        end_rect = self.geometry()
        start_rect = QRect(
            end_rect.x() + end_rect.width() // 4,
            end_rect.y() - 50,
            end_rect.width() // 2,
            end_rect.height() // 2
        )
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.start()
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('Password Generator')
        self.setFixedSize(500, 450)

        self.password_edit = QLineEdit()
        self.password_edit.setFont(QFont('Comic Sans MS', 14))
        self.button = QPushButton("Check")

        self.minimize_btn = QPushButton("─")
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.clicked.connect(self.showMinimized)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.close)
        
        self.safety_label = QLabel('Safety: -')
        self.strength_label = QLabel('Strength: -')
        self.setStyleSheet('''
            QWidget {
                font-family: Comic Sans MS;
            }
            QLabel {
                color: cyan;
                font-size: 30px;
                background-color: transparent;
            }
            GlowButton {
                background-color: rgba(0, 255, 255, 200);
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: black;
                border: 1px solid rgba(0, 128, 128, 100);
            }
            QLineEdit {
                color: black;
                selection-background-color: cyan;
                font-size: 16px;
                background-color: #06bbc4;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #999;
            }
            QPushButton#close_btn, QPushButton#minimize_btn {
                background-color: rgba(255, 255, 255, 100);
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton#close_btn:hover {
                background-color: rgba(255, 0, 0, 200);
            }
            QPushButton#minimize_btn:hover {
                background-color: rgba(255, 255, 255, 200);
                color: black;
            }
            QMessageBox {
                min-width: 900px;
                font-size: 12px;
                background-color: black;
            }
            QSlider::groove:horizontal {
                border: 1px solid #00ffff;
                height: 6px;
                background: rgba(0, 255, 255, 50);
                border-radius: 4px;
            }
        ''')     
        
        self.minimize_btn.setObjectName("close_btn")
        self.close_btn.setObjectName("close_btn")
        
        main_layout = QVBoxLayout()  
        
        title_layout = QHBoxLayout()
        title_layout.addStretch() 
        title_layout.addWidget(self.minimize_btn)
        title_layout.addWidget(self.close_btn)
        
        content_layout = QVBoxLayout()
        content_layout.addWidget(QLabel('Your password'))
        content_layout.addWidget(self.password_edit)
        content_layout.addWidget(self.button)
        content_layout.addWidget(self.safety_label)
        content_layout.addWidget(self.strength_label)

        main_layout.addLayout(title_layout)  
        main_layout.addLayout(content_layout)  
        
        self.setLayout(main_layout)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def connect_buttons(self):
        self.button.clicked.connect(self.check)
    def check(self):
        self.check_strength(self.password_edit.text())
    def check_strength(self, password1):
        strength = 0 
        length = len(password1)

        if length >= 12:
            strength += 2

        elif length >= 8:
            strength += 1

        else:
            strength -= 1

        has_upper = any(c.isupper() for c in password1)
        if has_upper:
            strength += 1
        else:
            strength -= 1
        
        has_lower = any(c.islower() for c in password1)
        if has_lower:
            strength += 1
        else:
            strength -= 1
        
        has_digits = any(c.isdigit() for c in password1)
        if has_digits:
            strength += 1
        else:
            strength -= 1
        
        special_chars = "!@#$%^&*()_+-=[]{};:,.<>?/\\|~`"
        has_special = any(c in special_chars for c in password1)
        if has_special:
            strength += 2
        else:
            strength -= 1
        
        common_patterns = [
            "password", "123456", "qwerty", "admin", "12345678",
            "123456789", "12345", "1234", "qwerty123", "abc123"
        ]
        if password1.lower() in common_patterns:
            strength -= 2

        if strength >= 7:
            level = "🔒 Very good"
            icon = "💪"
        elif strength >= 5:
            level = "🔐 Good"
            icon = "👍"
        elif strength >= 2:
            level = "⚠️ Mid"
            icon = "⚠️"
        elif strength >= 0:
            level = "❌ Weak"
            icon = "❌"
        else:
            level = "❗ Too weak"
            icon = "❗"
        
        result = f"{icon} {level}"
        self.safety_label.setText(f"Safety: {result}")
        self.strength_label.setText(f"Strength: {strength}/7")
if __name__ == "__main__":
    app = QApplication([])
    window = PasswordGenerator()
    window.show()
    app.exec_()