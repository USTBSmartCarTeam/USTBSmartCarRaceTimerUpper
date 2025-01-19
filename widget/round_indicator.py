from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class RoundIndicator(QWidget):
    def __init__(self, color="red", size=20, margin=1, parent=None):
        super().__init__(parent)
        self._color = QColor(color)  # 设置默认颜色
        self.setFixedSize(size, size)  # 设置控件固定大小
        self.margin = margin  # 设置间隙

    def setColor(self, color):
        self._color = QColor(color)
        self.update()  # 重绘控件

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 开启抗锯齿
        painter.setBrush(self._color)  # 设置填充颜色
        painter.setPen(Qt.PenStyle.NoPen)  # 无边框

        # 确保圆形在控件中间并且留有间隙
        diameter = min(self.width(), self.height()) - 2 * self.margin  # 减去间隙
        rect = QRect(self.margin, self.margin, diameter, diameter)  # 绘制区域
        rect.moveCenter(self.rect().center())  # 确保圆形居中

        painter.drawEllipse(rect)  # 绘制圆形


