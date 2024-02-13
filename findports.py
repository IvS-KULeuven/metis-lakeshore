import serial
import glob

# Search for available serial ports
ports = glob.glob('/dev/ttyUSB*')
print("Available serial ports:", ports)

# Iterate through each port and try to open it
for port in ports:
    try:
        # Open the serial port
        ser = serial.Serial(port, 115200, timeout=1)
        print("Connected to", port)
        
        # Attempt to communicate with the device here
        
        # Close the serial port
        ser.close()
        break  # Exit loop if successful
    except serial.SerialException:
        print("Failed to connect to", port)

else:
    print("No suitable serial port found.")
