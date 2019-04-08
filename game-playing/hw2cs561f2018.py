import time


def efficiency_arr(current_arr, node):
    new_arr = [sum(x) for x in zip(current_arr, map(int, list(all_data_dict.get(node)[-7:])))]
    return new_arr


def validity_check(array, check):
    return not any(element > check for element in array)


def s_play(node, s_set, l_set, s_array, l_array, s_added_set, l_added_set):
    global total_nodes
    global l_remaining_set
    global s_remaining_set

    local_array = efficiency_arr(s_array, node)
    local_best_score = sum(local_array)
    total_nodes += 1

    if validity_check(local_array, p) is False:
        #  if no valid SPLA end game and return 0
        return 0

    # remove current node from s_set
    if node in s_set:
        s_set.remove(node)
    if node in l_set:
        l_set.remove(node)

    # add node to s_added
    s_added_set.add(node)

    # check if it can be pruned
    if tuple([frozenset(s_set), frozenset(s_added_set), frozenset(l_set), frozenset(l_added_set)]) in prune_dict:
        return prune_dict[tuple([frozenset(s_set), frozenset(s_added_set), frozenset(l_set), frozenset(l_added_set)])]

    if len(l_set) == 0 or validity_check(l_array, b) is False:
        #  if no LAHSA remaining or no valid LAHSA remaining
        for user in s_set.copy():
            curr_score = s_play(user, s_set.copy(), l_set.copy(), local_array[:], l_array, s_added_set.copy(), l_added_set.copy())
            if curr_score > local_best_score:
                local_best_score = curr_score
    elif len(s_set) == 0:
        return 0
    else:
        for user in l_set.copy():
            curr_score = l_play(user, s_set.copy(), l_set.copy(), local_array[:], l_array, s_added_set.copy(), l_added_set.copy())
            if curr_score > local_best_score:
                local_best_score = curr_score

    # add to prune_dict
    if tuple([frozenset(s_set), frozenset(s_added_set), frozenset(l_set), frozenset(l_added_set)]) not in prune_dict:
        if len(s_set) != 0 and len(l_set) != 0:
            prune_dict[tuple([frozenset(s_set), frozenset(s_added_set), frozenset(l_set), frozenset(l_added_set)])] = local_best_score

    return local_best_score


def l_play(node, s_set, l_set, s_array, l_array, s_added_set, l_added_set):
    global total_nodes
    global l_remaining_set
    global s_remaining_set

    local_array = efficiency_arr(l_array, node)
    local_best_score = 0
    total_nodes += 1

    if validity_check(local_array, b) is False:
        # LAHSA is full fill out SPLA for remaining
        for user in s_set.copy():
            curr_score = s_play(user, s_set.copy(), l_set.copy(), s_array, local_array[:], s_added_set.copy(), l_added_set.copy())
            if curr_score > local_best_score:
                local_best_score = curr_score
    else:
        # remove current node and play game
        if node in s_set:
            s_set.remove(node)
        if node in l_set:
            l_set.remove(node)

        # add node to s_added
        l_added_set.add(node)

        if len(s_set) == 0:  # last element assigned
            return 0
        else:
            for user in s_set.copy():
                curr_score = s_play(user, s_set.copy(), l_set.copy(), s_array, local_array[:], s_added_set.copy(), l_added_set.copy())
                if curr_score > local_best_score:
                    local_best_score = curr_score

    return local_best_score


with open('input.txt') as input_file:
    lines = [line.rstrip() for line in input_file]
    start = time.time()

    # parse the lines
    b = int(lines[0])  # no. of beds
    p = int(lines[1])  # no. of parking spaces
    L = int(lines[2])  # no. of applications chosen by LAHSA so far
    l_ids_list = lines[3:(3+L)]  # LAHSA applicants
    S = int(lines[3+L])  # no. of applications chosen by SPLA so far
    s_ids_list = lines[(4+L):(4+L+S)]  # SPLA applicants
    A = int(lines[4+L+S])  # total no. of applications
    all_data_list = lines[(5+L+S):(5+L+S+A)]  # all applicants

    all_ids_list = []
    for item in all_data_list:
        all_ids_list.append(item[:5])

    l_ids_set = set(l_ids_list)
    s_ids_set = set(s_ids_list)
    a_ids_set = set(all_ids_list)
    all_data_dict = dict(zip(all_ids_list, all_data_list))

    s_remaining_set = a_ids_set - (s_ids_set | l_ids_set)
    for id in s_remaining_set.copy():
        if all_data_dict.get(id)[10:13] != 'NYY':
            s_remaining_set.remove(id)

    l_remaining_set = a_ids_set - (s_ids_set | l_ids_set)
    for id in l_remaining_set.copy():
        if all_data_dict.get(id)[5] != 'F' or all_data_dict.get(id)[9] != 'N' or int(all_data_dict.get(id)[6:9]) < 18:
            l_remaining_set.remove(id)

    best_score = 0
    best_move = ''
    total_nodes = 0
    prune_dict = {}

    for move in s_remaining_set.copy():
        score = s_play(move, s_remaining_set.copy(), l_remaining_set.copy(), [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], set(), set())
        if score > best_score:
            best_score = score
            best_move = move

    print "best_score", best_score
    print "best_move", best_move
    end = time.time()
    print "total_nodes", total_nodes
    print end - start

with open('output.txt', 'w') as output_file:
    output_file.write(best_move)
