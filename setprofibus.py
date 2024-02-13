import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:
    message = f"PROFINUM 2\n"
    ser.write(message.encode())
    
    message = f"PROFISLOT 2,2,1\n"
    ser.write(message.encode())

    message = f"PROFISLOT? 2\n"
    ser.write(message.encode())

    data = ser.read(1024).decode()
    print(f"PROFISLOT: {data}")

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()
