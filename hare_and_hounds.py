# (turn, hound1, hound2, hound3, hare, stalls)

HOUND_PLAYER = 0
HARE_PLAYER = 1

UNDECIDED = 0
HOUND_WIN = 1
HOUND_LOSS = 2

#   1 4 7
# 0 2 5 8 10
#   3 6 9

EDGES = {
    0: {1, 2, 3},
    1: {0, 2, 4, 5},
    2: {0, 1, 3, 5},
    3: {0, 2, 5, 6},
    4: {1, 5, 7},
    5: {1, 2, 3, 4, 6, 7, 8, 9},
    6: {3, 5, 9},
    7: {4, 5, 8, 10},
    8: {5, 7, 9, 10},
    9: {5, 6, 8, 10},
    10: {7, 8, 9},
}

def _compress(turn, hound1, hound2, hound3, hare, stalls):
    hound_num = 0
    for i in range(hound1):
        hound_num += (9 - i) * (10 - i) // 2
    for i in range(hound1 + 1, hound2):
        hound_num += (10 - i)
    hound_num += hound3 - (hound2 + 1)

    left = turn * (2 ** 7)
    left += 11 * stalls + hare
    return left * (2 ** 8) + hound_num

def _uncompress(num):
    left = num // (2 ** 8)
    hound_num = num % (2 ** 8)
    hound1 = 0
    while (9 - hound1) * (10 - hound1) // 2 <= hound_num:
        hound_num -= (9 - hound1) * (10 - hound1) // 2
        hound1 += 1
    hound2 = hound1 + 1
    while (10 - hound2) <= hound_num:
        hound_num -= (10 - hound2)
        hound2 += 1
    hound3 = hound2 + 1 + hound_num
    turn = left // (2 ** 7)
    stalls = (left % (2 ** 7)) // 11
    hare = (left % (2 ** 7)) % 11
    return (turn, hound1, hound2, hound3, hare, stalls)

initial_position = _compress(HOUND_PLAYER, 0, 1, 3, 10, 0)

def primitive(pos):
    turn, hound1, hound2, hound3, hare, stalls = _uncompress(pos)
    if hare == 0: # Hare makes it to other side of board
        return HOUND_LOSS
    if turn == HARE_PLAYER:
        occupied = {hound1, hound2, hound3, hare}
        for new_space in EDGES[hare]:
            if new_space not in occupied:
                if stalls >= 10:
                    return HOUND_LOSS
                return UNDECIDED
        return HOUND_WIN # Hare has no moves
    else:
        if min(hound1, hound2, hound3, hare) >= 7:
            return HOUND_LOSS
    return UNDECIDED

def generate_moves(pos):
    turn, hound1, hound2, hound3, hare, stalls = _uncompress(pos)
    occupied = {hound1, hound2, hound3, hare}
    if turn == HOUND_PLAYER:
        for init_space in (hound1, hound2, hound3):
            for new_space in EDGES[init_space]:
                if new_space not in occupied and \
                    ((init_space - 1) // 3 <= (new_space - 1) // 3):
                    yield (init_space, new_space)
    else:
        for new_space in EDGES[hare]:
            if new_space not in occupied:
                yield new_space

def do_move(pos, move):
    turn, hound1, hound2, hound3, hare, stalls = _uncompress(pos)
    if turn == HOUND_PLAYER:
        init_space, new_space = move
        if (init_space - 1) // 3 == (new_space - 1) // 3:
            stalls += 1
        else:
            stalls = 0
        hounds = [hound1, hound2, hound3]
        hounds[hounds.index(init_space)] = new_space
        hounds.sort()
        hound1, hound2, hound3 = hounds
        turn = HARE_PLAYER
        new_pos = (turn, hound1, hound2, hound3, hare, stalls)
    else:
        hare = move
        turn = HOUND_PLAYER
        new_pos = (turn, hound1, hound2, hound3, hare, stalls)
    return _compress(*new_pos)
