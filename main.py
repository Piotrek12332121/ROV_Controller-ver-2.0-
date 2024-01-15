import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import serial
import serial.tools.list_ports
import threading
import pygame
import re 
from src.boat_state import Boat
from src.rs_connection import UsbDevice
boat_=Boat()

# Function to list all available serial ports
def get_ports():
    ports = serial.tools.list_ports.comports(include_links=True)
    return [port.device for port in ports]

def get_values_from_raw(raw_string:str):
    filtered_string=re.findall(r'<(.*?)>', raw_string)
    values=filtered_string[0].split(',')
    return values

# Function to read data from the port and display it in the text area
def read_from_port(ser_port):
    while True:
        try:
            data = ser_port.ser.readline()
            decoded_data = data.decode('utf-8', 
                                       errors='replace').rstrip()
  
            if decoded_data:
                values=get_values_from_raw(decoded_data)
                boat_.update_values(values)
                update_real_time_data(values)
            
                received_text_area.insert(ttk.END,
                                           f"Received: {decoded_data}\n")
                received_text_area.see(ttk.END)

        except Exception as e:
            received_text_area.insert(ttk.END, f"Error: {e}\n")

# Function to connect to the selected port
def connect():
    port = port_combo.get()
    baud_rate = int(baud_rate_combo.get())
    try:
        global ser_port
        ser_port = UsbDevice(port,baud_rate)
        threading.Thread(target=read_from_port, args=(ser_port,),
                          daemon=True).start()
    except Exception as e:
        received_text_area.insert(ttk.END, f"Error: {e}\n")

# Function to send a command through the serial port
def send_command():
    command = command_entry.get()

    if len(command)==4:
        message=f'{command[0]}{command[1]}{command[2]}{command[3]}'
        if ser_port.ser:
            ser_port.ser.write(message.encode('utf-8'))
            sent_text_area.insert(ttk.END, f"Sent: {command}\n")
            sent_text_area.see(ttk.END)
    else: 
        matches =command.split(',')
        message=f'{matches[0]}{matches[1]}{matches[2]}{matches[3]}'

        if ser_port.ser:
            ser_port.ser.write(message.encode('utf-8'))
            sent_text_area.insert(ttk.END, f"Sent: {message}\n")
            sent_text_area.see(ttk.END)
        

# Function to convert gamepad axis value
def convert(x:float,range=False)->int:
    """
    In first mode ( choose_range== False) The values in range of <100,200> are send - for normal operation 
    In second monde (choose_range== True) the values in range of<0,200> are send - for unlocking motors 

    """
    if not range:
        value=-x*100
        value=int(value+100)
    else:
        value=x*100
        value=int(value+100+0.5)
    if value<0:
        value=0
    if value>200:
        value=200
    return value
# Function to handle gamepad input and send data through USB
def gamepad_thread():
    A_vel=100
    B_vel=100
    C_vel=100
    D_vel=100

    pygame.init()

    clock=pygame.time.Clock()
    change_range=False


    # Count the joysticks the computer has
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        # No joysticks!
        print("Error, I didn't find any joysticks.")
    else:
        # Use joystick #0 and initialize it
        my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()
        print("Joystick found and inicialized.")

    if joystick_count != 0:
        global ser_port
        running=True
        while running:
            for event in pygame.event.get():   


                if my_joystick.get_button(0)==1:
                    C_vel=C_vel+1
                    D_vel=D_vel-1

                    if C_vel<0: 
                        C_vel=0
                    if C_vel>200:
                        C_vel=200

                    if D_vel<0:
                        D_vel=0
                    if D_vel>200:
                        D_vel=200 

                if my_joystick.get_button(2)==1:
                    C_vel=C_vel-1
                    D_vel=D_vel+1

                    if C_vel<0:
                        C_vel=0
                    if C_vel>200:
                        C_vel=200

                    if D_vel<0:
                        D_vel=0
                    if D_vel>200:
                        D_vel=200 

            J1_axis_x = convert( my_joystick.get_axis(0),True)
            J1_axis_y= convert(my_joystick.get_axis(1),True)
            J2_axis_x = convert(my_joystick.get_axis(2),False)
            J2_axis_y= convert(my_joystick.get_axis(3),False)

            print(J1_axis_y,J2_axis_y,C_vel,D_vel)

            sent_text_area.insert(ttk.END, f"Sent: {J1_axis_y,J2_axis_y,C_vel,D_vel}\n")
            sent_text_area.see(ttk.END)
        
            ser_port.send_via_USB(int(J1_axis_y),int(J2_axis_y),int(C_vel),int(D_vel))
            clock.tick(10)

