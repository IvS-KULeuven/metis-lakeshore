from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QRunnable, QObject

class WorkerSignals(QObject):

    finished_signal = Signal()
    start_timers_signal = Signal()
    update_stylesheet_signal = Signal(QWidget, str)

class Worker(QRunnable):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.signals = WorkerSignals()

    def run(self):
        from serialcom.connect import read_serial
        print("Reading serial information")
        read_serial(self.main_window)
        print("Starting timers")
        self.signals.start_timers_signal.emit()
        print("Finished signal emitting")
        self.signals.finished_signal.emit()
