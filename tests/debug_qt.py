from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример QTableWidget")
        self.resize(600, 400)

        # Создание таблицы
        self.table = QTableWidget()
        self.table.setRowCount(3)  # Количество строк
        self.table.setColumnCount(3)  # Количество столбцов
        self.table.setHorizontalHeaderLabels(["Имя", "Возраст", "Город"])  # Заголовки столбцов

        # Добавление данных в ячейки
        self.table.setItem(0, 0, QTableWidgetItem("Алиса"))
        self.table.setItem(0, 1, QTableWidgetItem("25"))
        self.table.setItem(0, 2, QTableWidgetItem("Москва"))

        self.table.setItem(1, 0, QTableWidgetItem("Боб"))
        self.table.setItem(1, 1, QTableWidgetItem("30"))
        self.table.setItem(1, 2, QTableWidgetItem("Санкт-Петербург"))

        self.table.setItem(2, 0, QTableWidgetItem("Чарли"))
        self.table.setItem(2, 1, QTableWidgetItem("35"))
        self.table.setItem(2, 2, QTableWidgetItem("Казань"))

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()