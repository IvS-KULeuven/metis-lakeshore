from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout, QPushButton, QLineEdit, QComboBox
from PySide6.QtCore import Qt

class GeneralUI(QWidget):
    def __init__(self):
        super().__init__()

        # Create VBoxlayout for general part
        self.vlayout = QVBoxLayout()
        
        # General section frame
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # General section grid layout
        self.layout = QGridLayout(self.frame)

        # General label 
        self.general_label = QLabel("<b>General</b>")
        self.general_label.setStyleSheet("font-size: 14pt;")

        # Restore factory settings button
        self.restore_button = QPushButton("Restore factory settings")

        # Labels for general information
        self.module_name_label = QLineEdit()
        self.serial_number_label = QLabel()
        self.firmware_version_label = QLabel()
        self.brightness_combobox = QComboBox()
        self.brightness_combobox.addItems(["Off", "Low", "Medium", "High", "Max"])

        # Add labels to general grid layout
        self.layout.addWidget(QLabel("<b>Name</b>"), 0, 0)
        self.layout.addWidget(self.module_name_label, 0, 1)
        self.layout.addWidget(QLabel("<b>Serial Number</b>"), 1, 0)
        self.layout.addWidget(self.serial_number_label, 1, 1)
        self.layout.addWidget(QLabel("<b>Firmware Version</b>"), 2, 0)
        self.layout.addWidget(self.firmware_version_label, 2, 1)
        self.layout.addWidget(QLabel("<b>Screen Brightness</b>"), 3, 0)
        self.layout.addWidget(self.brightness_combobox, 3, 1)
        self.layout.addWidget(self.restore_button, 4, 0, 1, 2)
        
        # Add widgets to general_vlayout
        self.vlayout.addWidget(self.general_label)
        self.vlayout.addWidget(self.frame)
        
        # Set alignment of the general_vlayout to the left
        self.vlayout.setAlignment(Qt.AlignLeft)