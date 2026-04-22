# ----- Intelligent Systems: Advanced Pathfinding Agent -----

# --- Project Overview ---
This project focuses on **Classical Artificial Intelligence** and **Pathfinding Algorithms**. The objective was to formulate and implement a constraint-based state-space search problem from scratch using Python. 

The algorithm simulates an autonomous agent navigating a highly restricted 2D grid environment to reach a specific target while overcoming spatial limitations, gravity, and obstacles.

# --- Heuristic Optimization & A* Search ---
To optimize computational performance, the algorithm was upgraded from standard Breadth-First Search to **A* (A-Star) Search**. 
* **Compact State Representation:** The state tuples were heavily compressed. Complex variables like height, descent flags, and horizontal inertia are now encoded into a single integer `v`, drastically reducing the memory footprint of the search tree.
* **Custom Heuristic Function:** Implemented an advanced heuristic that calculates Manhattan Distance but actively predicts and prunes "Fatal Falls". By returning an infinite cost (`float('inf')`) when the agent enters an irreversible trajectory missing all solid platforms, the A* algorithm intelligently avoids expanding dead-end branches, accelerating execution time.

# --- Technical Implementation ---
* **Language:** Python
* **Concepts Applied:** Object-Oriented Programming (OOP), State-Space Representation, Graph Search Algorithms (A* Search, Breadth-First Search).
* **Core Logic:** The agent's movement is restricted by spatial physics. The algorithm handles maximum vertical flight limits, forced horizontal momentum, and landing constraints dynamically.
* **Algorithmic Efficiency:** Ensured native equality and O(1) hashing efficiency for search tree nodes through immutable tuple representations.

# --- How it Works ---
The `GridNavigator` class defines the environment dynamics and overrides the base `Problem` class:
1. `actions(state)`: Calculates all legally permissible moves (`Up`, `Down`, `Left`, `Right`) based on spatial constraints and current trajectory limits.
2. `result(state, action)`: Computes the resulting environmental state after applying vector physics, adjusting the agent's inertia and landing status.
3. `advanced_heuristic(node)`: The "brain" of the agent, evaluating the most promising paths and discarding mathematically impossible trajectories.

# --- Try it Yourself ---
To run the demonstration and see the agent solving a complex sample grid:
1. Clone this repository.
2. Ensure both `state-space-solver.py` and `searchPlus.py` are in the same directory.
3. Run the script from your terminal:
   ```bash
   python state-space-solver.py
