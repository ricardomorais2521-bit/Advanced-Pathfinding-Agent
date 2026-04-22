# State-Space Search Agent 🤖

## 📌 Project Overview
This project focuses on **Classical Artificial Intelligence** and **Pathfinding Algorithms**. The objective was to formulate and implement a constraint-based state-space search problem from scratch using Python. 

The algorithm simulates an autonomous agent navigating a restricted grid environment (M x N) to reach a specific target while overcoming spatial limitations and obstacles.

## 🛠️ Technical Implementation
* **Language:** Python
* **Concepts Applied:** Object-Oriented Programming (OOP), State-Space Representation, Graph Search Algorithms (e.g., Breadth-First Search).
* **Core Logic:** The agent's movement is highly restricted by spatial physics. The algorithm handles maximum vertical limits, forced horizontal momentum, and landing constraints dynamically.
* **State Representation:** Immutable tuples `(row, col, height, descent_flag, horizontal_momentum)` ensuring native equality and O(1) hashing efficiency for search tree nodes.

## 🚀 How it Works
The `GridNavigator` class defines the environment dynamics and overrides the base `Problem` class:
1. `actions(state)`: Calculates all legally permissible moves (`Up`, `Down`, `Left`, `Right`) based on spatial constraints and current trajectory limits.
2. `result(state, action)`: Computes the resulting environmental state after applying vector physics, adjusting the agent's inertia and landing status.
3. `goal_test(state)`: Verifies spatial 2D alignment with the target destination.

## 💡 Key Learnings
Developing this algorithm reinforced my foundation in algorithmic logic, constraint satisfaction, and writing clean, scalable Python code for complex search spaces. This lays a solid groundwork for more advanced pathfinding models and reinforcement learning applications.
