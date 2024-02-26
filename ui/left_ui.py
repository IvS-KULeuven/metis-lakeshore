from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from ui.general_ui import GeneralUI
from ui.connection_ui import ConnectionUI
from ui.profibus_ui import ProfibusUI
from ui.curve_ui import CurveUI
from ui.sensor_ui import SensorUI

class LeftUI(QWidget):
    def __init__(self):
        super().__init__()
        # Create QVBoxlayout for left part for lakeshore readings
        self.layout = QVBoxLayout()

        # Create instances of imported UI's
        self.general_ui = GeneralUI()
        self.connection_ui = ConnectionUI()
        self.profibus_ui = ProfibusUI()
        self.curve_ui = CurveUI()
        self.sensor_ui = SensorUI()

        # Create QHBoxlayout for general and connection part
        self.h1layout = QHBoxLayout()

        # Add general_vlayout and connection_vlayout to left_hlayout
        self.h1layout.addLayout(self.general_ui.vlayout)
        self.h1layout.addLayout(self.connection_ui.vlayout)
        
        # Create QHBoxlayout for Profibus and Curve part
        self.h2layout = QHBoxLayout()

        # Add profibus and curve layouts to left_h2layout
        self.h2layout.addLayout(self.profibus_ui.vlayout)
        self.h2layout.addLayout(self.curve_ui.vlayout)

        # Add sections to left layout
        self.layout.addLayout(self.h1layout)
        self.layout.addLayout(self.h2layout)
        self.layout.addWidget(self.sensor_ui.title_label)
        self.layout.addWidget(self.sensor_ui.frame)
