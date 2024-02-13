import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QTimer
import serial

class TemperatureWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Set number of columns
        self.table_widget.setRowCount(8)     # Set number of rows

        # Set column headers
        self.table_widget.setHorizontalHeaderLabels(["Name", "Temperature"])

        # Populate table with sample data
        for row in range(8):
            self.table_widget.setItem(row, 0, QTableWidgetItem(""))  # Set item in first column
            self.table_widget.setItem(row, 1, QTableWidgetItem("0"))  # Set item in second column

        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # Update every second
        self.timer.timeout.connect(self.read_temperature)
        self.timer.start()

        # Configure serial port settings
        self.port = '/dev/ttyUSB0'
        self.baudrate = 115200
        self.timeout = 1
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

    def read_temperature(self):
        try:
            # Write data to the port to ask temperatur in Kelvin
            message = "KRDG? 0\n"
            self.ser.write(message.encode())

            # Read data from the port
            data = self.ser.read(1024).decode().strip()  # Read up to 1024 bytes and decode
            temperatures = data.split(",")[:8]  # Extract the first 8 temperatures

            # Update table with temperatures
            for row, temp in enumerate(temperatures):
                self.table_widget.setItem(row, 1, QTableWidgetItem(temp))

        except serial.SerialException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = TemperatureWindow()
    window.show()
    app.exec()
