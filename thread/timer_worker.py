from PySide6.QtCore import QObject, QTimer

class TimerWorker(QObject):
    def __init__(self, main_window, signal_manager):
        super().__init__()
        self.main_window = main_window
        self.signal_manager = signal_manager

    def run(self):
        from serialcom.temperature import read_temperature, read_sensor_units
        self.temp_timer = QTimer(self)
        self.temp_timer.setInterval(2000)  # Update every 2 seconds
        self.temp_timer.timeout.connect(lambda: read_temperature(self.main_window, self.signal_manager))
        self.temp_timer.start()

        self.sensor_timer = QTimer(self)
        self.sensor_timer.setInterval(2000)  # Update every 2 seconds
        self.sensor_timer.timeout.connect(lambda: read_sensor_units(self.main_window, self.signal_manager))
        self.sensor_timer.start()
