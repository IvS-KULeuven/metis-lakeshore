import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:

    for i in range(8):
        # Write header to the port
        input_number = i+1  # Specify the input curve number

        # Write query
        message = f"INNAME? {input_number}\n"
        ser.write(message.encode())

        # Read data from the port
        data = ser.read(1024).decode()
        print(data)

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()