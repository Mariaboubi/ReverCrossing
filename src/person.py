class Person:
    def __init__(self, time):
        self._time: int = time # Time to cross the bridge
        self._fast: bool = False # True if the person is fast, False otherwise

    # Getters and setters
    @property 
    def p_time(self):
        return self._time

    @property
    def fast(self):
        return self._fast
    
    @p_time.setter
    def p_time(self,time):
        self._time = time

    @fast.setter
    def fast(self, fast):
        self._fast = fast
   
    # return a string representation of the person
    def __repr__(self):
        return " Time: " + str(self._time) + " " + "Fast: " + str(self._fast)
 