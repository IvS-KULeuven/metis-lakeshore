import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy
from PySide6.QtCore import Qt, QTimer
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

        # Set size policy to expand vertically
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set vertical header to resize to contents
        self.table_widget.verticalHeader().setSectionResizeMode(PySide6.QtWidgets.QHeaderView.ResizeToContents)

        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)

        # Configure serial port settings
        self.port = '/dev/ttyUSB0'
        self.baudrate = 115200
        self.timeout = 1
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

        # Read names of inputs
        self.read_input_names()

        # Read temperatures
        self.read_temperature()

        # Start timer for updating temperature
        self.timer = QTimer(self)
        self.timer.setInterval(10000)  # Update every 10 seconds
        self.timer.timeout.connect(self.read_temperature)
        self.timer.start()

        # Connect signal for name change
        self.table_widget.itemChanged.connect(self.handle_name_change)

    def read_input_names(self):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"INNAME? {input_number}\n"
                self.ser.write(message.encode())
                name = self.ser.read(1024).decode().strip()
                self.table_widget.setItem(row, 0, QTableWidgetItem(name))
        except serial.SerialException as e:
            print(f"Error: {e}")

    def read_temperature(self):
        try:
            # Write data to the port to ask temperature in Kelvin
            message = "KRDG? 0\n"
            self.ser.write(message.encode())

            # Read temperature data from the port
            data = self.ser.read(1024).decode().strip()  # Read up to 1024 bytes and decode
            temperatures = data.split(",")[:8]  # Extract the first 8 temperatures

            # Update table with formatted temperatures
            for row, temp in enumerate(temperatures):
                formatted_temp = temp.lstrip('+')  # Remove leading '+'
                if formatted_temp.startswith('0') and '.' in formatted_temp:
                    formatted_temp = formatted_temp.lstrip('0')  # Remove leading '0's except for '0.0'
                self.table_widget.setItem(row, 1, QTableWidgetItem(formatted_temp if formatted_temp != '.00000' else '0'))

        except serial.SerialException as e:
            print(f"Error: {e}")

    def handle_name_change(self, item):
        if item.column() == 0:  # Only handle changes in the "Name" column
            row = item.row()
            input_number = row + 1
            new_name = item.text()
            message = f"INNAME {input_number},{new_name}\n"
            self.ser.write(message.encode())
            # self.read_input_names()  # Update input names after change

if __name__ == "__main__":
    app = QApplication([])
    window = TemperatureWindow()
    window.show()
    app.exec()
