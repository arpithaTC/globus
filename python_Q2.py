from copy import deepcopy
import json
import random
import cv2
import numpy as np
import imageio
from collections import deque

data = json.load(open('data2.json'))["data"]

starting_points = []
ending_points = []

# Find starting location
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == 0:
            starting_points.append((i, j))


# Find ending location
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == 6:
            ending_points.append((i, j))

def find_path(grid, start, ending_points):
    prev_point = {}
    def neighbors(point):
        i, j = point
        for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
            if 0 <= x < len(grid) and 0 <= y < len(grid[j]):
                print(x, y)
                if grid[x][y] != 4:
                    yield (x, y)

    queue = [start]
    dist = {start: 0}

    while queue:
        point = queue.pop(0)
        if point in ending_points:
            break

        for neighbor in neighbors(point):
            if neighbor not in dist:
                dist[neighbor] = dist[point] + 1
                prev_point[neighbor] = point
                queue.append(neighbor)

    path = []
    while point != start:
        path.append(point)
        point = prev_point[point]
    path.append(start)
    return path[::-1]

paths = []

for start_point in starting_points:
    path = find_path(data, start_point, ending_points)
    paths.append(path)

paths = [deque(path) for path in paths]
print(paths)
paths = sorted(paths, key=len)

trajectory = [[1] * len(paths)]
end_points_set = set(path[-1] for path in paths)
def get_number_of_non_end_points(points):
    return sum(1 for point in points if point not in end_points_set)
while set(trajectory[-1]) != end_points_set:
    current_points = [paths[i].popleft() for i in range(len(paths))]
    
    if len(set(current_points)-end_points_set) == get_number_of_non_end_points(current_points):
        trajectory.append(current_points)
    else:
        non_repeat_idx = random.randint(0, len(current_points)-1)
        for i in range(len(paths)):
            if i != non_repeat_idx:
                paths[i].appendleft(current_points[i])
        current_points = deepcopy(trajectory[-1])
        trajectory.append(current_points)
    for i in range(len(paths)):
        if len(paths[i]) == 0:
            paths[i].appendleft(current_points[i])

#     print(trajectory, ending_points)


# exit()
trajectory = trajectory[1:]

cv2.namedWindow("Animation2", cv2.WINDOW_NORMAL)
m, n = len(data), len(data[0])
anim = []
writer = cv2.VideoWriter('animation2.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (n*20, m*20))
for time, step in enumerate(trajectory):
    img = np.zeros((m*20, n*20, 3), dtype=np.uint8)
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == 4:
                img[i*20:(i+1)*20, j*20:(j+1)*20] = [128, 128, 128]
            elif cell == -1:
                img[i*20:(i+1)*20, j*20:(j+1)*20] = [255, 255, 255]
            if (i, j) in starting_points:
                # if (i, j) != start and (i, j) != end:
                img[i*20:(i+1)*20, j*20:(j+1)*20] = [255, 0, 0]
            if (i, j) in ending_points:
                # if (i, j) != start and (i, j) != end:
                img[i*20:(i+1)*20, j*20:(j+1)*20] = [0, 0, 255]
    
    # i, j = start; cv2.rectangle(img, (j*20, i*20), (j*20+20, i*20+20), (255, 0, 0), 1)
    
    # i, j = end; cv2.rectangle(img, (j*20, i*20), (j*20+20, i*20+20), (0, 0, 255), 1)
    
    # i, j = point
    for (i, j) in step:
        cv2.circle(img, (j*20+10, i*20+10), 8, (0, 0, 0), -1)
        cv2.circle(img, (j*20+10, i*20+10), 6, (255, 255, 255), -1)
    # cv2.circle(img, (start[1]*20+10, start[0]*20+10), 10, (0, 0, 0), -1)
    cv2.imshow("Animation", img)
    anim.append(img)
    cv2.waitKey(500)

    for _ in range(10):writer.write(img)

writer.release()

imageio.mimsave('animation2.gif', anim, fps=2)