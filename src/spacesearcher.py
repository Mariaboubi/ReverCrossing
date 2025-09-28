import heapq

class spaceSearcher:
    def __init__(self):
        self.frontier = [] 

    # A Star Search  
    def AStar(self,initialState):
        if initialState.is_final(): # Check if the initial state is final state
           return initialState
        
        heapq.heappush(self.frontier, initialState) # Add the initial state to the frontier
      
        while len(self.frontier) > 0: # While the frontier is not empty

            currentState = heapq.heappop(self.frontier) # Get the first state from the frontier
            
            if currentState.is_final(): # Check if the current state is final
                return currentState
            
            children = currentState.get_children()
            for child in children: # Get the children of the current state

                heapq.heappush(self.frontier, child) # Add the children to the frontier


        return None

