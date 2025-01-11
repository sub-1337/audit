from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import openpyxl


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        path = "D:\\git\\audit\\data\\1kurs.xlsx"

        # To open the workbook 
        # workbook object is created
        wb_obj = openpyxl.load_workbook(path)

        # Get workbook active sheet object
        # from the active attribute
        sheet_obj = wb_obj.active

        row = 100
        col = 25

        self.setWindowTitle("Пример QTableWidget")
        self.resize(600, 400)

        # Создание таблицы
        self.table = QTableWidget()
        self.table.setRowCount(row)  # Количество строк
        self.table.setColumnCount(col)  # Количество столбцов
        #self.table.setHorizontalHeaderLabels(["Имя", "Возраст", "Город"])  # Заголовки столбцов

        def getMergedCellVal(sheet, cell):
            rng = [s for s in sheet.merged_cells.ranges if cell.coordinate in s]
            return sheet.cell(rng[0].min_row, rng[0].min_col).value if len(rng)!=0 else cell.value

        # Добавление данных в ячейки
        for i_row in range(1,row):
            for i_col in range(1, col):
                value = sheet_obj.cell(row =  i_row, column = i_col).value
                item = QTableWidgetItem(value)
                
                cell = sheet_obj.cell(row=i_row, column=i_col)
                if isinstance(cell, openpyxl.cell.cell.MergedCell):
                    value_merged = getMergedCellVal(sheet_obj, cell)
                    print("cell ",i_row, " ", i_col, " ", )                   
                #else:
                #    print("This cell is not merged.")

                self.table.setItem(i_row - 1, i_col - 1, item)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()