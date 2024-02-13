import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:
  # Write data to the port
  message = "KRDG? 0\n"
  ser.write(message.encode())  # Convert to bytes for sending

  # Read data from the port
  data = ser.read(1024).decode()  # Read up to 1024 bytes and decode
  print(f"Received in Kelvin: {data}")
  
except serial.SerialException as e:
  print(f"Error: {e}")

finally:
  # Close the serial port
  ser.close()