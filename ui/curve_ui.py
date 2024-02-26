from PySide6.QtWidgets import QWidget, QVBoxLayout,QLabel,QComboBox, QFrame, QSizePolicy, QGridLayout, QLineEdit, QPushButton

class CurveUI(QWidget):
    def __init__(self):
        super().__init__()
        # Vbox for Curve part
        self.vlayout = QVBoxLayout()

        # Label for curve setup
        self.curve_label = QLabel("<b>Curve setup</b>")
        self.curve_label.setStyleSheet("font-size: 14pt;")

        # New QFrame for curve section
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Grid layout for curve section
        self.layout = QGridLayout()
        self.frame.setLayout(self.layout)

        # Add labels for curve section
        self.layout.addWidget(QLabel("<b>Name</b>"), 0, 0)
        self.layout.addWidget(QLabel("<b>Curve</b>"), 0, 1)

        # Add QLine_edit for Name
        self.name_labels = []
        for row in range(1, 9):
            label = QLineEdit("")
            self.layout.addWidget(label, row, 0)
            self.name_labels.append(label)

        # Add rows for curve section
        self.curve_comboboxes = []
        for i in range(1, 9):
            combobox = QComboBox()
            combobox.addItems(["LSCI DT-600", "LSCI DT-400", "LSCI PT-100", "IEC PT100 RTD", "IEC PT1000 RTD", "Simulated Sensor-NTC"])
            self.curve_comboboxes.append(combobox)
            self.layout.addWidget(combobox, i, 1)
        
        # Delete buttons for curves
        self.delete_buttons = []
        for i in range(1, 9):
            button = QPushButton("DEL")
            self.delete_buttons.append(button)
            self.layout.addWidget(button, i, 2)

        
        # Add widgets to vlayout
        self.vlayout.addWidget(self.curve_label)
        self.vlayout.addWidget(self.frame)