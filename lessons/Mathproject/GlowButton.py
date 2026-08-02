from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QRect
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QPushButton
class GlowButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._glow_opacity = 0
        self._glow_color = QColor(255, 255, 255)
        self.glow_animation = QPropertyAnimation(self, b"glow_opacity")
        self.glow_animation.setDuration(200)
        self.press_animation = QPropertyAnimation(self, b"geometry")
        self.press_animation.setDuration(100)
        self.setMouseTracking(True)
    def get_glow_opacity(self):
        return self._glow_opacity
    def set_glow_opacity(self, opacity):
        self._glow_opacity = opacity
        self.update()
    glow_opacity = pyqtProperty(float, get_glow_opacity, set_glow_opacity)
    def enterEvent(self, event):
        self.glow_animation.setStartValue(self._glow_opacity)
        self.glow_animation.setEndValue(0.7)
        self.glow_animation.start()
        super().enterEvent(event)
    def leaveEvent(self, event):
        self.glow_animation.setStartValue(self._glow_opacity)
        self.glow_animation.setEndValue(0)
        self.glow_animation.start()
        super().leaveEvent(event)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press_animation.setStartValue(self.geometry())
            smaller_rect = QRect(
                self.x() + 2,
                self.y() + 2,
                self.width() - 4,
                self.height() - 4
            )
            self.press_animation.setEndValue(smaller_rect)
            self.press_animation.start()
        super().mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press_animation.setStartValue(self.geometry())
            self.press_animation.setEndValue(QRect(
                self.x() - 2,
                self.y() - 2,
                self.width() + 4,
                self.height() + 4
            ))
            self.press_animation.start()
        super().mouseReleaseEvent(event)
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self._glow_opacity > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(QColor(255, 255, 255, int(255 * self._glow_opacity)))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, 8, 8)
            pen2 = QPen(QColor(200, 230, 255, int(100 * self._glow_opacity)))
            pen2.setWidth(2)
            painter.setPen(pen2)
            painter.drawRoundedRect(3, 3, self.width()-6, self.height()-6, 6, 6)