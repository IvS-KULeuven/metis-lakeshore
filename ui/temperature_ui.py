from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

class TemperatureUI(QWidget):
    def __init__(self):
        super().__init__()

        # Vbox for Temperature part
        self.vlayout = QVBoxLayout()

        # Label for temperature setup
        self.temperature_label = QLabel("<b>Temperature readings</b>")
        self.temperature_label.setStyleSheet("font-size: 14pt;")

        # New QFrame for temperature section
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Grid layout for temperature section
        self.layout = QGridLayout()
        self.frame.setLayout(self.layout)

        # Add QTableWidget for temperature data
        self.table = QTableWidget(8, 5)
        self.table.setHorizontalHeaderLabels(["Name", "Temperature", "Sensor units", "Excitation", "Power"])
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Set fixed size of the table in pixels
        self.table.setFixedSize(540, 240)

        # Add table to layout
        self.layout.addWidget(self.table, 1, 0, 8, 5)

        # Set alignment of the general_vlayout to the left
        self.vlayout.setAlignment(Qt.AlignTop)

        # Add widgets to vlayout
        self.vlayout.addWidget(self.temperature_label)
        self.vlayout.addWidget(self.frame)
