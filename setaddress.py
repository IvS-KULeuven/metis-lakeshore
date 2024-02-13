import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:
    # Write header to the port
    address = 2  # Specify the input curve number

    message = f"ADDR {address}\n"
    ser.write(message.encode())

    # Write header query
    message = f"ADDR? \n"
    ser.write(message.encode())

    # Read data from the port
    data = ser.read(1024).decode()
    print(f"address: {data}")

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()
