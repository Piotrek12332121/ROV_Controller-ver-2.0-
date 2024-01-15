import pygame 
pygame.init()
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joysticks found.")
    return
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
i=0
while gamepad_send_var.get():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    # Handle joystick axis motion
    J1_axis_x = convert(my_joystick.get_axis(0), True)
    J1_axis_y = convert(my_joystick.get_axis(1), True)
    J2_axis_x = convert(my_joystick.get_axis(2), False)
    J2_axis_y = convert(my_joystick.get_axis(3), False)

    if ser:
        data_to_send = f"{J1_axis_x}{J1_axis_y}{J2_axis_x}{J2_axis_y}\n"
        ser.write(data_to_send.encode('utf-8'))
        sent_text_area.insert(ttk.END, f"Sent: {data_to_send}\n")
        sent_text_area.see(ttk.END)
    pygame.time.delay(20)  # Delay for 20 ms

pygame.quit()