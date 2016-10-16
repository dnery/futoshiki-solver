import sys


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

    def __init__(self, bdim, board, values, constraints):
        self.bdim = bdim
        self.board = board
        self.values = values
        self.constraints = constraints


def empty_pos(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return Pos(i, j)

    return None


def empty_pos_lrv(board, values):
    max = 10  # greater than possible
    pos = None
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0 and (len(values[i][j]) > 0 and
                                     len(values[i][j]) < max):
                max = len(values[i][j])
                pos = Pos(i, j)
    return pos


def valid_pos(board, pos, num, constraints):
    # check cols
    for i in range(len(board)):
        if board[i][pos.y] == num:
            return False
    # check rows
    for j in range(len(board)):
        if board[pos.x][j] == num:
            return False
    # check constraints
    for c in constraints[pos.x][pos.y]:
        if board[c[1].x][c[1].y] == 0:
            continue

        if c[0] is True:
            if board[c[1].x][c[1].y] > num:
                return False
        else:
            if board[c[1].x][c[1].y] < num:
                return False

    return True


def remove_value(values, pos, num, constraints):
    memory = []
    for i in range(len(values)):
        if num in values[i][pos.y]:
            values[i][pos.y].remove(num)
            memory.append((num, Pos(i, pos.y)))
        if num in values[pos.x][i]:
            values[pos.x][i].remove(num)
            memory.append((num, Pos(pos.x, i)))

    for c in constraints[pos.x][pos.y]:
        if c[0] is True:
            removals = [x for x in values[c[1].x][c[1].y] if x > num]
        else:
            removals = [x for x in values[c[1].x][c[1].y] if x < num]

        for removal in removals:
            values[c[1].x][c[1].y].remove(removal)
            memory.append((removal, Pos(c[1].x, c[1].y)))

    return memory


def rewind_value(values, memory):
    for pos in memory:
        values[pos[1].x][pos[1].y].append(pos[0])


def no_more_values(board, values):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0 and len(values[i][j]) == 0:
                return True
    return False


def solve_shiki(board, constraints, branches):
    pos = empty_pos(board)
    # success
    if pos is None:
        return True
    # failure by effort
    if branches[0] > 1000000:
        return False

    for num in range(1, len(board) + 1):  # all numbers 1 to dim + 1
        if valid_pos(board, pos, num, constraints):
            branches[0] += 1
            board[pos.x][pos.y] = num

            if solve_shiki(board, constraints, branches):
                return True

            board[pos.x][pos.y] = 0
    # failure by exhaustion
    return False


def solve_shiki_fwd(board, values, constraints, branches):
    # pos = empty_pos(board)
    pos = empty_pos_lrv(board, values)
    # success
    if pos is None:
        return True
    # failure by effort
    if branches[0] > 1000000:
        return False

    static_vals = list(values[pos.x][pos.y])
    for num in static_vals:
        branches[0] += 1
        board[pos.x][pos.y] = num
        # remove value from row, col
        mem = remove_value(values, pos, num, constraints)
        # forward check pass
        if not no_more_values(board, values):
            if solve_shiki_fwd(board, values, constraints, branches):
                return True

        # reinsert value in row, col
        rewind_value(values, mem)
        board[pos.x][pos.y] = 0
    # failure by exhaustion
    return False


def print_shiki(board):
    for row in board:
        print(row)


def read_experiment(stream):
    next(stream)  # skip test count

    tests = []
    for line in stream:
        # ignore empty lines
        if not line.strip():
            continue
        # read dims
        line = line.split()
        bdim, cdim = int(line[0]), int(line[1])
        # read board
        board = []
        for i in range(bdim):
            line = next(stream).split()
            board.append([int(x) for x in line])
        # read constraints
        constraints = []
        for i in range(bdim):
            constraints.append([])
            for j in range(bdim):
                constraints[i].append([])
        for i in range(cdim):
            line = next(stream).split()
            bign = Pos(int(line[2]) - 1, int(line[3]) - 1)
            smln = Pos(int(line[0]) - 1, int(line[1]) - 1)
            constraints[bign.x][bign.y].append((True, smln))
            constraints[smln.x][smln.y].append((False, bign))
        # generate values
        values = []
        for i in range(bdim):
            values.append([])
            for j in range(bdim):
                values[i].append([x for x in range(1, bdim + 1)])
        for i in range(bdim):
            for j in range(bdim):
                if board[i][j] != 0:
                    remove_value(values, Pos(i, j), board[i][j], constraints)
        # append
        tests.append(Test(bdim, board, values, constraints))

    return tests


def main():
    if len(sys.argv) > 1:
        stream = open(sys.argv[1], 'r')
    else:
        stream = sys.stdin
    tests = read_experiment(stream)

    tno = 0
    for test in tests:
        tno += 1
        branches = [0]
        # status = solve_shiki(test.board, test.constraints, branches)
        status = solve_shiki_fwd(test.board, test.values, test.constraints,
                                 branches)
        print(tno, ':')

        if status:
            print_shiki(test.board)
            print('done in', branches[0], 'branches')
        else:
            print('no solution:', branches[0], 'branches taken')

if __name__ == '__main__':
    main()
