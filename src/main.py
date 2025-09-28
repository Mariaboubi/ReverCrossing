import sys
import time
from person import Person
from spacesearcher import spaceSearcher
from state import State

def main(args):

    game_time = int(sys.argv[1]) # Time of the game
    N = int(sys.argv[2]) # Number of people
    argumentList = sys.argv[3:] 
    
    if N != len(argumentList) : # Check that the number of arguments is correct
        print("Invalid arguments")
        sys.exit(1)

    if game_time < 0 or N < 0: # Check that the arguments are positive
        print("Invalid arguments")
        sys.exit(1)

    # Create the list of people
    people = []  
    for i in range (N): 
        person = Person(int(argumentList[i]))
        people.append(person)

    # Sort the list of people by time
    people = sorted(people, key=lambda person: person.p_time)
    # Set the first two people as fast
    people[0].fast = True
    people[1].fast = True

    # Create the initial state
    right = people
    left = []
    initialState = State(right,left,None,"right",0,game_time)

    # Create the space searcher
    spacesearcher = spaceSearcher() 
    
    start = time.time()

    # Search the space
    solution = spacesearcher.AStar(initialState)
    
    end = time.time()

    if solution is None:
        print("GAME OVER")
        print("Time has expired")
    else:
        # Get the path to the solution
        path = [solution]
        t = solution
        while t.father is not None:
            path.append(t.father)
            t = t.father

        print("\nSolution:\n")
        for s in path[::-1]:
            print(s)
            print("")
        print("Total time: ", str(solution.total_time))

    print("Search time:", end - start, "sec.")

if __name__ == '__main__':
    main(args = sys.argv) 