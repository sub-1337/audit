from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QStyledItemDelegate
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import QRect, Qt

class BorderDelegate(QStyledItemDelegate):
    def __init__(self, row, column, color, parent=None):
        super().__init__(parent)
        self.row = row
        self.column = column
        self.color = color

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if index.row() == self.row and index.column() == self.column:
            pen = QPen(self.color, 2)
            painter.setPen(pen)
            rect = QRect(option.rect)
            rect.adjust(1, 1, -1, -1)  # Сужаем границу
            painter.drawRect(rect)

if __name__ == "__main__":
    import sys
    from PyQt6.QtGui import QColor

    app = QApplication(sys.argv)

    table = QTableWidget(5, 5)
    table.setWindowTitle("Пример бордера для ячейки")
    table.setGeometry(300, 100, 500, 400)

    # Заполняем таблицу
    for row in range(5):
        for col in range(5):
            table.setItem(row, col, QTableWidgetItem(f"({row}, {col})"))

    # Устанавливаем делегат для рисования бордера
    delegate = BorderDelegate(row=2, column=2, color=QColor("red"), parent=table)
    table.setItemDelegate(delegate)

    table.show()
    sys.exit(app.exec())