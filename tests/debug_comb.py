from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import openpyxl
import re

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
        #def isDayOfWeek(str):
        #    if str == "п о н е д е л ь н и к"

        processed = [ [0]*50 for i in range(100)]


        # Избавится от объеденённых ячеек
        def unMergeCells(sheet_obj, processed):
            for i_row in range(1,row):
                for i_col in range(1, col):              
                    cell = sheet_obj.cell(row=i_row, column=i_col)
                    if isinstance(cell, openpyxl.cell.cell.MergedCell):
                        value_merged = getMergedCellVal(sheet_obj, cell)
                        processed[i_row][i_col] = value_merged
                        #print("cell ",i_row, " ", i_col, " ", )                   
                    else:
                        processed[i_row][i_col] = sheet_obj.cell(row =  i_row, column = i_col).value
                    #    print("This cell is not merged.")
        
        unMergeCells(sheet_obj, processed)
        def detectClass(string):
            if "пара" in string:
                return True
            else:
                return False
        def detectTime(string):
            res = re.search("[+-]?([0-9]*[.])?[0-9]+?\/[+-]?([0-9]*[.])?[0-9]+", string)
            if res:
                return True
            else:
                return False

        def groupUpBorders(sheet_obj, processed):
            def check(i_row_parent, i_col_parent, i_row, i_col, sheet_obj, processed):
                def checkAny(cell):
                    if cell.border.top.style != None or \
                       cell.border.bottom.style != None or \
                       cell.border.left.style != None or \
                       cell.border.right.style != None:
                        return True
                    else:
                        return False
                def checkAll(cell):
                    if cell.border.top.style != None and \
                       cell.border.bottom.style != None and \
                       cell.border.left.style != None and \
                       cell.border.right.style != None:
                        return True
                    else:
                        return False
                def checkTop(cell):
                    if cell.border.top.style == None:
                        return True
                    else:
                        return False
                cell = sheet_obj.cell(row=i_row, column=i_col)
                if checkAny(cell):
                    if checkAll(cell) == False:
                        if cell.value != None:
                            if not detectClass(cell.value):
                                if checkTop(cell):
                                    if detectTime(cell.value) == False:
                                        if i_row < 100 and  i_col < 30:
                                            if (i_col - 1) > 1:
                                                check(i_row_parent, i_col_parent, i_row, i_col - 1, sheet_obj, processed)
                            else:
                                pass
                                    
            for i_row in range(1,row):
                for i_col in range(1, col):
                    check(i_row, i_col, i_row, i_col, sheet_obj, processed)

        groupUpBorders(sheet_obj, processed)


        for i_row in range(1,row):
            for i_col in range(1, col):
                item = QTableWidgetItem(processed[i_row][i_col])
                self.table.setItem(i_row - 1, i_col - 1, item)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()