import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading

def get_ports():
    """ List all available serial ports """
    ports = serial.tools.list_ports.comports(include_links=True)
    return [port.device for port in ports]

def read_from_port(ser):
    """ Read data from the port and display it in the text area """
    while True:
        try:
            data = ser.readline()
            decoded_data = data.decode('utf-8', errors='replace').rstrip()
            if decoded_data:
                received_text_area.insert(tk.END, f"Received: {decoded_data}\n")
                received_text_area.see(tk.END)
        except UnicodeDecodeError as e:
            received_text_area.insert(tk.END, f"Decode Error: {e}\n")
        except Exception as e:
            received_text_area.insert(tk.END, f"Error: {e}\n")

def connect():
    """ Connect to the selected port """
    port = port_combo.get()
    baud_rate = int(baud_rate_combo.get())
    try:
        global ser
        ser = serial.Serial(port, baud_rate, timeout=1)
        threading.Thread(target=read_from_port, args=(ser,), daemon=True).start()
    except Exception as e:
        received_text_area.insert(tk.END, f"Error: {e}\n")

def send_command():
    """ Send a command through the serial port and display it """
    command = command_entry.get()
    if ser:
        ser.write(command.encode('utf-8'))
        sent_text_area.insert(tk.END, f"Sent: {command}\n")
        sent_text_area.see(tk.END)

def gamepad_send():
    """ Function to handle gamepad data sending """
    while gamepad_send_var.get():
        # Add your code here to send data from the gamepad
        # Example: ser.write(gamepad_data.encode('utf-8'))
        pass
# Create the main window
root = tk.Tk()
root.title("USB Port Data Reader")

# Create frames
left_frame = tk.Frame(root)
left_frame.grid(column=0, row=0, sticky="nsew")

right_frame = tk.Frame(root)
right_frame.grid(column=1, row=0, sticky="nsew")

root.grid_columnconfigure(0, weight=2)  # Left frame weight
root.grid_columnconfigure(1, weight=1)  # Right frame weight

# Left Frame Components
# Dropdown for available ports
port_combo = ttk.Combobox(left_frame, values=get_ports(), postcommand=lambda: port_combo.configure(values=get_ports()))
port_combo.grid(column=0, row=0, padx=10, pady=10)

# Dropdown for baud rates
baud_rates = [9600, 115200]
baud_rate_combo = ttk.Combobox(left_frame, values=baud_rates, state="readonly")
baud_rate_combo.grid(column=1, row=0, padx=10, pady=10)
baud_rate_combo.current(0)  # default to 9600

# Connect button
connect_button = tk.Button(left_frame, text="Connect", command=connect)
connect_button.grid(column=2, row=0, padx=10, pady=10)

# Text area for received data display
received_text_area = tk.Text(left_frame, height=10, width=90)
received_text_area.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

# Command entry field
command_entry = tk.Entry(left_frame)
command_entry.grid(column=0, row=2, padx=10, pady=10)

# Send command button
send_button = tk.Button(left_frame, text="Send Command", command=send_command)
send_button.grid(column=1, row=2, padx=10, pady=10)

# Text area for sent data display
sent_text_area = tk.Text(left_frame, height=10, width=90)
sent_text_area.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

# Right Frame Components for displaying 7 text/numerical values
labels = []
roll=ttk.Label(right_frame, text=f"Roll  : 0", font=("Arial", 12))
roll.grid(column=0, row=0, sticky="w", padx=10, pady=5)
labels.append(roll)

pitch=ttk.Label(right_frame, text=f"Pitch: 0", font=("Arial", 12))
pitch.grid(column=0, row=1, sticky="w", padx=10, pady=5)
labels.append(pitch)

yaw=ttk.Label(right_frame, text=f"Yaw  : 0", font=("Arial", 12))
yaw.grid(column=0, row=2, sticky="w", padx=10, pady=5)
labels.append(yaw)

depth=ttk.Label(right_frame, text=f"Depth  : 0", font=("Arial", 12))
depth.grid(column=0, row=3, sticky="w", padx=10, pady=5)
labels.append(depth)

temp=ttk.Label(right_frame, text=f"Temp  : 0", font=("Arial", 12))
temp.grid(column=0, row=4, sticky="w", padx=10, pady=5)
labels.append(temp)

battery_voltage=ttk.Label(right_frame, text=f"Battery voltage  : 0", font=("Arial", 12))
battery_voltage.grid(column=0, row=5, sticky="w", padx=10, pady=5)
labels.append(battery_voltage)


# Checkbox for gamepad data sending
gamepad_send_var = tk.BooleanVar()
gamepad_send_checkbox = tk.Checkbutton(right_frame, text="Send Gamepad Data", variable=gamepad_send_var, command=lambda: threading.Thread(target=gamepad_send, daemon=True).start())
gamepad_send_checkbox.grid(column=0, row=6, sticky="w", padx=10, pady=10)

# Start the GUI event loop
root.mainloop()