import serial

# Erstellen Sie eine serielle Verbindung
ser = serial.Serial('/dev/tty.usbserial-130', 9600)

while True:
    if ser.in_waiting > 0:
        # Lesen Sie eine Zeile von der seriellen Verbindung
        line = ser.readline().decode('utf-8').strip()
        # Geben Sie die gelesene Zeile aus
        print(line)