# Create the main window with a dark theme
root = ttk.Window(themename='darkly')
root.title("ROV controller")
# GUI components setup
# Left frame
left_frame = ttk.Frame(root)
left_frame.grid(column=0, row=0, sticky="nsew")

port_combo = ttk.Combobox(left_frame, values=get_ports(), postcommand=lambda: port_combo.configure(values=get_ports()))
port_combo.grid(column=0, row=0, padx=(10, 5), pady=10)
port_combo.current(0)

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
a_vel = ttk.Label(right_frame, text=f"A velocity: 0 ", font=("Arial", 12))
a_vel.grid(column=0, row=0, sticky="w", padx=10, pady=5)

b_vel = ttk.Label(right_frame, text=f"B velocity: 0  ", font=("Arial", 12))
b_vel.grid(column=0, row=1, sticky="w", padx=10, pady=5)

c_vel = ttk.Label(right_frame, text=f"C velocity: 0  ", font=("Arial", 12))
c_vel.grid(column=0, row=2, sticky="w", padx=10, pady=5)

d_vel = ttk.Label(right_frame, text=f"D velocity: 0  ", font=("Arial", 12))
d_vel.grid(column=0, row=3, sticky="w", padx=10, pady=5)


roll = ttk.Label(right_frame,  text=f"Roll         : 0  ", font=("Arial", 12))
roll.grid(column=0, row=4, sticky="w", padx=10, pady=5)

pitch = ttk.Label(right_frame, text=f"Pitch       : 0", font=("Arial", 12))
pitch.grid(column=0, row=5, sticky="w", padx=10, pady=5)

yaw = ttk.Label(right_frame, text=  f"Compass: 0", font=("Arial", 12))
yaw.grid(column=0, row=6, sticky="w", padx=10, pady=5)

depth = ttk.Label(right_frame, text=f"Depth     : 0", font=("Arial", 12))
depth.grid(column=0, row=7, sticky="w", padx=10, pady=5)

temp = ttk.Label(right_frame, text=f"Temp      : 0", font=("Arial", 12))
temp.grid(column=0, row=8, sticky="w", padx=10, pady=5)

battery_voltage = ttk.Label(right_frame, text=f"Batt vol   : 0", font=("Arial", 12))
battery_voltage.grid(column=0, row=9, sticky="w", padx=10, pady=5)

def update_real_time_data(*args):
    a_vel.config(text=f"A velocity: {args[0][0]}")
    b_vel.config(text=f"B velocity: {args[0][1]}")
    c_vel.config(text=f"C velocity: {args[0][2]}")
    d_vel.config(text=f"D velocity: {args[0][3]}")

    roll.config(text= f"Roll    : {args[0][4]}")
    pitch.config(text=f"Pitch   : {args[0][5]}")
    yaw.config(text=  f"Compass : {args[0][6]}")
    depth.config(text=f"Depth : {int(args[0][7])/100} m ")
    if len(args)>=9:
        depth.config(text=f"Depth : {args[0][7]}")
        temp.config(text= f"Temp  : {args[0][8]}")
        battery_voltage.config(text= f"Batt vol : {args[0][9]}")

# Assign command to gamepad checkbox
def on_gamepad_checkbox():
    if gamepad_send_var.get():
        threading.Thread(target=gamepad_thread, daemon=True).start()

gamepad_send_checkbox.config(command=on_gamepad_checkbox)

# Start the GUI event loop
root.mainloop()
