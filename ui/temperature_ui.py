from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView

class TemperatureUI(QWidget):
    def __init__(self):
        super().__init__()
        # Layout for temperature table
        self.vlayout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(8)
        self.table.setHorizontalHeaderLabels(["Name", "Temperature", "Sensor units", "Excitation", "Power"])

        # Populate table with sample data
        for row in range(8):
            self.table.setItem(row, 0, QTableWidgetItem(""))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))
            self.table.setItem(row, 3, QTableWidgetItem(""))
            self.table.setItem(row, 4, QTableWidgetItem(""))

        # Set size policy to expand vertically
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set vertical header to resize to contents
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Add table to vlayout
        self.vlayout.addWidget(self.table)