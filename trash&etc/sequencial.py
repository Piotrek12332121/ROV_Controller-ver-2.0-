import pygame
from  src.rs_connection import UsbDevice
def convert(x:float,range=False)->int:
    """
    In first mode ( choose_range== False) The values in range of <100,200> are send - for normal operation 
    In second monde (choose_range== True) the values in range of<0,200> are send - for unlocking motors 

    """
    if not range:
        value=-x*50
        value=int(value+150)
    else:
        value=x*50
        value=int(value+150+0.5)
    if value<100:
        value=100
    if value>200:
        value=200
    return value

usb_=UsbDevice('COM11',115200)

A_vel=0
B_vel=0
C_vel=150
D_vel=150



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
    
    running=True
    while running:
        for event in pygame.event.get():   
            change_range = my_joystick.get_button(1)

            if my_joystick.get_button(0)==1:
                C_vel=C_vel+2
                D_vel=D_vel-2

                if C_vel<100:
                    C_vel=100 
                if C_vel>200:
                    C_vel=200 

                if D_vel<100:
                    D_vel=100
                if D_vel>200:
                    D_vel=200 

            if my_joystick.get_button(2)==1:
                C_vel=C_vel-2
                D_vel=D_vel+2
                if C_vel<100:
                    C_vel=100 
                if C_vel>200:
                    C_vel=200 

                if D_vel<100:
                    D_vel=100
                if D_vel>200:
                    D_vel=200 
            # if event.type == pygame.JOYAXISMOTION:
            #     # Handle joystick axis motion
        J1_axis_x = convert( my_joystick.get_axis(0),True)
        J1_axis_y= convert(my_joystick.get_axis(1),True)
        J2_axis_x = convert(my_joystick.get_axis(2),False)
        J2_axis_y= convert(my_joystick.get_axis(3),False)

                # width=4
                # precision = 2  # Number of decimal places you want to display
                # J1_x_formated = "{:0.{}f}".format(J1_axis_x, precision) 
                # J1_y_formated = "{:.{}f}".format(J1_axis_y, precision)
                # J2_x_formated = "{:0.{}f}".format(J2_axis_x, precision)
                # J2_y_formated = "{:.{}f}".format(J2_axis_y, precision)

                #print(f" Joy_1({J1_axis_x},{J1_axis_y}) Joy_2({J2_axis_x},{J2_axis_y})")
        print(J1_axis_y,J2_axis_y,C_vel,D_vel)
        usb_.send_via_USB(int(J1_axis_y),int(J2_axis_y),C_vel,D_vel)
        ##usb_.send_via_USB('B',int(J2_axis_y))
      #  print(f"USB: A {J1_axis_y} B {J2_axis_y}")
        clock.tick(5)
                
        