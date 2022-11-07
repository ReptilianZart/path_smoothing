import itertools
from heapq import heappush, heappop
from itertools import count
import numpy as np

global_image = None
global_dimensions = None


def heuristic(a, b):
    """L infinity distance"""
    D = 5.0
    D2 = 1.4
    if a == b:
        return 0
    return D * max(abs(a[0] - b[0]),
                   abs(a[1] - b[1]))  # D * distance(a, b) + (D2 - 2 * D) * min(abs(a[0] - b[0]), abs(a[1] - b[1]))


def distance(a, b):
    a = np.array(a)
    b = np.array(b)
    return 0.1 * np.linalg.norm(
        a - b)  # 0.1 * ((abs(a[0] - b[0]))**2 + (abs(a[1] - b[1]))**2)  #0.1 + (float(img[b]) - float(img[a])) ** 2 #


def __get_neighbors(r: int, c: int, image):
    """
    Return neighbor directly above, below, right, and left
    """
    matrix = image
    shape = (matrix.shape[1], matrix.shape[0])
    neighbors = []

    # ensure neighbors are within image boundaries
    if r > 0:
        if image[c][r - 1] > 250:
            neighbors.append(((r - 1, c), 1))

    if r > 0 and c > 0:
        if image[c - 1][r - 1] > 250:
            neighbors.append(((r - 1, c - 1), 1.4))

    if r < shape[0] - 1:
        if image[c][r + 1] > 250:
            neighbors.append(((r + 1, c), 1))

    if r > 0 and c < shape[1] - 1:
        if image[c + 1][r - 1] > 250:
            neighbors.append(((r - 1, c + 1), 1.4))

    if r < shape[0] - 1:
        if c > 0 and image[c - 1][r + 1] > 250:
            neighbors.append(((r + 1, c - 1), 1.4))
    if c > 0:
        if image[c - 1][r] > 250:
            neighbors.append(((r, c - 1), 1))

    if r < shape[0] - 1 and c < shape[1] - 1:
        if image[c + 1][r + 1] > 250:
            neighbors.append(((r + 1, c + 1), 1.4))
    if c < shape[1] - 1:
        if image[c + 1][r] > 250:
            neighbors.append(((r, c + 1), 1))
    return neighbors


def check_for_obstacle(r, c):
    image = global_image
    dimensions = global_dimensions
    row_pixel, column_pixel, length, width = get_pixel_info(dimensions)
    pixels_inside = image[r - row_pixel - 1: r + row_pixel, c - column_pixel - 1:c + column_pixel]
    if dimensions == (1, 1):
        return image[r, c] > 250
    return (pixels_inside > 250).all()


def get_pixel_info(dimensions):
    length, width = dimensions
    row_pixel = int((length - 1) / 2)
    column_pixel = int((width - 1) / 2)
    return row_pixel, column_pixel, length, width


