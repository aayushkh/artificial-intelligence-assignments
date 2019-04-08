import time


def dfs(vertex, visited, invalid, depth):
    global total_nodes
    global high_point
    global super_set
    global all_set
    total_nodes += 1
    if depth > p:
        return
    if vertex not in invalid:
        visited.add(vertex)
        add_invalid(vertex, invalid)
        queue = all_set - invalid
        if summer(queue, depth) + sum(matrix[i[0]][i[1]] for i in visited) > high_point:
            if queue not in super_set:
                super_set.add(frozenset(queue))
                for node in queue:
                    dfs(node[:], visited.copy(), invalid.copy(), depth+1)
        else:
            return
    if depth == p:
        points.add(sum(matrix[i[0]][i[1]] for i in visited))
        if high_point < max(points):
            high_point = max(points)
    if not points:
        return None
    else:
        return max(points)


def summer(queue, depth):
    alt_list = []
    for node in queue:
        alt_list.append(matrix[node[0]][node[1]])
    alt_list.sort(reverse=True)
    return sum(alt_list[:(p-depth)])


def add_invalid(vertex, invalid):
    invalid.add(vertex)  # add the current vertex
    for x in range(n):  # row-wise and col-wise
        invalid.add((x, vertex[1]))
        invalid.add((vertex[0], x))
    for i, j in zip(range(vertex[0], -1, -1), range(vertex[1], -1, -1)):
        invalid.add((i, j))
    for i, j in zip(range(vertex[0], n, 1), range(vertex[1], n, 1)):
        invalid.add((i, j))
    for i, j in zip(range(vertex[0], n, 1), range(vertex[1], -1, -1)):
        invalid.add((i, j))
    for i, j in zip(range(vertex[0], -1, -1), range(vertex[1], n, 1)):
        invalid.add((i, j))


with open('input.txt') as input_file:
    lines = [line.rstrip() for line in input_file]
    start = time.time()
if len(lines) > 3:
    # valid, hence making an output file
    with open('output.txt', 'w') as output_file:
        # parse the first three lines
        n = int(lines[0])   # city dimension
        p = int(lines[1])   # no. of police officers
        s = int(lines[2])   # no. of scooters
        steps = lines[3:]
        step_matrix = [steps[i:i+12] for i in range(0, len(steps), 12)]

        # initializing an n*n list and assigning weights
        matrix = [[0 for x in range(n)] for x in range(n)]

        for i in steps:
            val = i.split(',')
            matrix[int(val[0])][int(val[1])] += 1

        all_set = set()
        for i in range(n):
            for j in range(n):
                all_set.add((i, j))

        m_matrix = [[None for x in range(n)] for x in range(n)]
        total_nodes = 0
        high_point = 0
        super_set = set()
        points = set()

        for i in range(n):
            for j in range(n):
                total_nodes += 1
                m_matrix[i][j] = dfs((i, j), set(), set(), 1)
                points.clear()

        end = time.time()
        flat_list = [item for sublist in m_matrix for item in sublist]
        print end - start
        print max(flat_list)
        output_file.write(str(max(flat_list)))

