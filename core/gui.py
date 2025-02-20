from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from core.data_model import InputData

def GUI_input_show(inputData : InputData):
    app = QApplication([])
    window = GUI_input(inputData)
    window.show()
    app.exec()  
    
    

class GUI_input(QWidget):
    def __init__(self, inputData : InputData):
        super().__init__()
        self.setWindowTitle("Пример QTableWidget")
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
