#  CPP 
Path finding algorithm for battle units in a Real-Time Strategy (RTS) game
Solution:
BFS (Breadth-First Search) is ideal for the above problem because:
1. Shortest Path Guarantee: BFS explores all possible paths level by level, ensuring that the first time it reaches a goal, it finds the shortest path.
2. Uniform Grid Handling: The grid-based nature of the game UI fits well with BFS, as it efficiently processes each node (or tile) in layers.
3. Unweighted Edges: BFS is effective when all movements in the grid have the same cost, as it doesn't need to account for varying path costs.
4. Collision Detection: It naturally checks all neighboring nodes, ensuring that potential obstacles are easily detected.
5. Simple Implementation: BFS is straightforward to implement and understand, making it well-suited for handling pathfinding in grid-based games.
Functions Description:
// BFS Pathfinding Algorithm with Multiple Sources

int bfs_multi_source(const vector<vector<int>>& battlefield, const vector<pair<int, int>>& sources, pair<int, int> target)// Function to check if the next move is valid
bool is_valid_move(int x, int y, const vector<vector<int>>& battlefield)
Function to locate the start (0) and target (6) positions
pair<pair<int, int>, pair<int, int>> find_positions(const vector<vector<int>>& battlefield)
Function to read battlefield data from user input vector<vector<int>> read_battlefield_from_user()
Function to load battlefield from a JSON file
vector<vector<int>> read_battlefield_from_json(const string& file_path)
Function to load battlefield from a UI exported JSON file
vector<vector<int>> read_battlefield_from_ui_json(const string& file_path) Main function -> Start of execution
Example of CPP output.
![battlefield3](https://github.com/user-attachments/assets/03a9834b-3c70-45e7-a76a-6072eae2072a)

Example of Python output.


https://github.com/user-attachments/assets/5c2003ab-74c0-4c20-88ea-10a1c9fc3cd2


https://github.com/user-attachments/assets/4d782cff-40e2-4901-a19a-aa5968dde597


