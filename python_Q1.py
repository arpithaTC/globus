import json
import cv2
import numpy as np
import imageio

data = json.load(open('data.json'))["data"]

# Find starting location
for i, row in enumerate(data):
    try:
        j = row.index(0)
    except ValueError:
        continue
    if j != -1:
        start = (i, j)
        break

# Find ending location
for i, row in enumerate(data):
    try:
        j = row.index(6)
    except ValueError:
        continue
    if j != -1:
        end = (i, j)

# A dict to find the path
prev_point = {}

def find_path(grid, start, end):
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
        if point == end:
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


path = find_path(data, start, end)
print("Shortest path", path)

# for row in data:
#     print(row)

cv2.namedWindow("Animation", cv2.WINDOW_NORMAL)
m, n = len(data), len(data[0])
anim = []
writer = cv2.VideoWriter('animation.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (n*20, m*20))
for point in path:
    img = np.zeros((m*20, n*20, 3), dtype=np.uint8)
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            # if cell == 0:
            #     img[i*20:(i+1)*20, j*20:(j+1)*20] = [255, 0, 0]
            # elif cell == 6:
            #     img[i*20:(i+1)*20, j*20:(j+1)*20] = [0, 0, 255]
            if cell == 4:
                img[i*20:(i+1)*20, j*20:(j+1)*20] = [128, 128, 128]
            elif cell == -1:
                img[i*20:(i+1)*20, j*20:(j+1)*20] = [255, 255, 255]
    for i, j in path:
        # if (i, j) != start and (i, j) != end:
        img[i*20:(i+1)*20, j*20:(j+1)*20] = [0, 255, 0]
    
    i, j = start; cv2.rectangle(img, (j*20, i*20), (j*20+20, i*20+20), (255, 0, 0), 1)
    
    i, j = end; cv2.rectangle(img, (j*20, i*20), (j*20+20, i*20+20), (0, 0, 255), 1)
    
    i, j = point
    
    cv2.circle(img, (j*20+10, i*20+10), 8, (0, 0, 0), -1)
    cv2.circle(img, (j*20+10, i*20+10), 6, (255, 255, 255), -1)
    # cv2.circle(img, (start[1]*20+10, start[0]*20+10), 10, (0, 0, 0), -1)
    cv2.imshow("Animation", img)
    anim.append(img)
    cv2.waitKey(500)

    for _ in range(10):writer.write(img)

writer.release()

imageio.mimsave('animation.gif', anim, fps=2)