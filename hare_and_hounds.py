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

def compress(turn, hound1, hound2, hound3, hare, stalls):
    hound_num = 0
    for i in range(hound1):
        hound_num += (9 - i) * (10 - i) // 2
    for i in range(hound1 + 1, hound2):
        hound_num += (10 - i)
    hound_num += hound3 - (hound2 + 1)

    left = turn * (2 ** 7)
    left += 11 * stalls + hare
    return left * (2 ** 8) + hound_num

def uncompress(num):
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

def current_player(num):
    return uncompress(num)[0]

initial_position = compress(HOUND_PLAYER, 0, 1, 3, 10, 0) # 2561

def primitive(pos):
    turn, hound1, hound2, hound3, hare, stalls = uncompress(pos)
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
    turn, hound1, hound2, hound3, hare, stalls = uncompress(pos)
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
    turn, hound1, hound2, hound3, hare, stalls = uncompress(pos)
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
    return compress(*new_pos)

import functools

@functools.lru_cache(maxsize=32768)
def solve_next_moves(current_pos):
    result = primitive(current_pos)
    if result != UNDECIDED:
        return []
    current_turn = uncompress(current_pos)[0]
    can_win = False
    fastest_win = float('inf')
    slowest_loss = 0
    best_move = None
    best_rest = None
    next_moves = []
    for move in generate_moves(current_pos):
        new_pos = do_move(current_pos, move)
        new_value, remoteness = solve(new_pos)
        next_moves.append({
            'move': move,
            'board': uncompress(new_pos), # ','.join([str(s) for s in uncompress(new_pos)]),
            'value': new_value,
            'remoteness': remoteness,
        })
    return next_moves

@functools.lru_cache(maxsize=32768)
def solve(current_pos):
    result = primitive(current_pos)
    if result != UNDECIDED:
        return result, 0
    current_turn = uncompress(current_pos)[0]
    can_win = False
    fastest_win = float('inf')
    slowest_loss = 0
    for move in generate_moves(current_pos):
        new_pos = do_move(current_pos, move)
        new_result, remoteness = solve(new_pos)
        if current_turn == HARE_PLAYER:
            if new_result == HOUND_LOSS:
                can_win = True
                if remoteness + 1 < fastest_win:
                    fastest_win = remoteness + 1
            elif not can_win:
                if remoteness + 1 > slowest_loss:
                    slowest_loss = remoteness + 1
        else:
            if new_result == HOUND_WIN:
                can_win = True
                if remoteness + 1 < fastest_win:
                    fastest_win = remoteness + 1
            elif not can_win:
                if remoteness + 1 > slowest_loss:
                    slowest_loss = remoteness + 1
    if current_turn == HOUND_PLAYER:
        if can_win:
            return HOUND_WIN, fastest_win
        return HOUND_LOSS, slowest_loss
    else:
        if can_win:
            return HOUND_LOSS, fastest_win
        return HOUND_WIN, slowest_loss

@functools.lru_cache(maxsize=32768)
def fancy_solve(current_pos):
    result = primitive(current_pos)
    if result != UNDECIDED:
        return result, 0, []
    current_turn = uncompress(current_pos)[0]
    can_win = False
    fastest_win = float('inf')
    slowest_loss = 0
    best_move = None
    best_rest = None
    for move in generate_moves(current_pos):
        new_pos = do_move(current_pos, move)
        new_result, remoteness, rest = solve(new_pos)
        if current_turn == HARE_PLAYER:
            if new_result == HOUND_LOSS:
                can_win = True
                if remoteness + 1 < fastest_win:
                    fastest_win = remoteness + 1
                    best_move = move
                    best_rest = rest
            elif not can_win:
                if remoteness + 1 > slowest_loss:
                    slowest_loss = remoteness + 1
                    best_move = move
                    best_rest = rest
        else:
            if new_result == HOUND_WIN:
                can_win = True
                if remoteness + 1 < fastest_win:
                    fastest_win = remoteness + 1
                    best_move = move
                    best_rest = rest
            elif not can_win:
                if remoteness + 1 > slowest_loss:
                    slowest_loss = remoteness + 1
                    best_move = move
                    best_rest = rest
    if current_turn == HOUND_PLAYER:
        if can_win:
            return HOUND_WIN, fastest_win, move_list
        return HOUND_LOSS, slowest_loss, move_list
    else:
        if can_win:
            return HOUND_LOSS, fastest_win, move_list
        return HOUND_WIN, slowest_loss, move_list

def main():
    pos = initial_position
    while primitive(pos) == UNDECIDED:
        # print(fancy_solve(pos))
        move = input('move: ')
        if ',' in move:
            move = move.split(',')
            move = (int(move[0].strip()), int(move[1].strip()))
        else:
            move = int(move.strip())
        pos = do_move(pos, move)

if __name__ == '__main__':
    # main()
    print(solve_next_moves(initial_position))
