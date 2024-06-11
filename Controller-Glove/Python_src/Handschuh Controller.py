import serial
import tkinter as tk
from pynput.keyboard import Controller, Key, KeyCode


keyboard = Controller()

key_map = {
    # Spezielle Tasten
    "Return": Key.enter,
    "space": Key.space,
    "Backspace": Key.backspace,
    "Tab": Key.tab,
    "Escape": Key.esc,
    "Delete": Key.delete,
    "Right": Key.right,
    "Left": Key.left,
    "Down": Key.down,
    "Up": Key.up,
    "Prior": Key.page_up,
    "Next": Key.page_down,
    "Home": Key.home,
    "End": Key.end,
    "CapsLock": Key.caps_lock,
    "F1": Key.f1,
    "F2": Key.f2,
    "F3": Key.f3,
    "F4": Key.f4,
    "F5": Key.f5,
    "F6": Key.f6,
    "F7": Key.f7,
    "F8": Key.f8,
    "F9": Key.f9,
    "F10": Key.f10,
    "F11": Key.f11,
    "F12": Key.f12,
}

# Zeichen- und Zifferntasten
for char in 'abcdefghijklmnopqrstuvwxyz1234567890':
    key_map[char] = KeyCode.from_char(char)

# Großbuchstaben
for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    key_map[char] = KeyCode.from_char(char)

# Sonderzeichen
for char in '`~-_=+[{]};|:\'",<.>/?':
    key_map[char] = KeyCode.from_char(char)

# Globale Variablen
var_values = ['']*6
key_value = ''
entries = [None]*6  # Liste zum Speichern der Entry-Objekte

# Funktion zum Senden der Werte
def submit():
    global var_values, key_value
    var_values = [entries[i].get() for i in range(6)]  # Abrufen der Werte aus den Entry-Objekten
    print(f'Variable values: {var_values}')
    root.quit()

def on_key_press(event):
    key = event.keysym  # Ermittelt das Symbol des gedrückten Schlüssels
    pfeiltasten_var.set(key)
    event.widget.delete(0, 'end')  # Löscht den aktuellen Inhalt des Eingabefelds
    event.widget.insert(0, key)  # Fügt den Wert des gedrückten Schlüssels in das Eingabefeld ein
    print(f"Taste gedrückt: {key}")
    return 'break'

# Erstellen Sie das Tkinter-Fenster
root = tk.Tk()

# Erstelle eine StringVar, um die Pfeiltasten zu speichern
pfeiltasten_var = tk.StringVar()


# Liste der Titel
titles = ["Zeigefinger", "Mittelfinger", "Ringfinger", "Kleinerfinger", "Links kippen", "Rechts kippen"]

# In Ihrer Schleife:
for i in range(6):
    label = tk.Label(root, text=titles[i])
    label.grid(row=(i%2)*3, column=i//2)  # Positionieren Sie das Label in der Grid

    # Laden Sie das Bild
    image = tk.PhotoImage(file=f"./images/{titles[i]}.ppm")

    # Ändern Sie die Größe des Bildes mit subsample
    image = image.subsample(4, 4)  # Ändern Sie die Werte nach Bedarf

    # Erstellen Sie ein Label mit dem Bild
    image_label = tk.Label(root, image=image)
    image_label.image = image  # Behalten Sie eine Referenz, um die Garbage Collection zu verhindern
    image_label.grid(row=(i%2)*3+1, column=i//2)  # Positionieren Sie das Bildlabel in der Grid

    entry = tk.Entry(root)
    entry.grid(row=(i%2)*3+2, column=i//2)  # Positionieren Sie das Eingabefeld in der Grid
    entry.bind("<KeyPress>", on_key_press)
    entries[i] = entry

# Erstellen Sie die Schaltfläche zum Senden der Werte
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=6*3+2, column=0, columnspan=3)  # Positionieren Sie die Schaltfläche in der Grid

# Starten Sie die Tkinter-Schleife
root.mainloop()
root.destroy()

# Erstellen Sie eine serielle Verbindung
ser = serial.Serial('/dev/tty.usbserial-1130', 9600)

while True:
    if ser.in_waiting > 0:
        # Lesen Sie eine Zeile von der seriellen Verbindung
        line = ser.readline().decode('utf-8').strip()

        # Überprüfen Sie, ob die Zeile Daten enthält
        if "AcX" in line:
            # Teilen Sie die Zeile in ihre Komponenten
            parts = line.split(" | ")

            # Speichern Sie die Werte in Variablen
            acX = int(parts[0].split(" = ")[1])
            acY = int(parts[1].split(" = ")[1])

            print(f"Acceleration X: {acX}, Acceleration Y: {acY}")

            if acX > 10000:
                key = key_map.get(var_values[4])  # Holen Sie das Key-Objekt aus der Mapping-Tabelle
                keyboard.press(key)
            elif acX < -10000:
                key = key_map.get(var_values[5])  # Holen Sie das Key-Objekt aus der Mapping-Tabelle
                keyboard.press(key)
            else:
                key = key_map.get(var_values[4])  # Holen Sie das Key-Objekt aus der Mapping-Tabelle
                keyboard.release(key)
                key = key_map.get(var_values[5])  # Holen Sie das Key-Objekt aus der Mapping-Tabelle
                keyboard.release(key)

        elif "Sensor" in line:
            # Teilen Sie die Zeile in ihre Komponenten
            parts = line.split(": ") 

            # Speichern Sie die Werte in Variablen
            sensor_num = int(parts[0].split(" ")[1])
            sensor_value = int(parts[1])

            if sensor_value > 100:
                key = key_map.get(var_values[sensor_num])
                keyboard.press(key)
            else:
                key = key_map.get(var_values[sensor_num])
                keyboard.release(key)

            print(f"Sensor {sensor_num}: {sensor_value}")