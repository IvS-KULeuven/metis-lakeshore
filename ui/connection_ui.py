from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox

class ConnectionUI(QWidget):
    def __init__(self):
        super().__init__()
        # Create VBoxlayout for connection part
        self.vlayout = QVBoxLayout()
        
        # Connection label 
        self.connection_label = QLabel("<b>Connection</b>")
        self.connection_label.setStyleSheet("font-size: 14pt;")

        # Status label
        self.status_label = QLabel("<b>Status: </b>        Disconnected")

        # Refresh devices button
        self.refresh_button = QPushButton("Refresh devices")

        # Create HboxLayout for 2 buttons
        self.hbutton_layout = QHBoxLayout()

        # Create buttons
        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconnect")
        
        # Add buttons to hbutton_layout
        self.hbutton_layout.addWidget(self.connect_button)
        self.hbutton_layout.addWidget(self.disconnect_button)

        # Connection combobox
        self.connection_combobox = QComboBox()

        # Create list to store devices in
        self.devices_list = []

        # Add widgets to connection_vlayout
        self.vlayout.addWidget(self.connection_label)
        self.vlayout.addWidget(self.status_label)
        self.vlayout.addWidget(self.refresh_button)
        self.vlayout.addLayout(self.hbutton_layout)
        self.vlayout.addWidget(self.connection_combobox)