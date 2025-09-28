from typing import List

class State:

    def __init__(self,right: List, left: List ,father, torch: str, state_duration: int, game_time: int):
        self._total_time: int = 0 # Total time of the game until the current state including the time of the current state
        self._persons_moved: list = [] # List of people who move in the state
        self._f: int = 0 # Total cost of the state
        self._h: int = 0 # Heuristic cost of the state
        self._g: int = 0 # Cost of the path from the initial state to the current state
        self._left: List = left # List of people on the left side
        self._right: List = right # List of people on the right side
        self._father = father # Parent state
        self._state_duration: int = state_duration  # Time that the state lasts
        self._torch: str = torch # Torch position
        self._game_time: int = game_time # Time of the game
    
    # Getters
    @property
    def f(self):
        return self._f
    
    @property
    def g(self):
        return self._g
    
    @property
    def h(self):
        return self._h
    
    @property
    def father(self):
        return self._father
		
    @property
    def state_duration(self):
        return self._state_duration
    
    @property
    def torch(self):
        return self._torch
    
    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right
    
    @property
    def persons_moved(self):
        return self._persons_moved
    
    @property
    def total_time(self):
        return self._total_time
    
    @property
    def game_time(self):
        return self._game_time
 
    # Setters
    @f.setter
    def f(self, f):
        self._f = f

    @g.setter
    def g(self, g):
        self._g = g
   
    @h.setter
    def h(self, h):
        self._h = h
    
    @father.setter
    def father(self, f):
        self._father = f
    
    @total_time.setter
    def total_time(self,total):
        self._total_time = total
    
    @state_duration.setter
    def state_duration(self, time):
        self._state_duration = time

    @torch.setter
    def torch(self, torch):
        self._torch = torch

    @left.setter
    def left(self, left):
        self._left = left

    @right.setter
    def right(self, right):
        self._right = right

    @persons_moved.setter
    def persons_moved(self, persons_moved):
        self._persons_moved = persons_moved

    # Evaluate the state 
    def evaluate(self):
        self.f = self.calculate_G() + self.calculate_H() 
        return self.f
	
    # Calculate the cost of the path from the initial state to the current state
    def calculate_G(self):
        self.g = self.father.g + self.state_duration 
        return self.g
    
    # Calculate the heuristic cost of the state
    def calculate_H(self):
        total_score = 0 # Total score of the state
        individual = (len(self.persons_moved) == 1) # True if the move is individual, False otherwise
            
        # Calculate the score of the state taking into account if the move is individual or in pairs
        if self.torch == "right":  # the father has the torch on the left side and the child on the right side
           
            total_score += (10 + self.game_time) * (not individual)  # If the move is in pairs, the score is 10 + game_time, otherwise 0
           
            total_score += self.find_position_in_list() * self.state_duration # The time that the state lasts is multiplied by the position of the person in the list
           
        else:  # the father has the torch on the right side and the child on the left side
            
            total_score += (10 + self.game_time) * individual  # If the move is individual, the score is 10 + game_time, otherwise 0
            # Evaluate the movement of pairs moving to the left side
            if len(self.persons_moved) == 2:   
                total_score += self.evaluate_left_movement() 
           
           
        self.h = total_score
        return self.h

    # Evaluate the movement of people move from the right side to the left side
    def evaluate_left_movement(self):
        score = 0 # Score of the state
        sum_fast = 0 # Number of fast people on the left side

        father_left = self.father.left # List of people on the left side of the father
        father_right = self.father.right 
        
        sum_fast = sum(1 for person in father_left if person.fast)

        if sum_fast == 0: # No fast people on the left side so send the two fastest people
        # We have to give low score to the states that send the two fastest people otherwise high score
            if all(person.fast for person in self.persons_moved):
                score += 1
            else:
                score += self.state_duration * (10 + self.game_time)
                
        elif sum_fast >= 1: # One fast person on the left side so send the two slowest people
        # We have to give low score to states that send the two slowest people otherwise high score
            father_right = sorted(father_right, key=lambda person: person.p_time ,reverse=True)
            
            if (self.persons_moved[0].p_time ==father_right[0].p_time and self.persons_moved[1].p_time == father_right[1].p_time) \
                or (self.persons_moved[1].p_time==father_right[0].p_time and self.persons_moved[0].p_time==father_right[1].p_time):
                score += 1
            else:
                score += self.state_duration * (10 + self.game_time)

        return score


    # Find the position of the person in the list and return it 
    def find_position_in_list(self): 
        father_left = self.father.left
        if len(self.persons_moved)==1:
            person = self.persons_moved[0]
        else:
            self.persons_moved = sorted(self.persons_moved,key=lambda person: person.p_time)
            person= self.persons_moved[1]

        father_left = sorted(father_left, key=lambda person: person.p_time)

        position = father_left.index(person) + 1
        
        return position 

    # Get the children of the current state
    def get_children(self):
        children = []
        children = self.moveIndividual() + self.movePairs()
        return children
        
    # Move one person
    def moveIndividual(self):
        children = [] # List of children
        # If the torch is on the right side, the children are the people on the left side
        if self.torch == "right": 
            for person in self.right: 
                copy_left = self.left.copy() # Copy the list of people on the left side
                copy_right = self.right.copy() # Copy the list of people on the right side
                copy_right.remove(person)
                copy_left.append(person)
                
                # Create child state
                child = self.create_child_state(copy_right, copy_left, "left", person)
                if child is not None:    
                    children.append(child)
        else:
            for person in self.left:
                copy_left = self.left.copy() # Copy the list of people on the left side
                copy_right = self.right.copy() # Copy the list of people on the right side
                copy_left.remove(person)
                copy_right.append(person)
                
               # Create child state
                child = self.create_child_state( copy_right, copy_left, "right", person)
                if child is not None:
                    children.append(child)
            
        return children

    # Move two people
    def movePairs(self):
     
        children = []
        if self.torch == "right":
            for i in range(len(self.right)):
                for j in range(i + 1, len(self.right)):
                    person1 = self.right[i]
                    person2 = self.right[j]
                    if person1 != person2:  # Check that the persons are not the same
                        copy_left = self.left.copy() # Copy the list of people on the left side
                        copy_right = self.right.copy() # Copy the list of people on the right side
                        copy_right.remove(person1)
                        copy_right.remove(person2)
                        copy_left.append(person1)
                        copy_left.append(person2)
                        
                        # Create child state
                        child = self.create_child_state(copy_right, copy_left, "left", person1, person2)
                        if child is not None:
                            children.append(child)
                   
        else:
            for i in range(len(self.left)):
                for j in range(i + 1, len(self.left)):
                    person1 = self.left[i]
                    person2 = self.left[j]
                    if person1 != person2:  # Check that the persons are not the same
                        copy_left = self.left.copy() # Copy the list of people on the left side
                        copy_right = self.right.copy() # Copy the list of people on the right side
                        copy_left.remove(person1)
                        copy_left.remove(person2)
                        copy_right.append(person1)
                        copy_right.append(person2)
                        
                        # Create child state
                        child = self.create_child_state(copy_right, copy_left, "right", person1, person2)
                        if child is not None: 
                            children.append(child) # Add the child to the list of children
                   
    
        return children
    
    # Create a new state for individual or pair movement
    def create_child_state(self,right, left, torch, p1, p2=None):
        
        child = State(right=right, left=left, father=self, torch=torch, state_duration=max(p1.p_time, p2.p_time if p2 is not None else 0), game_time=self.game_time)
        
        # Add the people who move to the list of people who move
        child.persons_moved.append(p1)
        if p2 is not None:
            child.persons_moved.append(p2)

        # Update the total time of the game
        child.total_time += self.total_time + child.state_duration
        
        # Check that the child does not exceed the total time of the game
        if(child.total_time > self.game_time):
            return None

        child.evaluate() # Evaluate the child

        return child
    
    # Check if the state is final
    def is_final(self):
        return len(self.right) == 0
        
    # Compare two states
    def __lt__(self, s):
        return self.f < s.f
    
    # Return a string representation of the state
    def __repr__(self):
            left_times = [person.p_time for person in self.left]
            left_times.sort()
            right_times = [person.p_time for person in self.right]
            right_times.sort()
            moved_persons = [person.p_time for person in self.persons_moved]
            moved_persons.sort()
            state_str = "----------------------------\n"
            state_str += f"Torch position: {self.torch}\n"
            state_str += f"{left_times} ________ {right_times}\n"
            state_str += "\n"
            if self.total_time == 0:
                state_str += f"The game initialized, all people are on the right side.\n"
            else:
                state_str += f"Persons moved to {self.torch} side: {moved_persons}\n"
            state_str += f"Remaining time: {self.game_time - self.total_time}\n"
            state_str += "----------------------------\n"

            return state_str
