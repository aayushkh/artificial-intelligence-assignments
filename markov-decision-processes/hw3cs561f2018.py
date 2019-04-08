import operator
import time
import numpy as np


directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# ------------------------------------------------------------------------------------------- #
# ------------------------------------ Utility functions ------------------------------------ #
# ------------------------------------------------------------------------------------------- #

def print_dir(direction):
    if direction == (-1, 0):
        return 'W'
    elif direction == (0, 1):
        return 'S'
    elif direction == (1, 0):
        return 'E'
    elif direction == (0, -1):
        return 'N'


def turn_right(direction):
    return directions[directions.index(direction) - 1]


def turn_left(direction):
    return directions[(directions.index(direction) + 1) % len(directions)]


def vector_addition(a, b):
    return tuple(map(operator.add, a, b))


def argmax(sequence, fn):
    best = sequence[0]
    best_score = fn(best)
    for x in sequence:
        x_score = fn(x)
        if x_score > best_score:
            best, best_score = x, x_score
    return best


def out_of_bounds(state):
    global s
    if 0 <= state[0] < s and 0 <= state[1] < s:
        return False
    return True

# --------------------------------------------------------------------------------------------- #
# -------------------------------------- MDP Classes ------------------------------------------ #
# --------------------------------------------------------------------------------------------- #

class MDP:

    def __init__(self, list_of_actions, terminals, transitions=None, states=None):
        self.states = states
        self.list_of_actions = list_of_actions
        self.terminals = terminals
        self.transitions = transitions or {}


class EmmDeePee(MDP):

    def __init__(self, grid, terminals, transitions=None, reward=None, states=None, gamma=0.9, epsilon=0.1):
        list_of_actions = directions
        reward = {}
        states = set()
        self.grid = grid
        self.size = len(grid)

        for x in range(self.size):
            for y in range(self.size):
                if grid[y][x]:
                    states.add((x, y))
                    reward[(x, y)] = grid[y][x]

        self.states = states
        self.reward = reward
        self.gamma = gamma
        self.epsilon = epsilon

        transitions = {}
        for state in states:
            transitions[state] = {}
            for action in list_of_actions:
                transitions[state][action] = self.innitialize_transitions(state, action)

        MDP.__init__(self, list_of_actions=list_of_actions, terminals=terminals, transitions=transitions, states=states)


    def actions(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.list_of_actions

    def state_reward(self, state):
        return self.reward[state]

    def innitialize_transitions(self, state, action):
        if action:
            return [(0.7, self.next_state(state, action)),
                    (0.1, self.next_state(state, turn_right(action))),
                    (0.1, self.next_state(state, turn_left(action))),
                    (0.1, self.next_state(state, turn_left(turn_left(action))))]
        else:
            return [(0.0, state)]

    def transition_list(self, state, action):
        return self.transitions[state][action] if action else [(0.0, state)]

    def next_state(self, state, direction):
        state1 = vector_addition(state, direction)
        return state1 if state1 in self.states else state


# ----------------------------------------------------------------------------------------------------- #
# ------------------------------------------ Value Iteration ------------------------------------------ #
# ----------------------------------------------------------------------------------------------------- #


def value_iteration(mdp):
    U1 = {s: 0 for s in mdp.states}
    while True:
        U = U1.copy()
        delta = 0
        for s in mdp.states:
            U1[s] = mdp.state_reward(s) + mdp.gamma * max(sum(probability * U[s1] for (probability, s1) in mdp.transition_list(s, a)) for a in mdp.actions(s))
            delta = max(delta, abs(U1[s] - U[s]))
        if delta <= mdp.epsilon * (1 - mdp.gamma) / mdp.gamma:
            return U


def best_policy(mdp, Utility):
    pi = {}
    for state in mdp.states:
        pi[state] = argmax(mdp.actions(state), lambda action: sum(probability * Utility[s1] for (probability, s1) in mdp.transition_list(state, action)))
    return pi


# ------------------------------------------------------------------------------------------------ #
# ------------------------------------------ Simulation ------------------------------------------ #
# ------------------------------------------------------------------------------------------------ #

with open('input.txt') as input_file:
    lines = [line.rstrip() for line in input_file]
    start_time = time.time()

    # parse the lines
    s = int(lines[0])  # matrix dimension
    n = int(lines[1])  # no. of cars
    o = int(lines[2])  # no. of obstacles
    o_ords = lines[3:(3 + o)]  # obstacle co-ordinates

    # making the set of obstacles
    o_map = set()
    o_list = []
    for item in o_ords:
        val = item.split(',')
        xny = (int(val[0]), int(val[1]))
        o_map.add(xny)
        o_list.append(xny)

    ns_ords = lines[(3 + o):(3 + o + n)]  # car start co-ordinates
    ne_ords = lines[(3 + o + n):(3 + o + 2 * n)]  # car end co-ordinates

    ns_list = []
    ne_list = []
    for ns, ne in zip(ns_ords, ne_ords):
        ns_val, ne_val = ns.split(','), ne.split(',')
        ns_tuple, ne_tuple = (int(ns_val[0]), int(ns_val[1])), (int(ne_val[0]), int(ne_val[1]))
        ns_list.append(ns_tuple)
        ne_list.append(ne_tuple)

    super_grid = []
    for k in range(n):
        score_grid = []
        for j in range(s):
            temp = []
            for i in range(s):
                if (i, j) not in o_map and (i, j) != ne_list[k]:
                    temp.append(-1)
                elif (i, j) in o_map:
                    temp.append(-101)
                else:
                    temp.append(99)
            score_grid.append(temp)
        super_grid.append(score_grid)

    g = [None for i in range(n)]
    U = [None for i in range(n)]
    policies = [None for i in range(n)]
    for i in range(n):
        g[i] = EmmDeePee(super_grid[i], terminals=[ne_list[i]])
        U[i] = value_iteration(g[i])
        policies[i] = best_policy(g[i], U[i])

    average = []
    for i in range(n):
        sum = 0
        for j in range(10):
            o_count = 0
            pos = ns_list[i]
            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k = 0
            while pos != ne_list[i]:
                move = policies[i][pos]
                if pos in o_map:  # obstacle hit
                    o_count += 1
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = turn_left(turn_left(move))
                        else:
                            move = turn_left(move)
                    else:
                        move = turn_right(move)
                k += 1
                new_pos = vector_addition(pos, move)
                if not out_of_bounds(new_pos):
                    pos = new_pos
            sum = sum + (100 - k)
            sum = sum - o_count * 100
        average.append(sum/10)
    print average

    with open('output.txt', 'w') as output_file:
        for i in range(len(average)):
            output_file.write(str(average[i]) + '\n')

    print "\nTime : ", time.time() - start_time
