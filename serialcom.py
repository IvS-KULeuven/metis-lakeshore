import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:
  # Write data to the port
  message = "KRDG? 2\n"
  ser.write(message.encode())  # Convert to bytes for sending

  # Read data from the port
  data = ser.read(1024).decode()  # Read up to 1024 bytes and decode
  print(f"Received in Kelvin: {data}")

  # read degrees in celsius
  message = "CRDG? 2\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Received in Celsius: {data}")

  # check brightness
  message = "BRIGT?\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Brightness: {data}")

  # check identification
  message = "*IDN?\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Identification: {data}")

  #check module name
  message = "MODNAME?\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Module name: {data}")

  # check address
  message = "ADDR?\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Address: {data}")

  # curve data point query
  message = "CRVPT? 1 50\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Curve: {data}")

  # curve header query
  message = "CRVHDR? 2\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Curve Header: {data}")

  # check filter length
  message = "FILTER? 2\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Filter: {data}")

  # check sensor name
  message = "INNAME? 2\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Sensor name: {data}")

  # check range if autorange is on
  message = "INTYPE? 2\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"Range: {data}")

  # profibius slot count query
  message = "PROFINUM?\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"PROFIBIUS slots: {data}")

  # profislot configuration query
  message = "PROFISLOT? 2\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"PROFISLOT: {data}")

  # profibus connection status query
  message = "PROFISTAT?\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"status: {data}")

  # input reading status query
  message = "RDGST? 2\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"reading status: {data}")

  # sensor units input reading query
  message = "SRDG? 0\n"
  ser.write(message.encode())

  data = ser.read(1024).decode()
  print(f"SRDG: {data}")


except serial.SerialException as e:
  print(f"Error: {e}")

finally:
  # Close the serial port
  ser.close()