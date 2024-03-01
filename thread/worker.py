from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QObject

class Worker(QObject):
    finished_signal = Signal()
    start_timers_signal = Signal()
    update_stylesheet_signal = Signal(QWidget, str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def run(self):
        from serialcom.connect import read_serial
        read_serial(self.main_window)
        self.start_timers_signal.emit()
        self.finished_signal.emit()
