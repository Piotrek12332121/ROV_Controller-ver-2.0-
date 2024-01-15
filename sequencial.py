import pygame
from  src.rs_connection import UsbDevice
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



usb_=UsbDevice('COM11',9600)

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
        usb_.send_via_USB(int(J1_axis_y),int(J2_axis_y),int(C_vel),int(D_vel))
        clock.tick(20)
                
        