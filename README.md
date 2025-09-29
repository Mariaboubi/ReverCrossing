# River Crossing Challenge 

This project implements the classic **River Crossing challenge**, where players must transfer people from one side of the river to the other while following a set of constraints.  
The solution is implemented using the **A\* search algorithm**, ensuring that the optimal path is found.

---
## Problem Description
The challenge involves a set of rules that make the solution non-trivial.  
The goal is to transfer all people to the opposite riverbank without breaking the rules:

- At most **2 people** can be on the boat at the same time.  
- The process must be completed within a **limited total time**.  
- Each person has an individual crossing time, and the boat crossing duration is determined by the slower person on board.  


**Watch the video explaining the problem here:** 
👉 [River Crossing Problem Explanation](https://www.youtube.com/watch?v=5n6xmaS1D2A)  

For a more detailed description of the project and its implementation, check the **Project Description** included in the repository.
---

## Technologies
- Python  
- **A\*** Search Algorithm  

---

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Mariaboubi/ReverCrossing.git
2. Navigate to the src folder (cd src) and run:
    python main.py 30 5 1 3 6 8 12 
    (The first parameter is the total available time and theremaining ones represent the individual crossing times of each person.)

