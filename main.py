import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import serial
import serial.tools.list_ports
import threading
import pygame

# Function to list all available serial ports
def get_ports():
    ports = serial.tools.list_ports.comports(include_links=True)
    return [port.device for port in ports]

# Function to read data from the port and display it in the text area
def read_from_port(ser):
    while True:
        try:
            data = ser.readline()
            decoded_data = data.decode('utf-8', errors='replace').rstrip()
            if decoded_data:
                received_text_area.insert(ttk.END, f"Received: {decoded_data}\n")
                received_text_area.see(ttk.END)
        except Exception as e:
            received_text_area.insert(ttk.END, f"Error: {e}\n")

# Function to connect to the selected port
def connect():
    port = port_combo.get()
    baud_rate = int(baud_rate_combo.get())
    try:
        global ser
        ser = serial.Serial(port, baud_rate, timeout=1)
        threading.Thread(target=read_from_port, args=(ser,), daemon=True).start()
    except Exception as e:
        received_text_area.insert(ttk.END, f"Error: {e}\n")

# Function to send a command through the serial port
def send_command():
    command = command_entry.get()
    if len(command)==4:
        message=f'<{message[0]};{message[1]};{message[2]};{message[3]}>'
        if ser:
            ser.write(message.encode('utf-8'))
            sent_text_area.insert(ttk.END, f"Sent: {command}\n")
            sent_text_area.see(ttk.END)

# Function to convert gamepad axis value
def convert(x, range=False):
    if not range:
        value = -x * 50
        value = int(value + 150)
    else:
        value = x * 50
        value = int(value + 150 + 0.5)
    if value < 100:
        value = 100
    if value > 200:
        value = 200
    return value

# Function to handle gamepad input and send data through USB
def gamepad_thread():

    pygame.init()
    # joystick_count = pygame.joystick.get_count()
    # if joystick_count == 0:
    #     print("No joysticks found.")
        
    #     return
    # my_joystick = pygame.joystick.Joystick(0)
    # my_joystick.init()
    i=0
    while gamepad_send_var.get():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Handle joystick axis motion
        # J1_axis_x = convert(my_joystick.get_axis(0), True)
        # J1_axis_y = convert(my_joystick.get_axis(1), True)
        # J2_axis_x = convert(my_joystick.get_axis(2), False)
        # J2_axis_y = convert(my_joystick.get_axis(3), False)
        data_to_send=f'Dupa{i}\n'
        ser.write(data_to_send.encode('utf-8'))
        sent_text_area.insert(ttk.END, f"Sent: {data_to_send}\n")
        sent_text_area.see(ttk.END)
        i=i+1
        # Example of sending data via USB, replace with your own implementation
        # if ser:
        #     data_to_send = f"<{J1_axis_x};{J1_axis_y};{J2_axis_x};{J2_axis_y}>\n"
        #     ser.write(data_to_send.encode('utf-8'))

        pygame.time.delay(100)  # Delay for 20 ms

    pygame.quit()

# Create the main window with a dark theme
root = ttk.Window(themename='darkly')
root.title("ROV controller")
# GUI components setup
# Left frame
left_frame = ttk.Frame(root)
left_frame.grid(column=0, row=0, sticky="nsew")

port_combo = ttk.Combobox(left_frame, values=get_ports(), postcommand=lambda: port_combo.configure(values=get_ports()))
port_combo.grid(column=0, row=0, padx=(10, 5), pady=10)

baud_rate_combo = ttk.Combobox(left_frame, values=[115200, 9600], state="readonly")
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

# Right frame
right_frame = ttk.Frame(root)
right_frame.grid(column=2, row=0, sticky="nsew")

# Right Frame Components
labels = []
roll = ttk.Label(right_frame, text=f"Roll     : 0 ", font=("Arial", 12))
roll.grid(column=0, row=0, sticky="w", padx=10, pady=5)

pitch = ttk.Label(right_frame, text=f"Pitch    : 0", font=("Arial", 12))
pitch.grid(column=0, row=1, sticky="w", padx=10, pady=5)

yaw = ttk.Label(right_frame, text=f"Yaw      : 0", font=("Arial", 12))
yaw.grid(column=0, row=2, sticky="w", padx=10, pady=5)

depth = ttk.Label(right_frame, text=f"Depth    : 0", font=("Arial", 12))
depth.grid(column=0, row=3, sticky="w", padx=10, pady=5)

temp = ttk.Label(right_frame, text=f"Temp     : 0", font=("Arial", 12))
temp.grid(column=0, row=4, sticky="w", padx=10, pady=5)

battery_voltage = ttk.Label(right_frame, text=f"Batt vol : 0", font=("Arial", 12))
battery_voltage.grid(column=0, row=5, sticky="w", padx=10, pady=5)

def update_real_time_data(roll_value, pitch_value, yaw_value, depth_value, temp_value):
    roll.config(text=f"Roll     : {roll_value} ")
    pitch.config(text=f"{pitch_value:.2f}")
    yaw.config(text=f"{yaw_value:.2f}")
    depth.config(text=f"{depth_value:.2f}")
    temp.config(text=f"{temp_value:.2f}")

# Assign command to gamepad checkbox
def on_gamepad_checkbox():
    if gamepad_send_var.get():
        threading.Thread(target=gamepad_thread, daemon=True).start()

gamepad_send_checkbox.config(command=on_gamepad_checkbox)

# Start the GUI event loop
root.mainloop()