def __get_neighbors_dimensions(r: int, c: int):
    """
    Return neighbor directly above, below, right, and left
    """
    image = global_image

    dimensions = global_dimensions
    shape = (image.shape[1], image.shape[0])
    neighbors = []
    row_pixel, column_pixel, length, width = get_pixel_info(dimensions)
    # ensure neighbors are within image boundaries
    if r > length:
        if check_for_obstacle(c, r - length):
            distance = np.sqrt(((r - length) - r) ** 2 + (c - c) ** 2)
            neighbors.append(((r - length, c), int(distance)))

    if r > length and c > width:
        if check_for_obstacle((c - width), (r - length)):
            distance = int(np.sqrt(((r - length) - r) ** 2 + (c - (c - width)) ** 2))
            neighbors.append(((r - length, c - width), distance))

    if r < shape[0] - length and r>length:
        if check_for_obstacle(c, r + length):
            distance = int(np.sqrt(((r + length) - r) ** 2 + (c - c) ** 2))
            neighbors.append(((r + length, c), distance))

    if r > length and c < shape[1] - width:
        if check_for_obstacle(c + width, r - length):
            distance = int(np.sqrt(((r - length) - r) ** 2 + ((c + width) - c) ** 2))
            neighbors.append(((r - length, c + width), distance))

    if r < shape[0] - length and r > length:
        if c > width and check_for_obstacle(c - width, r + length):
            distance = int(np.sqrt(((r + length) - r) ** 2 + ((c - width) - c) ** 2))
            neighbors.append(((r + length, c - width), distance))
    if c > width and r > length:
        if check_for_obstacle(c - width, r):
            distance = int(np.sqrt((r - r) ** 2 + ((c - width) - c) ** 2))
            neighbors.append(((r, c - width), distance))

    if r < shape[0] - length and c < shape[1] - width:
        if check_for_obstacle(c + width, r + length):
            distance = int(np.sqrt(((r + length) - r) ** 2 + ((c + width) - c) ** 2))
            neighbors.append(((r + length, c + width), distance))
    if c < shape[1] - width and r > length:
        if check_for_obstacle(c + width, r):
            distance = int(np.sqrt(((r) - r) ** 2 + ((c + width) - c) ** 2))
            neighbors.append(((r, c + width), distance))
    return neighbors


def calculate_neigbours(r, c, image):
    width, height = image.shape
    radius = global_dimensions[0]#*global_dimensions[1]
    x_ = np.arange(max(c - radius, 0), min(c + radius + 1, width))
    y_ = np.arange(max(r - radius, 0), min(r + radius + 1, height))

    #x_, y_ = np.meshgrid(x_, y_)
    neig = []
    test = []

    for x, y in itertools.product(list(x_), list(y_)):

        width, height = image.shape
        X = x #+ c - 1
        Y = y #+ r - 1
        if (x, y) == (1, 1):
            continue
        if 0 <= X <= (width - radius) and (height - radius) >= Y >= 0:
            if image[Y][Y] > 250:
                distance = np.sqrt((X - c) ** 2 + (Y - r) ** 2)
                neig.append(((X, Y), distance))
            else:
                continue
    return neig

def reached_goal(current, goal):
    dimensions = global_dimensions
    r, c = current
    row_pixel, column_pixel, length, width = get_pixel_info(dimensions)
    row = np.arange(r - row_pixel - 1, r + row_pixel)
    column = np.arange(c - column_pixel - 1, c + column_pixel)
    for x, y in itertools.product(row, column):
        distance = int(np.sqrt((goal[0] - x) ** 2 + (goal[1] - y) ** 2))

        if (x, y) == goal or distance < (sum(dimensions)/2):
            return True
    return False


def optimal_path(start, goal, image):
    global global_image, global_dimensions

    global_image = image
    global_dimensions = (5, 5)

    print("shortest path called")
    push = heappush
    pop = heappop
    c = count()
    queue = [(0, next(c), start, 0, None)]
    enqueued = {}
    # Maps explored nodes to parent closest to the source.
    explored = {}

    count1 = 0

    while queue:
        count1 += 1
        # Pop the smallest item from queue.
        _, __, current_node, dist, parent = pop(queue)
        # plt.scatter(current_node[0], current_node[1])
        # if heuristic(current_node, goal) < 2.0:
        if reached_goal(current_node, goal):  # current_node == goal:
            path = [current_node]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if current_node in explored:
            # Do not override the parent of starting node
            if explored[current_node] is None:
                continue

            # Skip bad paths that were enqueued before finding a better one
            qcost, h = enqueued[current_node]
            if qcost < dist:
                continue

        explored[current_node] = parent
        neighbors = __get_neighbors_dimensions(current_node[0], current_node[1])
        for neighbor, w in neighbors:
            ncost = dist + w
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                # if qcost <= ncost, a less costly path from the
                # neighbor to the source was already determined.
                # Therefore, we won't attempt to push this neighbor
                # to the queue
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, goal)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, current_node))