import time
import serial
from pynput.keyboard import Controller
import tkinter as tk

def submit():
    global var_values
    var_values = [entry1.get(), entry2.get(), entry3.get(), entry4.get()]
    print(f'Variable 1: {var_values[0]}, Variable 2: {var_values[1]}, Variable 3: {var_values[2]}, Variable 4: {var_values[3]}')
    root.quit()

root = tk.Tk()

label1 = tk.Label(root, text="Variable 1:")
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="Variable 2:")
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

label3 = tk.Label(root, text="Variable 3:")
label3.pack()
entry3 = tk.Entry(root)
entry3.pack()

label4 = tk.Label(root, text="Variable 4:")
label4.pack()
entry4 = tk.Entry(root)
entry4.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
root.destroy()

ser = serial.Serial('/dev/tty.usbserial-120', 9600)
keyboard = Controller()

switch_names = ['Schalter 1', 'Schalter 2', 'Schalter 3', 'Schalter 4']


while True:
    for i in range(4):
        data = ser.readline().decode('utf-8').strip()
        if data == '1':
            print(f'{switch_names[i]} ist aktiv')
            print(f'Wert für {switch_names[i]}: {var_values[i]}')