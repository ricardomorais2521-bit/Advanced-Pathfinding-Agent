from searchPlus import *

def create_line(x, y, dx, dy, length):
    """Creates a row of cells of a given length starting at (x,y) in direction (dx,dy)."""
    return {(x + i * dx, y + i * dy) for i in range(length)}

class GridNavigator(Problem):
    def __init__(self, agent_start, target_goal, platforms, max_jump=3, rows=12, cols=12):
        self.rows, self.cols = rows, cols
        # Highly optimized compact state: (row, col, v)
        # 'v' is a bit-level encoded integer tracking height, descent, and horizontal inertia
        self.initial = (agent_start[0], agent_start[1], 0)
        self.goal = target_goal
        self.platforms = platforms
        self.max_jump = max_jump

    directions = {"D": (1, 0), "L": (0, -1), "R": (0, 1), "U": (-1, 0)}

    def is_valid_move(self, state, action):
        r, c, v = state
        dr, dc = self.directions[action]
        
        # Horizontal inertia constraint
        if v % 2 == 1 and abs(dc) == 1: 
            return False
            
        nr, nc = r + dr, c + dc
        
        # Environment boundaries and collision detection
        if (nr, nc) in self.platforms or not (0 <= nr < self.rows and 0 <= nc < self.cols): 
            return False
            
        # Valid standing/landing verification
        if (nr + 1, nc) in self.platforms: 
            return True
            
        # Maximum flight ceiling constraint
        if v >= 2 * self.max_jump and dr == -1: 
            return False
            
        return True
    
    def actions(self, state):
        return [a for a in self.directions if self.is_valid_move(state, a)]
    
    def result(self, state, action):
        r, c, v = state
        dr, dc = self.directions[action]
        nr, nc = r + dr, c + dc
        
        # Landing: reset inertia vector
        if (nr + 1, nc) in self.platforms: 
            return (nr, nc, 0)
            
        # Lateral movement increments inertia flag
        if abs(dc) == 1: 
            return (nr, nc, v + 1)
            
        # Vertical physics handling
        if dr == -1: 
            v += 1 if v % 2 == 1 else 2
        else: 
            v = 2 * self.max_jump
            
        return (nr, nc, v)
    
    def goal_test(self, state):
        return state[:-1] == self.goal

    def advanced_heuristic(self, node):
        """
        Advanced heuristic for A* Search.
        Evaluates Manhattan distance but detects fatal trajectories (infinite cost).
        """
        r, c, v = node.state
        gr, gc = self.goal
        manhattan_dist = abs(r - gr) + abs(c - gc)
        
        # Irreversible descent detection
        if v >= 2 * self.max_jump:
            # Check if direct target acquisition is still physically possible
            dv_target, dh_target = gr - r, abs(gc - c)
            if dv_target >= 0 and dh_target <= dv_target:
                if not (v % 2 == 1 and dv_target == 0 and dh_target > 0):
                    return manhattan_dist
            
            # Check if any emergency landing platform is reachable
            is_safe = False
            for (pr, pc) in self.platforms:
                dv_platform, dh_platform = (pr - 1) - r, abs(pc - c)
                if dv_platform >= 0 and dh_platform <= dv_platform:
                    if not (v % 2 == 1 and dv_platform == 0 and dh_platform > 0):
                        is_safe = True
                        break
                        
            # Prune branch: Fatal fall detected
            if not is_safe:
                return float('inf')
                
        return manhattan_dist

    def display(self, state):
        agent_pos = state[:-1]
        output = ""
        for i in range(self.rows):
            for j in range(self.cols):
                if agent_pos == (i, j): ch = '@'
                elif self.goal == (i, j): ch = "&"
                elif (i, j) in self.platforms: ch = "#"
                else: ch = "."
                output += ch + " "
            output += "\n"
        print(output)

# ==========================================
# TEST EXECUTION (Demonstration)
# ==========================================
if __name__ == "__main__":
    from searchPlus import astar_search_plus_count
    
    # Complex Environment Setup
    platforms = create_line(6, 11, 0, 1, 2) | create_line(6, 18, 0, 1, 2) | create_line(4, 18, 0, 1, 2) | \
                create_line(2, 18, 0, 1, 2) | create_line(8, 18, 0, 1, 4) | create_line(10, 16, 0, 1, 1) | \
                create_line(11, 19, 0, 1, 1) | create_line(8, 16, 0, 1, 1) | create_line(1, 16, 1, 0, 8) | \
                create_line(6, 4, 0, 1, 1) | {(3, 13), (1, 10), (11, 11), (10, 6)}
                
    env = GridNavigator(agent_start=(5, 11), target_goal=(5, 4), platforms=platforms, max_jump=2, rows=12, cols=22)
    
    print("Environment Map:")
    env.display(env.initial)
    
    print("Calculating optimal path using A* Search with Fatal-Fall Heuristic...")
    result_node, expansions, visited = astar_search_plus_count(env, env.advanced_heuristic)
    
    if result_node:
        print(f"Solution found! Total cost: {result_node.path_cost}")
        print(f"Action sequence: {result_node.solution()}")
        print(f"Algorithm Efficiency -> Expansions: {expansions} | Visited: {visited + expansions}")
    else:
        print("No solution found.")
