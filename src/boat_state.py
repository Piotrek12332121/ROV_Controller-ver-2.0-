class Boat():
    """
    Class contains all information about ROV state and controls 

    """
    def __init__(self):

        ###motor speeds
        self._a_vel=None
        self._b_vel=None
        self._c_vel=None
        self._d_vel=None

        ###sensor values
        self._depth_sensor_value=None
        self._battery_voltage=None
        self._internal_temperature=None
        self._external_temperature=None

        ###orientation 
        self._roll=None
        self._pitch=None
        self._yaw=None
        """
        Roll is in range <-180,180> degrees, where potitive values indicate rolling to the right, and negative rolling to the left
        Pitch is in range <-90,90> degrees, where positive pitch means that front is pointing above the horizon, and negative means pointing downward 
        Yaw is in range <-180,180> degrees, where positive values turning to the right and nefative ones means turining to the left.

        The Roll and Pitch angles are obtained from the accelerometer
        THe Yaw angle is obtained from the compass onboard
        
        """

    @property
    def a_vel(self):
        return self._a_vel
    @a_vel.setter
    def a_vel(self,new_value):
        if -100<=new_value<=100:
            self._a_vel=new_value
        else:
            raise ValueError (f'Motor speed {new_value} must be in range<-100,100>')

    @property
    def b_vel(self):
        return self._b_vel
    @b_vel.setter
    def b_vel(self,new_value):
        if -100<=new_value<=100:
            self._b_vel=new_value
        else:
            raise ValueError (f'Motor speed {new_value} must be in range<-100,100>')

    @property
    def c_vel(self):
        return self._c_vel
    @c_vel.setter
    def c_vel(self,new_value):
        if -100<=new_value<=100:
            self._b_vel=new_value
        else:
            raise ValueError (f'Motor speed {new_value} must be in range<-100,100>')
        
    @property
    def d_vel(self):
        return self._d_vel
    @d_vel.setter
    def d_vel(self,new_value):
        if -100<=new_value<=100:
            self._d_vel=new_value
        else:
            raise ValueError (f'Motor speed {new_value} must be in range<-100,100>')
        
    @property
    def roll(self):
        return self._roll
    @roll.setter
    def roll(self, new_value):
        if (-180<=new_value<=180):
            self._roll = new_value
        else:
            raise ValueError(f"Value {new_value} must be in range <-180,180>")
        
    @property
    def pitch(self):
        return self._pitch
    @pitch.setter
    def pitch(self, new_value):
        if (-90<=new_value<=90):
            self._pitch = new_value
        else:
            raise ValueError(f"Value {new_value} must be in range <-90,90>")
    @property
    def yaw(self):
        return self._yaw
    @yaw.setter
    def yaw(self, new_value):
        if (-180<=new_value<180):
            self._yaw = new_value
        else:
            raise ValueError(f"Value {new_value} must be in range <-180,180>")        
          
    def get_communication_frame(self):
        a_bytes=self._a_vel.to_bytes(1,byteorder='little') 
        b_bytes=self._b_vel.to_bytes(1,byteorder='little') 
        c_bytes=self._c_vel.to_bytes(1,byteorder='little') 
        d_bytes=self._d_vel.to_bytes(1,byteorder='little')
        data_frame=a_bytes+b_bytes+c_bytes+d_bytes
        return data_frame