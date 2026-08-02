from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel
class message_window(QWidget):
    def __init__(self, title, text):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

        icon_path = 'images/icon_for_per.ico'
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)
        self.resize(500, 580)
        self.text = text
        title = title
        self.flame = 0
        self.buttons_layout = QHBoxLayout()
        self.label_title = QLabel(title)
        self.buttons_layout.addWidget(self.label_title, alignment=Qt.AlignLeft)
        self.minimize_btn = QPushButton("─")
        self.minimize_btn.setFixedSize(30, 30)
        self.buttons_layout.addWidget(self.minimize_btn)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.buttons_layout.addWidget(self.close_btn)
        self.close_btn.clicked.connect(self.close)
        self.text_edit = QTextEdit(self)
        self.text_edit.setText(self.text)
        self.text_edit.setReadOnly(True)
        self.setStyleSheet('''
            QWidget {
                font-family: Comic Sans MS;
                background-color: #fff2d1;
            }
            QLabel{
                color: black;
                font-size: 15px;
                background-color: transparent;
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
            QTextEdit{
                background-color: #fcf2d7;
                color: black;
                font-size: 18px;
            }
        ''')     
        self.minimize_btn.setObjectName("minimize_btn")
        self.close_btn.setObjectName("close_btn")
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 10, 20, 20) 
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addWidget(self.text_edit)
        self.setLayout(self.main_layout)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
if __name__ == '__main__':
    app = QApplication([])
    window = message_window(".", ".")
    window.show()
    app.exec_()