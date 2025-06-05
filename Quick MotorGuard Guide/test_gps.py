import serial
import time
import sys

# Open serial port to A7670SA
try:
    ser = serial.Serial("/dev/ttyUSB3", baudrate=115200, timeout=2)
except Exception as e:
    print(f"Failed to open serial port: {e}")
    sys.exit(1)

def send_at(command, delay=1.5, expect_ok=True):
    print(f"> Sending: {command}")
    ser.write((command + "\r\n").encode())
    time.sleep(delay)

    response = []
    while ser.in_waiting:
        line = ser.readline().decode(errors="ignore").strip()
        print(f"< {line}")
        response.append(line)

    if expect_ok and not any("OK" in r for r in response):
        print(f"Command '{command}' failed or returned no OK.")
        return False
    return True

# Test sequence with fail handling
if not send_at("AT"):
    print("Modem not responding. Check power or wiring.")
    sys.exit(1)

if not send_at("AT+CSQ"):
    print("No signal quality reported.")

if not send_at("AT+CGMI"):
    print("Could not read manufacturer info.")

if not send_at("AT+CREG?"):
    print("Not registered to network.")
    print("Make sure SIM card is inserted and module is in coverage area.")
    sys.exit(1)

print("\nAll essential AT tests passed. Module is ready.")
