from __future__ import print_function
from sys import argv
from sys import exit
from sys import stdin
from timeit import timeit

# TODO (só pra contextualizar):
# 1. DONEZO - guardar dados de performance
# 2. usar inteiros (bit containers) ao invés de listas
# 3. outras otimizações:
#   3.1. DONEZO - <list>.append é reavaliado todo laço; isole referência antes
#   3.2. use `map' onde possível, em listas, ao invés de laços comuns


class Pos:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x, self.y = x, y


class Test:
    bdim = 0
    board = []
    values = []
    constraints = []
    branches = 0
    exectime = 0

    def __init__(self, bdim, board, values, constraints):
        self.bdim = bdim
        self.board = board
        self.values = values
        self.constraints = constraints


def bit_count(value):
    count = 0
    while value > 0:
        if value & 1 == 1:
            count += 1
        value = value >> 1
    return count


def empty_pos(test):
    for i in range(test.bdim):
        for j in range(test.bdim):
            if test.board[i][j] == 0:
                return Pos(i, j)
    return None


def lrv_empty_pos(test):
    max = 10
    pos = None
    for i in range(test.bdim):
        for j in range(test.bdim):  # nesse teste, fazer check se values[i] > 0
            if test.board[i][j] == 0 and (len(test.values[i][j]) > 0 and len(test.values[i][j]) < max):
                max = len(test.values[i][j])  # max = 2^(bdim)
                pos = Pos(i, j)
    return pos


def valid_pos(test, pos, num):
    # check rows, cols
    for i in range(test.bdim):
        if test.board[i][pos.y] == num:
            return False
        if test.board[pos.x][i] == num:
            return False
    # check constraints
    for c in test.constraints[pos.x][pos.y]:
        if test.board[c[1].x][c[1].y] == 0:
            continue
        elif c[0] is True and test.board[c[1].x][c[1].y] > num:
            return False
        elif c[0] is False and test.board[c[1].x][c[1].y] < num:
            return False
    return True


def propagate_removal(test, pos, num):
    test.board[pos.x][pos.y] = num
    # clear row, col
    memory = []
    appendf = memory.append  # append function
    for i in range(test.bdim):
        if num in test.values[i][pos.y]:
            test.values[i][pos.y].remove(num)
            appendf((num, Pos(i, pos.y)))
        if num in test.values[pos.x][i]:
            test.values[pos.x][i].remove(num)
            appendf((num, Pos(pos.x, i)))
    # satisfy constraints
    for c in test.constraints[pos.x][pos.y]:
        for x in list(test.values[c[1].x][c[1].y]):  # has to be a copy
            if (c[0] is True and x > num) or (c[0] is False and x < num):
                test.values[c[1].x][c[1].y].remove(x)
                appendf((x, Pos(c[1].x, c[1].y)))
    return memory


def rewind_removal(test, pos, memory):
    test.board[pos.x][pos.y] = 0
    for entry in memory:
        test.values[entry[1].x][entry[1].y].append(entry[0])


def no_more_values(test, pos):
    for i in range(test.bdim):
        if test.board[pos.x][i] == 0 and len(test.values[pos.x][i]) == 0:
            return True
        if test.board[i][pos.y] == 0 and len(test.values[i][pos.y]) == 0:
            return True
    return False


def solve_shiki(test):
    pos = empty_pos(test)
    # success
    if pos is None:
        return True
    # failure by effort
    if test.branches > 1e6:
        return False
    # all possible values overall
    for num in range(1, test.bdim + 1):
        if valid_pos(test, pos, num):
            test.board[pos.x][pos.y] = num
            test.branches += 1

            if solve_shiki(test):
                return True

            test.board[pos.x][pos.y] = 0
    # failure by exhaustion
    return False


def fwd_solve_shiki(test, scan_function):
    pos = scan_function(test)
    # success
    if pos is None:
        return True
    # failure by effort
    if test.branches > 1e6:
        return False
    # all possible values for this position
    for num in list(test.values[pos.x][pos.y]):
        # remove value from board
        mem = propagate_removal(test, pos, num)
        test.branches += 1
        # do forward check pass
        if not no_more_values(test, pos):
            if fwd_solve_shiki(test, scan_function):
                return True

        # reinsert value in board
        rewind_removal(test, pos, mem)
    # failure by exhaustion
    return False


def print_shiki(it, board):
    print(it)
    for row in board:
        print(*row)


def next_valid(stream):
    line = next(stream)
    while line.strip() == '':
        line = next(stream)
    return line


def read_experiment(stream):
    ntests = int(next_valid(stream))
    # read ntests
    tests = []
    for i in range(ntests):
        # read dimensions
        line = next_valid(stream).split()
        bdim, cdim = int(line[0]), int(line[1])

        # read game board
        board = []
        for i in range(bdim):
            line = next_valid(stream).split()
            board.append([int(x) for x in line])

        # generate constraint array
        constraints = []
        for i in range(bdim):
            constraints.append([])
            for j in range(bdim):
                constraints[i].append([])

        # populate constraint array
        for i in range(cdim):
            line = next_valid(stream).split()
            bign = Pos(int(line[2]) - 1, int(line[3]) - 1)
            smln = Pos(int(line[0]) - 1, int(line[1]) - 1)
            constraints[bign.x][bign.y].append((True, smln))
            constraints[smln.x][smln.y].append((False, bign))

        # generate possible values
        values = []
        for i in range(bdim):
            values.append([])
            for j in range(bdim):
                values[i].append([x for x in range(1, bdim + 1)])

        # clear pre-occupied positions
        test = Test(bdim, board, values, constraints)
        for i in range(bdim):
            for j in range(bdim):
                if board[i][j] != 0:
                    propagate_removal(test, Pos(i, j), board[i][j])
        # append
        tests.append(test)
    return tests


def call_wrapper(func, *args, **kwargs):
    def wrapped_call():
        return func(*args, **kwargs)
    return wrapped_call


def main():
    if len(argv) > 2:
        stream = open(argv[2], 'r')
    else:
        stream = stdin
    tests = read_experiment(stream)

    if argv[1] != 'a' and argv[1] != 'b' and argv[1] != 'c':
        print('Parametro \'', argv[1], '\'nao reconhecido')
        exit(1)

    for i in range(len(tests)):
        if argv[1] == 'a':
            wrapped = call_wrapper(solve_shiki, tests[i])
            tests[i].exectime = timeit(wrapped)
        elif argv[1] == 'b':
            wrapped = call_wrapper(fwd_solve_shiki, tests[i], empty_pos)
            tests[i].exectime = timeit(wrapped)
        elif argv[1] == 'c':
            wrapped = call_wrapper(fwd_solve_shiki, tests[i], lrv_empty_pos)
            tests[i].exectime = timeit(wrapped)

        if tests[i].branches < 1e6:
            print_shiki(i + 1, tests[i].board)
            print('done in', tests[i].branches, 'branches and',
                  tests[i].exectime, 'sec\'s\n')
        else:
            print(str(i + 1) + '\n', 'no solution :', tests[i].branches,
                  'branches taken,', tests[i].exectime, 'sec\'s elapsed\n')
    stream.close()

if __name__ == '__main__':
    main()
