class Timer:
    def __init__(self, current_time):
        """
        Constructor for Timer class

        Attributes:
            current_time (int): value to start timer at
        """
        self.current_time = current_time

    def decrement(self):
        """
        decrements current_time attribute by 1

        Returns:
            updated current_time (int)
        """
        if self.current_time > 0:
            self.current_time = self.current_time - 1
        return self.current_time

    def __get_time__(self):
        """
        Returns current_time (int)
        """
        return self.current_time
    
    def __set_time__(self, x):
        """
        sets current time count to x

        Args:
            x (int): number for current_time to be assigned to
            
        Returns:
            None
        """
        self.current_time = x
    

class Hatcher:

    def __init__(self):
        """
        Constructor for Hatcher class

        Attributes"

            count (int): the current number of eggs in the hatcher
            high_count (int): the highest number of eggs that have been in the hatcher
        
        """
        self.count = 0 
        self.high_count = 0

    def __len_count__(self):
        """
        The number of eggs currently in the hatcher

        Returns:
            count (int): number of eggs
        """
        return self.count

    def __len_high_count__(self):
        """
        The largest number of eggs hatched at once

        Returns:
            high_count (int): high score of eggs hatched
        """
        return self.high_count
    
    def __set_high_count__(self, x):
        """
        sets high count to x

        Args:
            x (int): number for high count to be assigned to

        Returns:
            None
        """
        self.high_count = x

    def __set_count__(self, x):
        """
        sets count to x

        Args:
            x (int): number for count to be assigned to
            
        Returns:
            None
        """
        self.count = x
    
    def lay_egg(self):
        """
        increases egg count by one

        Returns:
            None
        """
        self.count += 1
