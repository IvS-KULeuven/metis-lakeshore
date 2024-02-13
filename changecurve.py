import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:
    # Write header to the port
    input_number = 1  # Specify the input curve number
    name = "LSCI_PT-100"  # Curve name limited to 15 characters
    serial_number = "Standard C"  # Curve serial number limited to 10 characters
    format_code = 3  # Format code for resistance versus temperature
    limit_value = 810.0  # Upper temperayture limit in Kelvin
    coefficient = 2  # Positive temperature coefficient

    message = f"CRVHDR {input_number},{name},{serial_number},{format_code},{limit_value},{coefficient}\n"
    ser.write(message.encode())

    # Write header query
    message = f"CRVHDR? {input_number}\n"
    ser.write(message.encode())

    # Read data from the port
    data = ser.read(1024).decode()
    print(f"Curve Header: {data}")

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()
