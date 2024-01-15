from src.boat_state import Boat
from src.rs_connection import UsbDevice

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import serial
import serial.tools.list_ports
import threading

boat=Boat()
def update_boat_state(raw_string:str):
    pass

def get_ports():
    """ List all available serial ports """
    ports = serial.tools.list_ports.comports(include_links=True)
    return [port.device for port in ports]

def read_from_port(ser):
    """ Read data from the port and display it in the text area """
    while True:
        try:
            data = ser.readline()
            update_boat_state(data)
            decoded_data = data.decode('utf-8', errors='replace').rstrip()
            if decoded_data:
                received_text_area.insert(ttk.END, f"Received: {decoded_data}\n")
                received_text_area.see(ttk.END)
        except UnicodeDecodeError as e:
            received_text_area.insert(ttk.END, f"Decode Error: {e}\n")
        except Exception as e:
            received_text_area.insert(ttk.END, f"Error: {e}\n")

def connect():
    """ Connect to the selected port """
    port = port_combo.get()
    baud_rate = int(baud_rate_combo.get())
    try:
        global ser
        ser = serial.Serial(port, baud_rate, timeout=1)
        threading.Thread(target=read_from_port, args=(ser,), daemon=True).start()
    except Exception as e:
        received_text_area.insert(ttk.END, f"Error: {e}\n")

def send_command():
    """ Send a command through the serial port and display it """
    command = command_entry.get()
    if ser:
        ser.write(command.encode('utf-8'))
        sent_text_area.insert(ttk.END, f"Sent: {command}\n")
        sent_text_area.see(ttk.END)






# Create the main window with a dark theme
root = ttk.Window(themename='darkly')

# Create frames
left_frame = ttk.Frame(root)
left_frame.grid(column=0, row=0, sticky="nsew")

separator = ttk.Frame(root, width=2, style='White.TFrame')
separator.grid(column=1, row=0, sticky='ns')

right_frame = ttk.Frame(root)
right_frame.grid(column=2, row=0, sticky="nsew")

root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)

# Left Frame Components
port_combo = ttk.Combobox(left_frame, values=get_ports(), postcommand=lambda: port_combo.configure(values=get_ports()))
port_combo.grid(column=0, row=0, padx=(10, 5), pady=10)

baud_rate_combo = ttk.Combobox(left_frame, values=[115200,9600], state="readonly")
baud_rate_combo.grid(column=1, row=0, padx=(5, 5), pady=10)
baud_rate_combo.current(0)

connect_button = ttk.Button(left_frame, text="Connect", command=connect, bootstyle=PRIMARY)
connect_button.grid(column=2, row=0, padx=(5, 10), pady=10)

received_text_area = ttk.Text(left_frame, height=10, width=100)
received_text_area.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

command_entry = ttk.Entry(left_frame)
command_entry.grid(column=0, row=2, padx=(10, 5), pady=10)

send_button = ttk.Button(left_frame, text="Send Command", command=send_command, bootstyle=PRIMARY)
send_button.grid(column=1, row=2, padx=(5, 5), pady=10)

gamepad_send_var = ttk.BooleanVar()
gamepad_send_checkbox = ttk.Checkbutton(left_frame, text="Send Gamepad Data", variable=gamepad_send_var, bootstyle=SUCCESS)
gamepad_send_checkbox.grid(column=2, row=2, padx=(5, 10), pady=10)

sent_text_area = ttk.Text(left_frame, height=10, width=100)
sent_text_area.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

# Right Frame Components
labels = []
roll = ttk.Label(right_frame, text=f"Roll  : 0", font=("Arial", 12))
roll.grid(column=0, row=0, sticky="w", padx=10, pady=5)

pitch = ttk.Label(right_frame, text=f"Pitch: 0", font=("Arial", 12))
pitch.grid(column=0, row=1, sticky="w", padx=10, pady=5)

yaw = ttk.Label(right_frame, text=f"Yaw  : 0", font=("Arial", 12))
yaw.grid(column=0, row=2, sticky="w", padx=10, pady=5)

depth = ttk.Label(right_frame, text=f"Depth  : 0", font=("Arial", 12))
depth.grid(column=0, row=3, sticky="w", padx=10, pady=5)

temp = ttk.Label(right_frame, text=f"Temp  : 0", font=("Arial", 12))
temp.grid(column=0, row=4, sticky="w", padx=10, pady=5)

battery_voltage = ttk.Label(right_frame, text=f"Battery voltage  : 0", font=("Arial", 12))
battery_voltage.grid(column=0, row=5, sticky="w", padx=10, pady=5)

# Start the GUI event loop
print(gamepad_send_var)
root.mainloop()