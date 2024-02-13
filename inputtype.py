import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:

    # write intype
    message = "INTYPE 1,2,0,0,1,1,1\n"
    ser.write(message.encode())

    # read intype
    message = "INTYPE? 1\n"
    ser.write(message.encode())

    data = ser.read(1024).decode()
    print(f"Curve Header: {data}")

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()
