from abc import ABC, abstractmethod

class Session(ABC):

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def look_at(self, radius, theta, phi, v):
        pass

    @abstractmethod
    def inverse_kinematics(self, quaternion):
        pass

    @abstractmethod
    def goto(self):
        pass
    
    @abstractmethod
    def r_antenna_set_position(self, position):
        pass

    @abstractmethod
    def l_antenna_set_position(self, position):
        pass

    @abstractmethod
    def antennas_speed_limit(self, v):
        pass

    @abstractmethod
    def start_autofocus(self):
        pass
    
    @abstractmethod
    def stop_autofocus(self):
        pass

    @abstractmethod
    def get_frame(self):
        pass