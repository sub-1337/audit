from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt
from core.data_model import InputData

def GUI_input_show(inputData : InputData):
    app = QApplication([])
    window = GUI_input(inputData)
    window.show()
    app.exec()  
    
def GUI_main_window_show():
    app = QApplication([])
    window = GUI_main_window()
    window.show()
    app.exec()      

class GUI_main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Утилита audit")
        self.resize(400, 300)
    
        self.path_text = QLineEdit(self)
        self.path_text.setPlaceholderText("Path")
        
        self.button_choose = QPushButton("Browse", self)
        self.button_choose.clicked.connect(self.choose_file)

        self.button_run = QPushButton("Ok", self)
        self.button_run.setFixedWidth(100)

        self.layout_file_path = QHBoxLayout()
        self.layout_file_path.addWidget(self.path_text)
        self.layout_file_path.addWidget(self.button_choose)

        self.layout_all = QVBoxLayout()
        self.layout_all.addLayout(self.layout_file_path)
        
        self.layout_all_centered = QHBoxLayout()
        self.layout_all_centered.addWidget(self.button_run)

        self.layout_all.addLayout(self.layout_all_centered)
        self.layout_all.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout_all)
    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Файл xlsx (*.xlsx)")
        self.path_text.setText(file_path)
        pass

class GUI_input(QWidget):
    def __init__(self, inputData : InputData):
        super().__init__()
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
