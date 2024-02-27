from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFrame, QSizePolicy
from PySide6.QtCore import Qt

class ConnectionUI(QWidget):
    def __init__(self):
        super().__init__()

        # Create VBoxlayout for connection part
        self.vlayout = QVBoxLayout()

        # Frame
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create VBoxlayout for widgets inside the frame
        self.frame_layout = QVBoxLayout()

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

        # Add widgets to frame layout
        self.frame_layout.addWidget(self.status_label)
        self.frame_layout.addWidget(self.refresh_button)
        self.frame_layout.addLayout(self.hbutton_layout)
        self.frame_layout.addWidget(self.connection_combobox)

        # Set frame layout
        self.frame.setLayout(self.frame_layout)

        # Add connection label to main layout
        self.vlayout.addWidget(self.connection_label)

        # Add frame to main layout
        self.vlayout.addWidget(self.frame)

        # Set alignment of the connection_vlayout to the left
        self.vlayout.setAlignment(Qt.AlignLeft)



