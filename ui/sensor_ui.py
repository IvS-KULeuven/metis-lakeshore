from PySide6.QtWidgets import QWidget, QVBoxLayout,QLabel,QComboBox, QFrame, QSizePolicy, QGridLayout, QLineEdit

class SensorUI(QWidget):
    def __init__(self):
        super().__init__()
        # Sensor setup section
        self.title_label = QLabel("<b>Sensor setup</b>")
        self.title_label.setStyleSheet("font-size: 14pt;")

        # New QFrame for sensor section
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Grid layout for sensor section
        self.layout = QGridLayout()
        self.frame.setLayout(self.layout)

        # Labels for sensor section
        header_labels = ["Power", "Name", "Type", "Current Reversal", "Autorange", "Range", "Display Units"]

        # Add labels to sensor grid layout
        for col, label in enumerate(header_labels):
            self.layout.addWidget(QLabel(f"<b>{label}</b>"), 0, col)

        # Add QComboBox for Power (On/Off)
        power_options = ["Off", "On"]
        self.power_comboboxes = []
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(power_options)
            self.layout.addWidget(combo_box, row, 0)
            self.power_comboboxes.append(combo_box)

        # Add QLineEdit for Name
        self.name_line_edits = []
        for row in range(1, 9):
            line_edit = QLineEdit()
            self.layout.addWidget(line_edit, row, 1)
            self.name_line_edits.append(line_edit)

        # Add QComboBox for Type
        sensor_types = ["Diode", "Platinum RTD", "NTC RTD"]
        self.type_comboboxes = []  # Store the combo boxes in a list to access them later if needed
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(sensor_types)
            self.layout.addWidget(combo_box, row, 2)
            self.type_comboboxes.append(combo_box)

        # Add QComboBox for Current Reversal
        on_off_values = ["Off", "On"]
        self.current_reversal_comboboxes = []
        for row in range(1, 9):
                combo_box = QComboBox()
                combo_box.addItems(on_off_values)
                self.current_reversal_comboboxes.append(combo_box)
                self.layout.addWidget(combo_box, row, 3)

        # Add QComboBox for Autorange
        on_off_values = ["Off", "On"]
        self.autorange_comboboxes = []
        for row in range(1, 9):
                combo_box = QComboBox()
                combo_box.addItems(on_off_values)
                self.autorange_comboboxes.append(combo_box)
                self.layout.addWidget(combo_box, row, 4)

        # Add comboboxes for Range
        range_values = ["7.5 V (10 µA)", "1 kΩ (1 mA)", "10 Ω (1 mA)", "30 Ω (300 µA)", "100 Ω (100 µA)", "300 Ω (30 µA)",
                        "1 kΩ (10 µA)", "3 kΩ (3 µA)", "10 kΩ (1 µA)", "30 kΩ (300 nA)", "100 kΩ (100 nA)"]
        self.range_comboboxes = []
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(range_values)
            self.range_comboboxes.append(combo_box)
            self.layout.addWidget(combo_box, row, 5)
            
        # Add comboboxes for Display Units
        display_units = ["Kelvin", "Celsius", "Sensor", "Fahrenheit"]
        self.display_units_comboboxes = []
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(display_units)
            self.display_units_comboboxes.append(combo_box)
            self.layout.addWidget(combo_box, row, 6)