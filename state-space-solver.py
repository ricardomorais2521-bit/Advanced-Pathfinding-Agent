from searchPlus import *

def create_line(x, y, dx, dy, length):
    """Creates a row of cells of a given length starting at (x,y) in direction (dx,dy)."""
    return {(x + i * dx, y + i * dy) for i in range(length)}

class GridNavigator(Problem):
    def __init__(self, agent_start, target_goal, platforms, max_jump=3, rows=12, cols=12):
        self.rows = rows # Number of rows in the environment grid
        self.cols = cols # Number of columns in the environment grid
        self.platforms = platforms
        self.max_jump = max_jump
        
        # State representation: (row, col, current_height, is_descending, horizontal_momentum)
        # Guarantees native equality and O(1) hashing efficiency for graph search.
        self.initial = (agent_start[0], agent_start[1], 0, False, False)
        self.goal = target_goal
        
        super().__init__(self.initial, self.goal)
    
    def actions(self, state):
        valid_actions = []
        r, c, h, is_descending, h_moved = state
        
        # Check if the agent is standing on a solid platform
        on_platform = (r + 1, c) in self.platforms
        
        # Action: Move Down (D)
        if r < self.rows - 1 and not on_platform and (r + 1, c) not in self.platforms:
            valid_actions.append('D')
            
        # Action: Move Left (L)
        if c > 0 and (r, c - 1) not in self.platforms:
            if on_platform or not h_moved:
                valid_actions.append('L')
                
        # Action: Move Right (R)
        if c < self.cols - 1 and (r, c + 1) not in self.platforms:
            if on_platform or not h_moved:
                valid_actions.append('R')
                
        # Action: Move Up (U)
        if r > 0 and (r - 1, c) not in self.platforms:
            if not is_descending and h < self.max_jump:
                valid_actions.append('U')
        
        valid_actions.sort()
        return valid_actions
    
    def result(self, state, action):
        r, c, h, is_descending, h_moved = state
        
        new_r, new_c = r, c
        new_h = h
        new_desc = is_descending
        new_h_moved = h_moved
        
        # Apply vector physics based on the chosen action
        if action == 'U':
            new_r -= 1
            new_h += 1
            new_h_moved = False # Vertical movement breaks horizontal inertia
        elif action == 'D':
            new_r += 1
            new_desc = True     # Triggers irreversible descent flag
            new_h_moved = False 
        elif action == 'L':
            new_c -= 1
            new_h_moved = True  # Registers lateral movement to force trajectory alternation
        elif action == 'R':
            new_c += 1
            new_h_moved = True  
            
        # Landing sequence: Reset flight constraints if landing on a solid platform
        if (new_r + 1, new_c) in self.platforms:
            new_h = 0
            new_desc = False
            new_h_moved = False
            
        return (new_r, new_c, new_h, new_desc, new_h_moved)
    
    def goal_test(self, state):
        # The target is fixed. The goal is a 2D spatial verification.
        return (state[0], state[1]) == self.goal
    
    def display(self, state):
        """Visualizes the grid environment and the agent's current state."""
        agent_pos = (state[0], state[1]) 
        output = ""
        for i in range(self.rows):
            for j in range(self.cols):
                if agent_pos == (i, j):
                    ch = '@' # Agent
                elif self.goal == (i, j):
                    ch = '&' # Target
                elif (i, j) in self.platforms:
                    ch = '#' # Platform/Obstacle
                else:
                    ch = '.' # Empty space
                output += ch + " "
            output += "\n"
        print(output)
        
    def execute(self, state, plan, show=False):
        """Executes a sequence of actions from the state, returning the final state,
        the accumulated cost, and a boolean indicating whether the objective was achieved.
        """
        cost = 0
        if show:
            self.display(state)
        for a in plan:
            seg = self.result(state, a)
            cost = self.path_cost(cost, state, a, seg)
            state = seg
            obj = self.goal_test(state)
            if show:
                print('Action Executed:', a)
                self.display(state)
                print('Total Cost:', cost)
                print('Goal Reached?', obj)
                print()
        return (state, cost, obj)