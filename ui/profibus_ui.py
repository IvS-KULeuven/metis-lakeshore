from PySide6.QtWidgets import QWidget, QVBoxLayout,QLabel,QComboBox, QFrame, QSizePolicy, QGridLayout, QLineEdit

class ProfibusUI(QWidget):
    def __init__(self):
        super().__init__()
        # Vbox for Profibus part
        self.vlayout = QVBoxLayout()

        # New QLabel for PROFIBUS
        self.profibus_label = QLabel("<b>PROFIBUS communication</b>")
        self.profibus_label.setStyleSheet("font-size: 14pt;")

        # New QFrame for PROFIBUS communication
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Grid layout for PROFIBUS communication
        self.layout = QGridLayout()
        self.frame.setLayout(self.layout)
        self.layout.addWidget(QLabel("<b>Address</b>"), 0, 0)
        self.address_line_edit = QLineEdit()
        self.layout.addWidget(self.address_line_edit, 0, 1)
        self.layout.addWidget(QLabel("<b>Slot Count</b>"), 1, 0)
        self.slot_combobox = QComboBox()
        self.slot_combobox.addItems([str(i) for i in range(1, 9)])
        self.layout.addWidget(self.slot_combobox, 1, 1)

        # Add an empty row
        self.layout.addWidget(QLabel(""), 2, 0)

        # Header labels
        self.layout.addWidget(QLabel("<b>Channel</b>"), 3, 1)
        self.layout.addWidget(QLabel("<b>Units</b>"), 3, 2)

        # Labels for Slot1-8
        for i in range(1, 9):
            self.layout.addWidget(QLabel(f"<b>Slot {i}</b>"), i + 3, 0)

        # Comboboxes for Channel
        self.channel_comboboxes = []
        for i in range(1, 9):
            channel_combobox = QComboBox()
            channel_combobox.addItems([str(j) for j in range(1, 9)])
            self.channel_comboboxes.append(channel_combobox)
            self.layout.addWidget(channel_combobox, i + 3, 1)

        # Comboboxes for Units
        self.units_comboboxes = []
        for i in range(1, 9):
            units_combobox = QComboBox()
            units_combobox.addItems(["Kelvin", "Celsius", "sensor", "Fahrenheit"])
            self.units_comboboxes.append(units_combobox)
            self.layout.addWidget(units_combobox, i + 3, 2)
        
        # Add widgets to vlayout
        self.vlayout.addWidget(self.profibus_label)
        self.vlayout.addWidget(self.frame)