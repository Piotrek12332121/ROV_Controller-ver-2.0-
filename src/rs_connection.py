import serial
class UsbDevice():
    def __init__(self,port:str,baundrate:int):
        self.ser=serial.Serial(port,baundrate)
        self.is_serial_active=0
        print(self.ser)

    def send_via_USB(self,Avel:int,Bvel:int,Cvel:int,Dvel:int):      ### method for sending signals via USB - needs engine name and speed value 

        assert Avel >=0, f"Value {Avel} needs to be between 0 and 400"
        assert Avel <=200, f"Value {Avel} needs to be between 0 and 400"
        a_bytes=Avel.to_bytes(1,byteorder='little') 
        b_bytes=Bvel.to_bytes(1,byteorder='little') 
        c_bytes=Cvel.to_bytes(1,byteorder='little') 
        d_bytes=Dvel.to_bytes(1,byteorder='little') 
        data=a_bytes+b_bytes+c_bytes+d_bytes
        ##print(data)
        self.ser.write(data)
