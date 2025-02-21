from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QGridLayout, QSpinBox
from PyQt6.QtCore import Qt
from core.data_model import InputData, CalenderData
from core.control import CreateDocument
import calendar
from datetime import datetime, timedelta

def GUI_input_show(inputData : InputData):
    app = QApplication([])
    window = GUI_input(inputData, None)
    window.show()
    app.exec()  
    
def GUI_main_window_show():
    app = QApplication([])
    window = GUI_main_window()
    window.show()
    app.exec()      

def GUI_calender_window_show(calenderData : CalenderData):
    app = QApplication([])
    window = GUI_calendar(calenderData)
    window.show()
    app.exec()     

class GUI_calendar(QWidget):
    def __init__(self, calenderData : CalenderData):
        super().__init__()
        self.setWindowTitle("Режим календаря")
        self.resize(400, 200)

        #self.grid = QGridLayout()
        """self.grid.addWidget(QPushButton('Button 1'), 0,0)
        self.grid.addWidget(QPushButton('Button 2'), 1,0)
        self.grid.addWidget(QPushButton('Button 3'), 2,0)
        self.grid.addWidget(QPushButton('Button 4'), 3,0)"""
        self.initUI()


        #self.setLayout(self.grid)
        #self.show()
    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2100)
        self.year_input.setValue(2024)
        
        self.month_input = QSpinBox()
        self.month_input.setRange(1, 12)
        self.month_input.setValue(2)
        
        self.week_input = QSpinBox()
        self.week_input.setRange(1, 53)
        self.week_input.setValue(1)
        
        self.day_input = QSpinBox()
        self.day_input.setRange(0, 6)
        self.day_input.setValue(0)
        
        self.year_input.valueChanged.connect(self.update_calendar)
        self.month_input.valueChanged.connect(self.update_calendar)
        
        self.layout.addWidget(QLabel("Выберите год:"))
        self.layout.addWidget(self.year_input)
        self.layout.addWidget(QLabel("Выберите месяц:"))
        self.layout.addWidget(self.month_input)
        
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)
        
        self.layout.addWidget(QLabel("Выберите номер недели:"))
        self.layout.addWidget(self.week_input)
        self.layout.addWidget(QLabel("Выберите день недели (0 - Пн, 6 - Вс):"))
        self.layout.addWidget(self.day_input)
        
        self.date_label = QLabel("Дата:")
        self.layout.addWidget(self.date_label)
        
        self.week_input.valueChanged.connect(self.get_date_from_week)
        self.day_input.valueChanged.connect(self.get_date_from_week)
        
        self.setLayout(self.layout)
        self.update_calendar()
    
    def update_calendar(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        year = self.year_input.value()
        month = self.month_input.value()
        cal = calendar.monthcalendar(year, month)
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for col, day in enumerate(days):
            self.grid_layout.addWidget(QLabel(day), 0, col)
        
        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    btn = QPushButton(str(day))
                    self.grid_layout.addWidget(btn, row, col)
    
    def get_date_from_week(self):
        year = self.year_input.value()
        week = self.week_input.value()
        day = self.day_input.value()
        
        first_day = datetime(year, 1, 1)
        first_monday = first_day + timedelta(days=(7 - first_day.weekday()) % 7)
        date = first_monday + timedelta(weeks=week-1, days=day)
        
        self.date_label.setText(f"Дата: {date.strftime('%d.%m.%Y')}")

class GUI_main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Утилита audit")
        self.resize(400, 200)
    
        self.path_text = QLineEdit(self)
        self.path_text.setPlaceholderText("Path")
        
        self.button_choose = QPushButton("Browse", self)
        self.button_choose.clicked.connect(self.choose_file)

        self.button_run = QPushButton("Ok", self)
        self.button_run.clicked.connect(self.open_file)
        self.button_run.setFixedWidth(100)

        self.button_show_doc = QPushButton("View", self)
        self.button_show_doc.clicked.connect(self.show_document)
        self.button_show_doc.setFixedWidth(100)

        self.layout_file_path = QHBoxLayout()
        self.layout_file_path.addWidget(self.path_text)
        self.layout_file_path.addWidget(self.button_choose)

        self.layout_all = QVBoxLayout()
        self.layout_all.addLayout(self.layout_file_path)

        self.layout_all_centered = QHBoxLayout()
        self.layout_all_centered.addWidget(self.button_run)
        self.layout_all_centered.addWidget(self.button_show_doc)

        self.layout_all.addLayout(self.layout_all_centered)
        self.layout_all.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout_all)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Файл xlsx (*.xlsx)")
        self.path_text.setText(file_path)
    def open_file(self):        
        self.calender = GUI_calendar()
        self.calender.show()
    def show_document(self):
        path = self.path_text.text()
        if not path:
            return
        data = CreateDocument(path)
        self.run_menue = GUI_input(data, self)
        self.hide()
        self.run_menue.show()

# Получает данные и родительское окно (чтобы восстановить его после закрытия текущего)
class GUI_input(QWidget):
    def __init__(self, inputData : InputData, parent : QWidget):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Отладочный вывод парсинга")
        self.resize(600, 400)

        self.table = QTableWidget()
        self.table.setRowCount(inputData.rowMax)  # Количество строк
        self.table.setColumnCount(inputData.colMax)

        for i_row in range(1,inputData.rowMax):
            for i_col in range(1, inputData.colMax):
                item = QTableWidgetItem(inputData.processed[i_row][i_col])
                self.table.setItem(i_row - 1, i_col - 1, item)\
                
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
    def closeEvent(self, event):
        if self.parent:
            self.parent.show()
        event.accept()
