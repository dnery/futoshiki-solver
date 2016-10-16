#!/usr/bin/env python3
import sys


class Pos:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x, self.y = x, y


class Test:
    bdim = 0
    cdim = 0
    board = []
    constraints = []

    def __init__(self, bdim, cdim, board, constraints):
        self.bdim = bdim
        self.cdim = cdim
        self.board = board
        self.constraints = constraints


def valid_location(board, pos, num, constraints):
    for i in range(len(board)):
        if board[i][pos.y] == num:
            return False

    for j in range(len(board)):
        if board[pos.x][j] == num:
            return False

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


def find_location(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return Pos(i, j)

    return None


def print_shiki(board):
    for row in board:
        print(row)


def solve_shiki(board, constraints, branches):
    pos = find_location(board)
    # success
    if pos is None:
        return True
    # failure by effort
    if branches[0] > 1000000:
        return False

    for num in range(1, len(board) + 1):  # all numbers 1 to dim + 1
        if valid_location(board, pos, num, constraints):
            branches[0] += 1
            board[pos.x][pos.y] = num
            if solve_shiki(board, constraints, branches):
                return True

            board[pos.x][pos.y] = 0
    # failure by exhaustion
    return False


def read_experiment(stream):
    next(stream)  # skip test

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
        # append
        tests.append(Test(bdim, cdim, board, constraints))

    return tests


def main():
    if len(sys.argv) > 1:
        stream = open(sys.argv[1], 'r')
    else:
        stream = sys.stdin
    tests = read_experiment(stream)

    tno = 1
    for test in tests:
        branches = [0]
        status = solve_shiki(test.board, test.constraints, branches)
        print(tno, ':')

        if status:
            print_shiki(test.board)
            print('done in', branches[0], 'branches')
        else:
            print('no solution:', branches[0], 'branches taken')
        tno += 1

if __name__ == '__main__':
    main()
