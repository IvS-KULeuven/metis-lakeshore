import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:
    message = f"CRVHDR? 1\n"
    ser.write(message.encode())
    name = ser.read(1024).decode().strip()
    print(name)
            
except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()