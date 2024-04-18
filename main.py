from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtCore import QTimer
from ui.left_ui import LeftUI
from ui.temperature_ui import TemperatureUI
from serialcom.temperature import read_temperature, read_sensor_units
from serialcom.connect import find_connected_devices, handle_disconnect, handle_connect
from thread.signal_manager import SignalManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create QHBoxlayout for the application, it will be split into a left and right part
        self.layout = QHBoxLayout(self)

        # Create instances of imported UI's
        self.left_ui = LeftUI()
        self.temperature_ui = TemperatureUI()

        # Add left and right layouts to main layout
        self.layout.addLayout(self.left_ui.layout)
        self.layout.addLayout(self.temperature_ui.vlayout)

        # Access attributes from instances of LeftUI
        self.general_ui = self.left_ui.general_ui
        self.connection_ui = self.left_ui.connection_ui
        self.profibus_ui = self.left_ui.profibus_ui
        self.curve_ui = self.left_ui.curve_ui
        self.sensor_ui = self.left_ui.sensor_ui

        # Create variables to store serial information
        self.port = ''
        self.baudrate = 115200
        self.timeout = 1
        self.ser = ''

        # Initialize worker and thread
        self.worker = None
        self.worker_thread = None

        signal_manager = SignalManager()

        # Connect the signal to a slot for updating the UI
        signal_manager.update_ui_signal.connect(self.update_ui_slot)

        # Connect the buttons
        self.connection_ui.connect_button.clicked.connect(lambda: handle_connect(self, signal_manager))
        self.connection_ui.disconnect_button.clicked.connect(lambda: handle_disconnect(self))
        self.connection_ui.refresh_button.clicked.connect(lambda: find_connected_devices(self))

        # Call the function to search for connected devices
        find_connected_devices(self)

        # Create the timers for reading temperature and sensor units
        self.temp_timer = QTimer(self)
        self.temp_timer.setInterval(10000)  # Update every 10 seconds
        self.temp_timer.timeout.connect(lambda: read_temperature(self))
        self.sensor_timer = QTimer(self)
        self.sensor_timer.setInterval(10000)  # Update every 10 seconds
        self.sensor_timer.timeout.connect(lambda: read_sensor_units(self))

    def update_ui_slot(self, element_str, command, value):
        # Convert the string identifier to the correct UI element reference
        ui_element = self.find_ui_element(element_str)

        # Perform UI update safely
        if command == "setItem":
            row, column, item = value
            getattr(ui_element, command)(row, column, item)
        else:
            getattr(ui_element, command)(value)

    def find_ui_element(self, element_str):
        full_element_str = "self." + element_str
        try:
            return eval(full_element_str)
        except AttributeError:
            print(f"UI element '{full_element_str}' not found.")
            return None



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
