from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QCalendarWidget, QSpacerItem
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QGridLayout, QSpinBox, QComboBox, QMessageBox
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QDate
from core.data_model import InputData
import core.data_model as dm
#from core.control import ReadDocument
import calendar
from datetime import datetime, timedelta
from functools import partial
from core.document_reader import DocumentReader

def GUI_main_window_show():
    app = QApplication([])
    window = GUI_main_window()
    window.show()
    app.exec()  

class GUI_rule(QWidget):
    """
    Просмотр правила (не используется)
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Правило')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

class GUI_rules(QWidget):
    """
    Окно с правилами
    """
    def __init__(self, rules : dm.Rules):
        super().__init__()
        self.setWindowTitle('Правила расписания')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        rowCount = len(rules.rules)
        columnCoun = 1

        self.table = QTableWidget()
        self.table.setRowCount(rowCount)
        self.table.setColumnCount(columnCoun)
        for i in range(len(rules.rules)):
            cell = QTableWidgetItem(str(rules.rules[i]))
            self.table.setItem(0, i, cell)
        
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

class GUI_day(QWidget):
    """
    Просмотр дня
    """
    def __init__(self, calender : dm.CalenderYear, currentDay):
        super().__init__()
        self.setWindowTitle('Расписание на день')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        day: dm.CalenderDay = calender.getDay(currentDay)
        if day is None:
            self.noData = True
        else:
            self.noData = False
        
        if not self.noData:
            #day.CalcArrayByAudirory()
            auditorArr = day.ReturnArrayByAuditory()
            
            rowCount = len(auditorArr)
            columnCoun = 7
            if len(auditorArr) == 0:
                self.setNoData()
                return
            assert(len(auditorArr[0]) == columnCoun)

            # Create a table

            self.table = QTableWidget()
            self.table.setRowCount(rowCount)    # 3 rows
            self.table.setColumnCount(columnCoun) # 3 columns
            self.table.setHorizontalHeaderLabels(['Аудитория', 'Пара 1', 'Пара 2', 'Пара 3', 'Пара 4', 'Пара 5', 'Пара 6'])
            def GetCell(block : dm.CalenderBlock):
                return f"{block.comment}\n{block.group}"
            for row_i in range(rowCount):
                for col_j in range(columnCoun):
                    cell = None
                    if isinstance(auditorArr[row_i][col_j], dm.CalenderBlock):
                        cell = QTableWidgetItem(GetCell(auditorArr[row_i][col_j]))
                    else:
                        cell = QTableWidgetItem(str(auditorArr[row_i][col_j]))
                    if isinstance(auditorArr[row_i][col_j], dm.CalenderBlock):
                        if len(auditorArr[row_i][col_j].overlapWith) > 0:
                            cell.setForeground(QColor('red'))
                    cell.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 
                    self.table.setItem(row_i, col_j, cell)                    
            
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
            # Set layout
            layout = QVBoxLayout()
            layout.addWidget(self.table)
            self.setLayout(layout)
        else:
            self.setNoData()
            
    def setNoData(self):
        self.noDataText = QLabel("Нет данных за этот период")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.noDataText)
        self.setLayout(self.layout)
    def initUI(self):
        pass

class GUI_auditories(QWidget):
    """
    Список аудиторий
    """

    def __init__(self, auditories : dm.AllAuditories):
        super().__init__()
        self.setWindowTitle("Список аудиторий")
        self.resize(400, 200)

class GUI_calendar(QWidget):
    """
    Календарь
    """
    
    def __init__(self, dataYear : dm.CalenderYear, startDate):
        super().__init__()        
        self.dataYear = dataYear
        self.dateOfStartDic = startDate
        self.setWindowTitle("Режим календаря")
        self.resize(400, 200)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()        

        # Год
        self.yearInput = QSpinBox()
        self.yearInput.setRange(1900, 2100)
        self.yearInput.setValue(2025)
        
        # Месяц
        self.monthInput = QSpinBox()
        self.monthInput.setRange(1, 12)
        self.monthInput.setValue(9)

        # Месяц - выпадающий список
        self.monthName = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.monthNameBox = QComboBox()
        self.monthNameBox.addItems(self.monthName)

        # Дата - начало надпись
        startDate = self.dateOfStartDic
        self.startDateLabel = QLabel(f"Дата начала: {startDate['day']:02}.{startDate['month']:02}.{startDate['year']}")
        
        # Номер недели
        self.weekInput = QSpinBox()
        self.weekInput.setRange(0, 53)
        self.weekInput.setValue(0)
        
        # День недели - выпадающий список
        self.weekDayName = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        self.weekDayNameBox = QComboBox()
        self.weekDayNameBox.addItems(self.weekDayName)

        # День недели
        self.dayInput = QSpinBox()
        self.dayInput.setRange(0, 6)
        self.dayInput.setValue(0)

        # День - переход по дню недели
        self.dayWeekButton = QPushButton("[перейти]")
        
        self.yearInput.valueChanged.connect(self.update_calendar)
        self.monthInput.valueChanged.connect(self.update_calendar)
        self.monthNameBox.currentIndexChanged.connect(self.updateMonthBox)         

        self.yearAndMonthLayout = QHBoxLayout()

        # Год
        self.yearLayout = QHBoxLayout()
        self.yearLayout.addWidget(QLabel("Выберите год:"))
        self.yearLayout.addWidget(self.yearInput)
        self.yearLayout.addStretch()
        self.yearAndMonthLayout.addLayout(self.yearLayout)
        #self.layout.addLayout(self.yearLayout)

        # Месяц
        self.monthLayout = QHBoxLayout()
        self.monthLayout.addWidget(QLabel("Выберите месяц:"))
        self.monthLayout.addWidget(self.monthNameBox)
        self.monthLayout.addWidget(self.monthInput)
        self.monthLayout.addStretch()
        self.yearAndMonthLayout.addLayout(self.monthLayout)
        #self.layout.addLayout(self.monthLayout)

        self.layout.addLayout(self.yearAndMonthLayout)

        # Дни таблицей
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)
            
        # Дата начала
        self.layout.addWidget(self.startDateLabel) 

        self.weekDayLayout = QHBoxLayout()       
        self.weekDayLayout.addWidget(QLabel("Номер недели:"))
        self.weekDayLayout.addWidget(self.weekInput)
        
        self.weekDayLayout.addWidget(QLabel("День недели:"))
        self.weekDayLayout.addWidget(self.weekDayNameBox)
        self.weekDayLayout.addWidget(self.dayInput)
        self.layout.addLayout(self.weekDayLayout)
        
        self.layout.addWidget(self.dayWeekButton)

        self.weekDayNameBox.currentIndexChanged.connect(self.updateWeekNameBox)     
        self.weekInput.valueChanged.connect(self.get_date_from_week)
        self.dayInput.valueChanged.connect(self.get_date_from_week)
        
        self.setLayout(self.layout)
        self.update_calendar()
        self.get_date_from_week()
    
    def updateWeekNameBox(self):
        self.dayInput.setValue(self.weekDayNameBox.currentIndex())
    def updateMonthBox(self):
        self.monthInput.setValue(self.monthNameBox.currentIndex() + 1)
    def update_calendar(self):
        for i in reversed(range(self.grid_layout.count())):
            # Костыл чтобы не падало из-за плейсхолдера
            try:
                self.grid_layout.itemAt(i).widget().setParent(None)
            except:
                pass
        
        year = self.yearInput.value()
        month = self.monthInput.value()
        cal = calendar.monthcalendar(year, month)        
        
        assert (month - 1) < len(self.monthName)
        self.monthNameBox.setCurrentText(self.monthName[month - 1])

        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for col, day in enumerate(days):
            self.grid_layout.addWidget(QLabel(day), 0, col)
        
        # Добавить плейсхолдер чтобы размер грида был одинаков
        sizeVertical = 60
        sizeHorizontal = 50
        spacerItem = QSpacerItem(sizeVertical, sizeHorizontal)

        self.grid_layout.addItem(spacerItem, 0, 0)
        self.grid_layout.addItem(spacerItem, 6, 0)

        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    btn = QPushButton(str(day))
                    btn.setFixedSize(sizeVertical, sizeHorizontal)
                    btn.clicked.connect(partial(self.click_day_button, day))
                    self.grid_layout.addWidget(btn, row, col)
    
    def click_day_button(self, day):
        year = self.yearInput.value()
        month = self.monthInput.value()        
        self.callDay({'year' : year, 'month' : month , 'day' : day})
    def callDay(self, fullDay):
        self.day_widget = GUI_day(self.dataYear, fullDay)
        self.day_widget.show()
    def get_date_from_week(self):
        week = self.weekInput.value()
        day = self.dayInput.value()
        
        first_day = datetime(self.dateOfStartDic['year'], self.dateOfStartDic['month'], self.dateOfStartDic['day'])
        first_monday = first_day + timedelta(days=(7 - first_day.weekday()) % 7)
        date = first_monday + timedelta(weeks=week-1, days=day)
        
        self.dayWeekButton.setText(f"Дата: {date.strftime('%d.%m.%Y')}")
        self.dayWeekButton.clicked.connect(lambda: self.callDay({'year' : date.year, 'month' :  date.month , 'day' :  date.day}))

        assert 0 <= self.dayInput.value()
        assert self.dayInput.value() < len(self.weekDayName)
        self.weekDayNameBox.setCurrentText(self.weekDayName[self.dayInput.value()])

class GUI_main_window(QWidget):
    """
    Главное окно
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Утилита audit")
        self.resize(400, 200)

        self.dateOfStartDic = None

        self.calendar = QCalendarWidget(self)
        self.label_calender = QLabel("Выберите дату начала занятий", self)

        self.comboSheet = QComboBox()
        self.comboSheet.currentIndexChanged.connect(self.comboSheetChanged)

        self.path_text = QLineEdit(self)
        self.path_text.setPlaceholderText("Path")
        
        self.button_choose = QPushButton("Browse", self)
        self.button_choose.clicked.connect(self.choose_file)

        self.button_run = QPushButton("Ok", self)
        self.button_run.clicked.connect(self.open_file)
        self.button_run.setDisabled(True) 
        self.button_run.setFixedWidth(100)

        self.button_show_doc = QPushButton("View", self)
        self.button_show_doc.clicked.connect(self.show_document)
        self.button_show_doc.setDisabled(True)
        self.button_show_doc.setFixedWidth(100)

        self.layout_file_path = QHBoxLayout()
        self.layout_file_path.addWidget(self.path_text)
        self.layout_file_path.addWidget(self.button_choose)
        self.layout_file_path.addWidget(self.comboSheet)
        
        self.layout_date = QVBoxLayout()        
        self.layout_date.addWidget(self.label_calender)
        self.layout_date.addWidget(self.calendar)

        self.calendar.clicked.connect(self.dateSelected)

        self.layout_all = QVBoxLayout()
        self.layout_all.addLayout(self.layout_file_path)
        self.layout_all.addLayout(self.layout_date)

        self.layout_all_centered = QHBoxLayout()
        self.layout_all_centered.addWidget(self.button_run)
        self.layout_all_centered.addWidget(self.button_show_doc)

        self.layout_all.addLayout(self.layout_all_centered)
        self.layout_all.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout_all)

        self.document = None
    def comboSheetChanged(self, var):
        self.document.worbookNamesCurrent = self.comboSheet.currentText()
        #self.readDoc()
    def dateSelected(self, date : QDate):
        self.dateOfStartDic = {'year' : date.year(), 'month' : date.month(), 'day' : date.day()}
        #self.readDoc()
    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Файл xlsx (*.xlsx)")
        self.path_text.setText(file_path)
        self.readHeadOfDoc()

        self.comboSheet.clear()
        if self.document.worbookNames:
            self.comboSheet.addItems(self.document.worbookNames)

        self.button_run.setDisabled(False)
        self.button_show_doc.setDisabled(False)
    def open_file(self):
        if self.readDoc():
            self.calender = GUI_calendar(self.document.dataYear, self.dateOfStartDic)
            self.calender.show()
            self.auditoryList = GUI_auditories(self.document.allAuditories)
            self.auditoryList.show()
    def show_document(self):
        if self.readDoc() == False:
            return
        self.run_menue = GUI_input(self.document.data)
        self.run_menue.show()
        self.rulesMenue = GUI_rules(self.document.getRules())
        self.rulesMenue.show()
    def readHeadOfDoc(self):
        path = self.path_text.text()
        if not path:
            return
        self.document = DocumentReader(path)
    def readDoc(self):
        if self.dateOfStartDic:
            self.document.readDoc(self.dateOfStartDic)
            return True
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Ошибка")
            msg.setText("Установите дату начала")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return False

class GUI_input(QWidget):
    """
    Отладочный вывод таблицы
    """
    def __init__(self, inputData : InputData):
        super().__init__()
        #self.parent = parent
        self.setWindowTitle("Отладочный вывод парсинга")
        self.resize(600, 400)

        self.table = QTableWidget()
        self.table.setRowCount(inputData.rowMax)  # Количество строк
        self.table.setColumnCount(inputData.colMax)

        for i_row in range(1,inputData.rowMax):
            for i_col in range(1, inputData.colMax):
                #if i_row < len(inputData.processed) and i_col < len(inputData.processed[i_row]):
                if inputData.processed[i_row][i_col]:
                    item = QTableWidgetItem(inputData.processed[i_row][i_col])
                else:
                    item = QTableWidgetItem("")
                self.table.setItem(i_row - 1, i_col - 1, item)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 

        
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
    def closeEvent(self, event):
        #if self.parent:
        #    self.parent.show()
        event.accept()
