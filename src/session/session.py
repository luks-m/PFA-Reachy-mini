from abc import ABC, abstractmethod

class Session(ABC):

    #Switch on the motorisation of the head
    @abstractmethod
    def turn_on(self):
        pass

    #Switch off the motorisation of the head
    @abstractmethod
    def turn_off(self):
        pass
    
    #Compute and send disks position to look at the position (radius, thetha, phi) point in spherical coordinates with a duration d
    #radius : meter, theta : degree, phi : degree, d : second
    @abstractmethod
    def look_at(self, radius, theta, phi, d):
        pass

    #Compute disks position from quaternion
    @abstractmethod
    def inverse_kinematics(self, quaternion):
        pass

    #Send disk position
    @abstractmethod
    def goto(self, dict, duration):
        pass
    
    #Send right antenna position
    @abstractmethod
    def r_antenna_set_position(self, position):
        pass

    #Send left antenna position
    @abstractmethod
    def l_antenna_set_position(self, position):
        pass

    #Set speed limit for both antennas
    @abstractmethod
    def antennas_speed_limit(self, v):
        pass

    #Get current angles
    @abstractmethod
    def get_angles(self):
        pass

    #Start autofocus of right camera
    @abstractmethod
    def start_autofocus(self):
        pass
    
    #Stop autofocus of right camera
    @abstractmethod
    def stop_autofocus(self):
        pass

    #Get last frame of right camera
    @abstractmethod
    def get_frame(self):
        pass