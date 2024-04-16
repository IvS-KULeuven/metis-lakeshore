from PySide6.QtCore import QObject, Signal

class SignalManager(QObject):
    # Define a signal with arguments for UI update
    update_ui_signal = Signal(str, str, str)

    def update_ui(self, element_str, command, value):
        # Emit the signal with the arguments
        self.update_ui_signal.emit(element_str, command, value)
