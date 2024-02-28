from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtCore import QTimer, Signal, QObject, QThread
from ui.left_ui import LeftUI
from ui.temperature_ui import TemperatureUI
from serialcom.temperature import read_temperature, read_sensor_units
from serialcom.connect import find_connected_devices, handle_disconnect, handle_connect, connect_signals

class Worker(QObject):
    finished_signal = Signal()
    start_timers_signal = Signal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def run(self):
        handle_connect(self.main_window)
        self.start_timers_signal.emit()
        self.finished_signal.emit()  # Emit the finished signal when the task is complete

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

        # Connect the buttons
        self.connection_ui.connect_button.clicked.connect(self.handle_connect_button)
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

    def handle_connect_button(self):
        if not self.worker_thread or not self.worker_thread.isRunning():
            # Create new worker and thread
            self.worker = Worker(self)
            self.worker_thread = QThread()
            self.worker.moveToThread(self.worker_thread)
            self.worker.finished_signal.connect(self.handle_worker_finished)  # Connect the finished signal
            self.worker_thread.started.connect(self.worker.run)
            self.worker.start_timers_signal.connect(self.start_timers)
            self.worker_thread.start()

    def handle_worker_finished(self):
        # Perform cleanup when the worker has finished its task
        if self.worker_thread and self.worker_thread.isRunning():
            print("deleting thread")
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None
            self.worker = None
        connect_signals(self)

    def start_timers(self):
        self.temp_timer.start()
        self.sensor_timer.start()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
