#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
#include <utility>
#include <random>
#include <nlohmann/json.hpp> 
#include<stack>
#include<tuple>
// For reading JSON files we need header file to include

using namespace std;
using json = nlohmann::json;

// Directions: right, down, left, up
const vector<pair<int, int>> DIRECTIONS = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

// Function to check if the next move is valid
bool is_valid_move(int x, int y, const vector<vector<int>>& battlefield) {
    int n = battlefield.size();
    return x >= 0 && x < n && y >= 0 && y < n && battlefield[x][y] != 4;
}

// BFS Pathfinding Algorithm with Multiple Sources
int bfs_multi_source(const vector<vector<int>>& battlefield, const vector<pair<int, int>>& sources, pair<int, int> target) {
    int n = battlefield.size();
    vector<vector<bool>> visited(n, vector<bool>(n, false));
    vector<vector<pair<int, int>>> parent(n, vector<pair<int, int>>(n, {-1, -1}));  // To track the previous node
    queue<pair<int, int>> q;

    // Initialize the queue with all sources
    for (const auto& source : sources) {
        q.push(source);
        visited[source.first][source.second] = true;
    }

    int steps = 0;
    while (!q.empty()) {
        int size = q.size();
        for (int i = 0; i < size; ++i) {
            auto [x, y] = q.front();
            q.pop();

            if (x == target.first && y == target.second) {
                // Reconstruct and print the path from target to one of the sources
                stack<pair<int, int>> path;
                while (x != -1 && y != -1) {
                    path.push({x, y});
                    tie(x, y) = parent[x][y];  // Move to the parent node
                }

                cout << "Path: ";
                while (!path.empty()) {
                    auto [px, py] = path.top();
                    path.pop();
                    cout << "(" << px << ", " << py << ")";
                    if (!path.empty()) cout << " -> ";
                }
                cout << endl;

                return steps; // Found the target, return the number of steps
            }

            for (const auto& [dx, dy] : DIRECTIONS) {
                int nx = x + dx, ny = y + dy;
                if (is_valid_move(nx, ny, battlefield) && !visited[nx][ny]) {
                    visited[nx][ny] = true;
                    parent[nx][ny] = {x, y};  // Track the parent node
                    q.push({nx, ny});
                }
            }
        }
        steps++;
    }

    return -1; // Return -1 if no path is found
}

// Function to locate the start (0) and target (6) positions
pair<pair<int, int>, pair<int, int>> find_positions(const vector<vector<int>>& battlefield) {
    pair<int, int> start = {-1, -1}, target = {-1, -1};
    for (int i = 0; i < battlefield.size(); ++i) {
        for (int j = 0; j < battlefield[i].size(); ++j) {
            if (battlefield[i][j] == 0) {
                start = {i, j};
            } else if (battlefield[i][j] == 6) {
                target = {i, j};
            }
        }
    }
    return {start, target};
}

// Function to read battlefield data from user input
vector<vector<int>> read_battlefield_from_user() {
    int n;
    cout << "Enter battlefield dimensions (n x n): ";
    cin >> n;
    vector<vector<int>> battlefield(n, vector<int>(n));

    cout << "Enter battlefield data row by row (use space to separate values):\n";
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> battlefield[i][j];
        }
    }

    return battlefield;
}

// Function to load battlefield from a JSON file
vector<vector<int>> read_battlefield_from_json(const string& file_path) {
    ifstream file(file_path);
    json j;
    file >> j;

    return j["data"].get<vector<vector<int>>>();
}

// Function to load battlefield from a UI exported JSON file
vector<vector<int>> read_battlefield_from_ui_json(const string& file_path) {
    ifstream file(file_path);
	vector<vector<int>> battlefield;
    json j;
    file >> j;
    //cout<<j;
	//file.close();

    // Loop through each layer and extract the "data"
    for (const auto& layer : j["layers"]) {
        vector<int> data = layer["data"].get<vector<int>>();
		cout<<data.size()<<endl;
        battlefield.push_back(data);
    }

    return battlefield;
  
}

/*
 * MAIN function (i.e Start of Programe execution).
 */

int main() {
	
    int option;
    vector<vector<int>> battlefield;

    /*
	 * Here We are Providing 2 Options for User. 
	   1. Input Battlefield Manually.
	   2. Read/Load Json file.
	 */
    cout << "Choose input method:\n";
    cout << "1. Input battlefield manually\n";
    cout << "2. Load battlefield from JSON file\n";
	//cout<< "3. Read Json File from UI export file.\n";
    cin >> option;

    if (option == 1) {
        battlefield = read_battlefield_from_user();
    } else if (option == 2) {
        string file_path;
        cout << "Enter JSON file path: ";
        cin >> file_path;
        battlefield = read_battlefield_from_json(file_path);
    // } else if (option ==3 )
    // {
		// string file_path;
        // cout << "Enter UI exported JSON file path: ";
        // cin >> file_path;
		
		// vector<vector<int>> dataArrays = read_battlefield_from_ui_json(file_path);

    // // Display the extracted data arrays
    // for (size_t i = 0; i < dataArrays.size(); ++i) {
			// cout << "Data Array " << i + 1 << ": ";
        // for (int val : dataArrays[i]) {
            // cout << val << " ";
        // }
        // cout << endl;
    // }
		
	 } else {
        cout << "Please Provide correct option.\n";
        return 1;
    }

     vector<pair<int, int>> sources;
    pair<int, int> target;

    // Locate the multiple sources (0s) and the single target (6)
    for (int i = 0; i < battlefield.size(); ++i) {
        for (int j = 0; j < battlefield[i].size(); ++j) {
            if (battlefield[i][j] == 0) {
                sources.push_back({i, j});
            } else if (battlefield[i][j] == 6) {
                target = {i, j};
            }
        }
    }

    int result = bfs_multi_source(battlefield, sources, target);
    if (result != -1) {
        cout << "Shortest path found in " << result << " steps.\n";
    } else {
        cout << "No path found.\n";
    }
    return 0;
}